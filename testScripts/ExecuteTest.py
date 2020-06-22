from action.PageAction import *
from util.ParseExcel import ParseExcel
from config.VarConfig import *
from util.Log import *
import traceback,random
from airtest.core.api import Template

# 创建解析Excel对象
excelObj = ParseExcel()
# 用例或用例步骤执行结束后，向excel中写执行结果信息
def writeTestResult(sheetObj, rowNo, colsNo, testResult, errorInfo = None, picPath = None):
    # 测试通过结果信息为绿色，失败为红色
    colorDict = {"pass":"green", "faild":"red"}

    # 因为“测试用例”工作表和“用例步骤sheet表”中都有测试执行时间和
    # 测试结果列，定义此字典对象是为了区分具体应该写哪个工作表
    colsDict = {"testCase":[testCase_runTime, testCase_testResult],"caseStep":[testStep_runTime, testStep_testResult]}
    try:
        # 在测试步骤sheet中，写入测试时间
        excelObj.writeCellCurrentTime(sheetObj, rowNo = rowNo, colsNo = colsDict[colsNo][0])
        # 在测试步骤sheet中，写入测试结果
        excelObj.writeCell(sheetObj, content = testResult, rowNo = rowNo, colsNo = colsDict[colsNo][1], style = colorDict[testResult])
        if errorInfo and picPath:
            # 在测试步骤sheet中，写入异常信息
            excelObj.writeCell(sheetObj, content = errorInfo, rowNo = rowNo, colsNo = testStep_errorInfo)
            # 在测试步骤sheet中，写入异常截图路径
            excelObj.writeCell(sheetObj, content = picPath, rowNo = rowNo, colsNo = testStep_errorPic)
        else:
            # 在测试步骤sheet中，清空异常信息单元格
            excelObj.writeCell(sheetObj, content = "",
                    rowNo = rowNo, colsNo = testStep_errorInfo)
            # 在测试步骤sheet中，清空异常信息单元格
            excelObj.writeCell(sheetObj, content = "",
                    rowNo = rowNo, colsNo = testStep_errorPic)
    except Exception as err:
        debug("写excel出错，%s" %traceback.print_exc())

def executeExcel(stepSheet,step,stepRow,keyWord,locationType,locatorExpression,operateValue):
    expressionStr = ""
    successfulSteps = 0
    # 构造需要执行的python语句，
    # 对应的是PageAction.py文件中的页面动作函数调用的字符串表示
    if keyWord and operateValue and locationType is None and locatorExpression is None:
        expressionStr = keyWord.strip() + "('" + operateValue + "')"
    elif keyWord and operateValue is None and locationType is None and locatorExpression is None:
        expressionStr = keyWord.strip() + "()"
    elif keyWord and locationType and operateValue and locatorExpression is None:
        expressionStr = keyWord.strip() + "('" + locationType.strip() + "', '" + operateValue + "')"
    elif keyWord and locationType and locatorExpression and operateValue:
        expressionStr = keyWord.strip() + "('" + locationType.strip() + "', '" + locatorExpression.replace("'",'"').strip() + "', '" + operateValue + "')"
    elif keyWord and locationType and locatorExpression and operateValue is None:
        expressionStr = keyWord.strip() + "('" + locationType.strip() + "', '" + locatorExpression.replace("'",'"').strip() + "')"
    # print(expressionStr)
    try:
        returnValue = eval(expressionStr)
        # 在测试执行时间列写入执行时间
        excelObj.writeCellCurrentTime(stepSheet, rowNo=step, colsNo=testStep_runTime)
    except Exception as err:
        # 截取异常屏幕图片
        capturePic = capture_screen()
        # 获取详细的异常堆栈信息
        errorInfo = traceback.format_exc()
        # 在测试步骤Sheet中写入失败信息
        writeTestResult(stepSheet, step, "caseStep", "faild", errorInfo, capturePic)
        info("步骤“%s”执行失败！" % stepRow[testStep_testStepDescribe - 1].value)
    else:
        # 在测试步骤Sheet中写入成功信息
        writeTestResult(stepSheet, step, "caseStep", "pass")
        # 每成功一步，successfulSteps变量自增1
        successfulSteps += 1
        info("步骤“%s”执行通过！" % stepRow[testStep_testStepDescribe - 1].value)
        return returnValue

def selectExcelSheet(jsonDict):
    caseStepSheetName = '1'  # 默认类型为场景集合页或普通商品
    executeScene = '2'  # 默认为微信环境呼起app，1表示微信环境，2表示QQ环境
    #获取执行脚本终端类型，orderTerminal
    # 1:PC端  2:M端  3:小程序端  4:App端  5:APP端跨M  6:PC端跨M  7:PC端跨App端
    TerminalType = jsonDict.get('orderTerminal','1')  #如果不存在该字段，默认PC端执行下单操作
    if TerminalType == '1':
        linkTypeName = jsonDict.get("linkType",'1')
        if linkTypeName == '1':
            excelObj.loadWorkBook(PCorderBusinessFilePath)
            caseStepSheetName = orderBusinessDict.get(jsonDict.get('orderBusinessType'))
        else:
            excelObj.loadWorkBook(PCorderCommodityFilePath)
            caseStepSheetName = orderCommodityDict.get(jsonDict.get('orderCommodityType'))
    elif TerminalType == '2':
        pass #增加m端读取excel文件代码
    elif TerminalType == '3':
        pass #增加小程序端读取excel文件代码
    elif TerminalType == '4':
        #增加App端读取excel文件代码
        if TerminalType == '1':
            linkTypeName = jsonDict.get("linkType", '1')
            if linkTypeName == '1':
                if executeScene == '1':
                    excelObj.loadWorkBook(WchatorderBusinessFilePath)
                else:
                    excelObj.loadWorkBook(QQorderBusinessFilePath)
                caseStepSheetName = orderBusinessDict.get(jsonDict.get('orderBusinessType'))
            else:
                if executeScene == '1':
                    excelObj.loadWorkBook(WchatorderCommodityFilePath)
                else:
                    excelObj.loadWorkBook(QQorderCommodityFilePath)
                caseStepSheetName = orderCommodityDict.get(jsonDict.get('orderCommodityType'))
    else:
        pass #后续增加跨屏操作
    return caseStepSheetName

def PCExecuteTest(jsonDict):
    caseStepSheetName = selectExcelSheet(jsonDict)
    try:
        # 根据用例步骤名获取步骤sheet对象
        stepSheet = excelObj.getSheetByName(caseStepSheetName)
        # 获取步骤sheet中步骤数
        stepNum = excelObj.getRowsNumber(stepSheet)
        for step in range(2, stepNum + 1):
            # 因为步骤sheet中的第一行为标题行，无需执行
            # 获取步骤sheet中第step行对象
            stepRow = excelObj.getRow(stepSheet, step)
            # 获取关键字作为调用的函数名
            keyWord = stepRow[testStep_keyWords - 1].value
            # 获取操作元素定位方式作为调用的函数的参数
            locationType = stepRow[testStep_locationType - 1].value
            # 获取操作元素的定位表达式作为调用函数的参数
            locatorExpression =stepRow[testStep_locatorExpression-1].value
            # 获取操作值作为调用函数的参数
            operateValue = stepRow[testStep_operateValue - 1].value
            # 将操作值为数字类型的数据转成字符串类型，方便字符串拼接
            if isinstance(operateValue, int):
                operateValue = str(operateValue)
            #列出execute函数的入参
            args = stepSheet, step, stepRow, keyWord, locationType, locatorExpression, operateValue
            returnValue = executeExcel(*args)
    except Exception as err:
        # 打印详细的异常堆栈信息
        debug(traceback.print_exc())
    finally:
        eval("close_browser()")
        return returnValue


def mobileExecuteTest(jsonDict):
    caseStepSheetName = selectExcelSheet(jsonDict)
    try:
        # 根据用例步骤名获取步骤sheet对象
        stepSheet = excelObj.getSheetByName(caseStepSheetName)
        # 获取步骤sheet中步骤数
        stepNum = excelObj.getRowsNumber(stepSheet)
        for step in range(2, stepNum + 1):
            stepRow = excelObj.getRow(stepSheet, step)
            keyWord = stepRow[mobile_keyWords - 1].value
            #testStep_locationType表示对应图片名称或app原生路径
            picValue = stepRow[mobile_picPath-1].value
            threshold = stepRow[mobile_threshold-1].value
            target_pos = stepRow[mobile_target_pos-1].value
            rgb = stepRow[mobile_rgb-1].value




class Order(object):
    def __init__(self,stepbook,OrderType):
        self.excelbook = ParseExcel()
        self.excelbook.loadWorkBook(stepbook)
        self.OrderType = OrderType
        self.stepbook = stepbook

    def Order(self,poco):
        '''
        :param poco: 表示poco对象，用于调用安卓原生组件
        :param type: 表示要下单的类型，包括单品、二合一、三合一等
        :return: 返回订单号
        '''
        basePath = os.path.split(self.stepbook)[0]  #获取存放step和图片的路径
        try:
            stepSheet = self.excelbook.getSheetByName(self.OrderType)
            executeColumn = self.excelbook.getColumn(stepSheet, 1)
            for idx, i in enumerate(executeColumn[1:],2):
                stepRow = self.excelbook.getRow(stepSheet, idx)
                # 获取关键字作为调用的函数名
                functionId = stepRow[2].value
                # 获取函数的参数
                argv = stepRow[3].value
                expressionStr = functionId+'('+str(argv)+')'
                print(expressionStr)
                eval(expressionStr)
            orderId = poco("com.jd.lib.ordercenter:id/apb").get_text()
        except Exception as error:
            traceback.print_exc()
        else:
            return orderId
if __name__ == '__main__':
    runScriptJson = {"linkType": "2", "promotionLinkType": "1", "shopType": "1",
                     "orderTerminal": "1", "operationType": "1", "builtInType": "sdk",
                     "desType": "getcopon", "sdkType": "unionSdk", "orderplatform": "android",
                     "bitType": "32", "orderBusinessType": "2", "orderCommodityType": "4"}
    PCExecuteTest(runScriptJson)

from action.PageAction import *
from action.AppAction import *
from util.ParseExcel import ParseExcel
from config.VarConfig import *
from util.Log import *
import traceback,random
from airtest.core.api import Template


def writeTestResult(excelObj, sheetObj, rowNo, colsNo, testResult, errorInfo=None, picPath=None):
    # 因为“测试用例”工作表和“用例步骤sheet表”中都有测试执行时间和测试结果列，定义此字典对象是为了区分具体应该写哪个工作表
    # 测试通过结果信息为绿色，失败为红色
    colorDict = {"pass": "green", "faild": "red"}
    #写入测试时间和测试结果（pass或fail）
    colsDict = {"mobile": [mobile_runTime, mobile_testResult,mobile_errorInfo,mobile_errorPic],
                "pc": [testStep_runTime, testStep_testResult,testStep_errorInfo,testStep_errorPic]}
    try:
        # 在测试步骤sheet中，写入测试时间
        excelObj.writeCellCurrentTime(sheetObj, rowNo=rowNo, colsNo=colsDict[colsNo][0])
        # 在测试步骤sheet中，写入测试结果
        excelObj.writeCell(sheetObj, content=testResult, rowNo=rowNo, colsNo=colsDict[colsNo][1], style=colorDict[testResult])
        if errorInfo or picPath:
            # 在测试步骤sheet中，写入异常信息
            excelObj.writeCell(sheetObj, content=errorInfo, rowNo=rowNo, colsNo=colsDict[colsNo][2])
            # 在测试步骤sheet中，写入异常截图路径
            excelObj.writeCell(sheetObj, content=picPath, rowNo=rowNo, colsNo=colsDict[colsNo][3])
        # else:
        #     # 在测试步骤sheet中，清空异常信息单元格
        #     excelObj.writeCell(sheetObj, content = "",rowNo = rowNo, colsNo = testStep_errorInfo)
        #     # 在测试步骤sheet中，清空异常信息单元格
        #     excelObj.writeCell(sheetObj, content = "",rowNo = rowNo, colsNo = testStep_errorPic)
    except Exception as err:
        debug("写excel出错，%s" % traceback.print_exc())

class executeScriptWithPC(object):
    #针对pc环境的脚本执行操作
    def __init__(self,FilePath):
        # 创建解析Excel对象
        self.excelObj = ParseExcel()
        self.excelFile = FilePath
        self.excelObj.loadWorkBook(FilePath)

    def executeStep(self,stepSheet,step,stepDescribe,keyWord,locationType,locatorExpression,operateValue):
        #执行web主流程测试步骤，并记录测试结果到excel文件中
        #初始化执行语句表达式为空
        expressionStr = ""
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
        print(expressionStr)
        try:
            eval(expressionStr)
            # 在测试执行时间列写入执行时间
            self.excelObj.writeCellCurrentTime(stepSheet, rowNo=step, colsNo=testStep_runTime)
        except Exception as err:
            # 截取异常屏幕图片
            capturePic = capture_screen()
            # 获取详细的异常堆栈信息
            errorInfo = traceback.format_exc()
            # 在测试步骤Sheet中写入失败信息
            writeTestResult(self.excelObj,stepSheet, step, "pc", "faild", errorInfo, capturePic)
            info("步骤“%s”执行失败! 函数执行表达式为：%s" %(stepDescribe,expressionStr))
        else:
            # 在测试步骤Sheet中写入成功信息
            writeTestResult(self.excelObj,stepSheet, step, "pc", "pass")
            info("步骤“%s”执行通过！函数执行表达式为：%s" %(stepDescribe,expressionStr))

    def execute(self,caseStepSheetName):
        #根据测试sheetName，遍历表单中的测试步骤
        try:
            # 根据用例步骤名获取步骤sheet对象
            info('开始<%s>场景的测试...' % caseStepSheetName)
            stepSheet = self.excelObj.getSheetByName(caseStepSheetName)
            # 获取步骤sheet中步骤数
            stepNum = self.excelObj.getRowsNumber(stepSheet)
            for step in range(2, stepNum + 1):
                # 因为步骤sheet中的第一行为标题行，无需执行
                # 获取步骤sheet中第step行对象
                stepRow = self.excelObj.getRow(stepSheet, step)
                #获取测试步骤描述
                stepDescribe = stepRow[testStep_testStepDescribe - 1].value
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
                args = stepSheet, step, stepDescribe, keyWord, locationType, locatorExpression, operateValue
                self.executeStep(*args)
        except Exception as err:
            # 打印详细的异常堆栈信息
            debug(traceback.print_exc())
        finally:
            eval("close_browser()") #最终关闭浏览器

    def getOrderId(self):
        #获取订单号
        #参数在varConfig全局配置中定义
        return getAttr(expression_type,expression_str,expression_value)

class executeScriptWithMobile(object):
    #针对移动终端的脚本执行操作
    def __init__(self,FilePath):
        self.excelObj = ParseExcel()
        self.excelFile = FilePath
        self.excelObj.loadWorkBook(FilePath)

    def executeStep(self,stepSheet,step,stepDescribe,keyWord,picValue,threshold,target_pos,rgb):
        temp = "" #初始化中间临时变量
        # 构造需要执行的python语句，对应的是AppAction.py文件中的终端动作函数调用的字符串表示
        if isinstance(picValue, int):
            picValue = str(picValue)
        if picValue and picValue.endswith('.png'):
            picValue = os.path.join(os.path.split(self.excelFile)[0], picValue)
        if threshold is None and target_pos is None and rgb is None:
            if picValue and picValue.endswith('.png'):
                temp = "(Template(r'" + picValue + "'))"
            else:
                temp = "'" + picValue + "'"
        elif threshold and target_pos is None and rgb is None:
            temp = "Template(r'" + picValue + "', threshold=" + str(threshold) + ")"
        elif threshold is None and target_pos and rgb is None:
            temp = "Template(r'" + picValue + "', target_pos=" + str(target_pos) + ")"
        elif threshold is None and target_pos is None and rgb:
            temp = "Template(r'" + picValue + "', rgb=" + rgb + ")"
        elif threshold and target_pos and rgb is None:
            temp = "Template('r" + picValue + "', threshold=" + str(threshold) + ", target_pos=" + str(
                target_pos) + ")"
        elif threshold and target_pos is None and rgb:
            temp = "Template(r'" + picValue + "', threshold=" + str(threshold) + ", rgb=" + rgb + ")"
        elif threshold is None and target_pos and rgb:
            temp = "Template(r'" + picValue + "', target_pos=" + str(target_pos) + ", rgb=" + rgb + ")"
        elif threshold and target_pos and rgb:
            temp = "Template(r'" + picValue + "', threshold=" + str(threshold) + ", target_pos=" + str(
                target_pos) + ", rgb=" + rgb + ")"
        expressionStr = keyWord.strip() + "(" + temp + ")"
        # 执行表达式
        print(expressionStr)
        try:
            eval(expressionStr)
            # 在测试执行时间列写入执行时间
            self.excelObj.writeCellCurrentTime(stepSheet, rowNo=step, colsNo=mobile_runTime)
        except Exception as err:
            # 截取异常屏幕图片
            capturePic = snapShot()
            # 获取详细的异常堆栈信息
            errorInfo = traceback.format_exc()
            # 在测试步骤Sheet中写入失败信息
            writeTestResult(self.excelObj, stepSheet, step, "mobile", "faild", errorInfo, capturePic)
            info("步骤“%s”执行失败！函数执行表达式为：%s" % (stepDescribe, expressionStr))
        else:
            # 在测试步骤Sheet中写入成功信息
            writeTestResult(self.excelObj, stepSheet, step, "mobile", "pass")
            # 记录syslog信息
            info("步骤“%s”执行通过！函数执行表达式为：%s" % (stepDescribe, expressionStr))

    def execute(self,caseStepSheetName):
        # 利用aritest执行手机终端，遍历指定excel表单中的内容
        try:
            # 根据用例步骤名获取步骤sheet对象
            info('开始<%s>场景的测试...' % caseStepSheetName)
            stepSheet = self.excelObj.getSheetByName(caseStepSheetName)
            # 获取步骤sheet中步骤数
            stepNum = self.excelObj.getRowsNumber(stepSheet)
            for step in range(2, stepNum + 1):
                stepRow = self.excelObj.getRow(stepSheet, step)
                # 获取excel表单中每一行单元格的数据
                stepDescribe = stepRow[testStep_testStepDescribe - 1].value
                keyWord = stepRow[mobile_keyWords - 1].value
                picValue = stepRow[mobile_picPath - 1].value
                threshold = stepRow[mobile_threshold - 1].value
                target_pos = stepRow[mobile_target_pos - 1].value
                rgb = stepRow[mobile_rgb - 1].value
                args = stepSheet,step,stepDescribe,keyWord,picValue,threshold,target_pos,rgb
                self.executeStep(*args)
        except Exception as err:
            # 打印详细的异常堆栈信息
            debug(traceback.print_exc())

    def getOrderId(self):
        # 获取订单号
        if jsonDict.get('orderTerminal') == '4':
            time.sleep(5)
            return TerminalPoco("com.jd.lib.ordercenter:id/atm").get_text()

if __name__ == '__main__':
    runScriptJson = {"linkType": "2", "promotionLinkType": "1", "shopType": "1",
                     "orderTerminal": "1", "operationType": "1", "builtInType": "sdk",
                     "desType": "getcopon", "sdkType": "unionSdk", "orderplatform": "android",
                     "bitType": "32", "orderBusinessType": "2", "orderCommodityType": "4"}
    # PCExecuteTest(runScriptJson)
    # es = executeScript(runScriptJson)
    # print(es.getTerminalSN())
from action.PageAction import *
from util.ParseExcel import ParseExcel
from config.VarConfig import *
from util.Log import *
import traceback,random
from airtest.core.api import Template
from action.AppAction import *

class executeScript(object):

    def __init__(self,jsonDict):
        # 创建解析Excel对象
        self.excelObj = ParseExcel()
        # 测试通过结果信息为绿色，失败为红色
        self.colorDict = {"pass":"green", "faild":"red"}
        # 前端请求的json串转换的字典格式
        self.jsonDict = dict(jsonDict)

    # 用例或用例步骤执行结束后，向excel中写执行结果信息
    def writeTestResult(self,sheetObj, rowNo, colsNo, testResult, errorInfo = None, picPath = None,secen=None):
        # 因为“测试用例”工作表和“用例步骤sheet表”中都有测试执行时间和
        # 测试结果列，定义此字典对象是为了区分具体应该写哪个工作表
        if secen is not None:
            colsDict = {"testCase": [mobile_runTime, mobile_testResult],
                        "caseStep": [mobile_runTime, mobile_testResult]}
        else:
            colsDict = {"testCase":[testCase_runTime, testCase_testResult],"caseStep":[testStep_runTime, testStep_testResult]}
        try:
            # 在测试步骤sheet中，写入测试时间
            self.excelObj.writeCellCurrentTime(sheetObj, rowNo = rowNo, colsNo = colsDict[colsNo][0])
            # 在测试步骤sheet中，写入测试结果
            self.excelObj.writeCell(sheetObj, content = testResult, rowNo = rowNo, colsNo = colsDict[colsNo][1], style = self.colorDict[testResult])
            if errorInfo and picPath:
                # 在测试步骤sheet中，写入异常信息
                self.excelObj.writeCell(sheetObj, content = errorInfo, rowNo = rowNo, colsNo = mobile_errorInfo)
                # 在测试步骤sheet中，写入异常截图路径
                self.excelObj.writeCell(sheetObj, content = picPath, rowNo = rowNo, colsNo = mobile_errorPic)
            # else:
            #     # 在测试步骤sheet中，清空异常信息单元格
            #     excelObj.writeCell(sheetObj, content = "",rowNo = rowNo, colsNo = testStep_errorInfo)
            #     # 在测试步骤sheet中，清空异常信息单元格
            #     excelObj.writeCell(sheetObj, content = "",rowNo = rowNo, colsNo = testStep_errorPic)
        except Exception as err:
            debug("写excel出错，%s" %traceback.print_exc())

    def executeExcel(self,stepSheet,step,stepDescribe,keyWord,locationType,locatorExpression,operateValue):
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
            returnValue = eval(expressionStr)
            # 在测试执行时间列写入执行时间
            self.excelObj.writeCellCurrentTime(stepSheet, rowNo=step, colsNo=testStep_runTime)
        except Exception as err:
            # 截取异常屏幕图片
            capturePic = capture_screen()
            # 获取详细的异常堆栈信息
            errorInfo = traceback.format_exc()
            # 在测试步骤Sheet中写入失败信息
            self.writeTestResult(stepSheet, step, "caseStep", "faild", errorInfo, capturePic)
            info("步骤“%s”执行失败! 函数执行表达式为：%s" %(stepDescribe,expressionStr))
        else:
            # 在测试步骤Sheet中写入成功信息
            self.writeTestResult(stepSheet, step, "caseStep", "pass")
            info("步骤“%s”执行通过！函数执行表达式为：%s" %(stepDescribe,expressionStr))
            return returnValue

    def selectExcelSheet(self):
        caseStepSheetName = '1'  # 默认类型为场景集合页或普通商品
        #获取执行脚本终端类型，orderTerminal
        # 1:PC端  2:M端  3:小程序端  4:App端  5:APP端跨M  6:PC端跨M  7:PC端跨App端
        TerminalType = self.jsonDict.get('orderTerminal','1')  #如果不存在该字段，默认PC端执行下单操作
        if TerminalType == '1':
            linkTypeName = self.jsonDict.get("linkType",'1')
            if linkTypeName == '1':
                FilePath = PCorderBusinessFilePath
                casePath = os.path.split(FilePath)[0] #获取用例文件路径
                caseStepSheetName = orderBusinessDict.get(self.jsonDict.get('orderBusinessType'))
            else:
                FilePath = PCorderCommodityFilePath
                casePath = os.path.split(FilePath)[0]  #获取用例文件路径
                caseStepSheetName = orderCommodityDict.get(self.jsonDict.get('orderCommodityType'))
        elif TerminalType == '2':
            pass #增加m端读取excel文件代码
        elif TerminalType == '3':
            pass #增加小程序端读取excel文件代码
        elif TerminalType == '4':
            #增加App端读取excel文件代码
            linkTypeName = self.jsonDict.get("linkType", '1')
            if linkTypeName == '1':
                if TerminalexecuteScene == '1':
                    FilePath = WchatorderBusinessFilePath
                    casePath = os.path.split(FilePath)[0] #获取用例文件路径
                else:
                    FilePath = QQorderBusinessFilePath
                    casePath = os.path.split(FilePath)[0]  #获取用例文件路径
                caseStepSheetName = orderBusinessDict.get(self.jsonDict.get('orderBusinessType'))
            else:
                if TerminalexecuteScene == '1':
                    FilePath = WchatorderCommodityFilePath
                    casePath = os.path.split(FilePath)[0] #获取用例文件路径
                else:
                    FilePath = QQorderCommodityFilePath
                    casePath = os.path.split(FilePath)[0]  # 获取用例文件路径
                caseStepSheetName = orderCommodityDict.get(self.jsonDict.get('orderCommodityType'))
        else:
            pass #后续增加跨屏操作
        self.excelObj.loadWorkBook(FilePath)
        return caseStepSheetName,casePath

    def PCExecuteTest(self):
        caseStepSheetName,_,_ = self.selectExcelSheet()
        #定义最终订单号结果
        returnValue = None
        try:
            # 根据用例步骤名获取步骤sheet对象
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
                returnValue = self.executeExcel(*args)
        except Exception as err:
            # 打印详细的异常堆栈信息
            debug(traceback.print_exc())
        finally:
            eval("close_browser()")
            return returnValue

    def selectMobileTerminal(self):
        #通过前端入参选择要下单的终端设备
        # "orderplatform": "android","bitType": "32",'manufacturer':'huawei'
        #预设一个终端设备列表，存储到excel文件中，根据条件进行匹配，或者指定sn号进行选择终端测试机

        try:
            initAllDevice()  #初始化当前连接的所有终端设备
            sn = self.getTerminalSN(self.jsonDict)  #获取指定条件的终端设备sn号
            if not checkDevice(sn):
                getDeviceWithSn(sn)
            return sn
        except Exception as err:
            raise err

    def getTerminalSN(self,**kargs):
        #从提供的设备列表中选择对应的移动终端
        if TerminalSn is not None:
            return TerminalSn
        terminalList = [] #用于存放匹配的设备列表
        terminalObject = ParseExcel()
        print(TerminalFilePath)
        terminalObject.loadWorkBook(TerminalFilePath)
        # 根据用例步骤名获取步骤sheet对象
        stepSheet = terminalObject.getSheetByName('Terminal')
        # 获取步骤sheet中步骤数
        stepNum = terminalObject.getRowsNumber(stepSheet)
        #获取前端入参
        orderPlatform = kargs.get('orderplatform', 'android')  # 获取终端系统类型
        bitType = kargs.get('bitType', '32')  # 获取终端设备位数
        manufacturer = kargs.get('manufacturer', 'huawei')  # 获取终端厂商名称
        for step in range(2, stepNum + 1):
            stepRow = terminalObject.getRow(stepSheet, step)
            terminalSN = stepRow[terminal_ser - 1].value
            terminalPlatform = stepRow[terminal_platform - 1].value
            terminalBittype = str(stepRow[terminal_bittype - 1].value)
            terminalManufacturer = stepRow[terminal_manufacturer - 1].value
            terminalIsonline = stepRow[terminal_isonline - 1].value
            if terminalPlatform ==  orderPlatform and terminalBittype == bitType:
                if terminalSN and terminalIsonline == 'Y':
                    terminalList.append(terminalSN)
        return None if len(terminalList) == 0 else terminalList[random.randint(0,len(terminalList)-1)]

    def selectAppInit(self):
        #连接设备并启动指定app环境
        sn = self.selectMobileTerminal()  # 选择连接终端设备
        poco = generatePoco(sn)
        if TerminalexecuteScene == '1':
            start_app('com.tencent.mm')
        elif TerminalexecuteScene == '2':
            start_app('com.tencent.mobileqq')
            poco("com.tencent.mobileqq:id/et_search_keyword").click()
            poco("com.tencent.mobileqq:id/et_search_keyword").set_text('我的电脑')
        else:
            pass  # 启动其他应用程序
        return poco

    def ExecuteTest(self):
        #执行指定excel表单中的内容
        caseStepSheetName,casePath = self.selectExcelSheet()
        poco = self.selectAppInit()
        try:
            # 根据用例步骤名获取步骤sheet对象
            print('开始<%s>场景的测试...' % caseStepSheetName)
            stepSheet = self.excelObj.getSheetByName(caseStepSheetName)
            # 获取步骤sheet中步骤数
            stepNum = self.excelObj.getRowsNumber(stepSheet)
            for step in range(2, stepNum + 1):
                stepRow = self.excelObj.getRow(stepSheet, step)
                #获取excel表单中每一行单元格的数据
                stepDescribe = stepRow[testStep_testStepDescribe - 1].value
                keyWord = stepRow[mobile_keyWords - 1].value
                picValue = stepRow[mobile_picPath-1].value
                threshold = stepRow[mobile_threshold-1].value
                target_pos = stepRow[mobile_target_pos-1].value
                rgb = stepRow[mobile_rgb-1].value
                expressionStr = ""
                temp = ""
                # 构造需要执行的python语句，
                # 对应的是AppAction.py文件中的终端动作函数调用的字符串表示
                if isinstance(picValue,int):
                    picValue = str(picValue)
                if picValue and picValue.endswith('.png'):
                    picValue = os.path.join(casePath, picValue)
                if threshold is None and target_pos is None and rgb is None:
                    if picValue and picValue.endswith('.png'):
                        temp = "(Template(r'" + picValue + "'))"
                    else:
                        temp = "'"+picValue+"'"
                elif threshold and target_pos is None and rgb is None:
                    temp = "Template(r'" + picValue + "', threshold=" + str(threshold) + ")"
                elif threshold is None and target_pos and rgb is None:
                    temp = "Template(r'" + picValue + "', target_pos=" + str(target_pos) + ")"
                elif threshold is None and target_pos is None and rgb:
                    temp = "Template(r'" + picValue + "', rgb=" + rgb + ")"
                elif threshold and target_pos and rgb is None:
                    temp = "Template('r" + picValue + "', threshold=" + str(threshold) + ", target_pos=" + str(target_pos) + ")"
                elif threshold and target_pos is None and rgb:
                    temp = "Template(r'" + picValue + "', threshold=" + str(threshold) + ", rgb=" + rgb + ")"
                elif threshold is None and target_pos and rgb:
                    temp = "Template(r'" + picValue + "', target_pos=" + str(target_pos) + ", rgb=" + rgb + ")"
                elif threshold and target_pos and rgb:
                    temp = "Template(r'" + picValue + "', threshold=" + str(threshold) + ", target_pos=" + str(target_pos) + ", rgb=" + rgb + ")"
                expressionStr = keyWord.strip() + "(" + temp + ")"
                #执行表达式
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
                    self.writeTestResult(stepSheet, step, "caseStep", "faild", errorInfo, capturePic,secen='mobile')
                    info("步骤“%s”执行失败！函数执行表达式为：%s" %(stepDescribe,expressionStr))
                else:
                    # 在测试步骤Sheet中写入成功信息
                    self.writeTestResult(stepSheet, step, "caseStep", "pass",secen='mobile')
                    # 记录syslog信息
                    info("步骤“%s”执行通过！函数执行表达式为：%s" %(stepDescribe,expressionStr))
        except Exception as err:
            # 打印详细的异常堆栈信息
            debug(traceback.print_exc())
        finally:
            return self.getOrderId(poco)

    def getOrderId(self,poco):
        #获取订单号
        orderId = None
        if self.jsonDict.get('orderTerminal') == '4':
            time.sleep(5)
            orderId = poco("com.jd.lib.ordercenter:id/atm").get_text()
        return orderId

if __name__ == '__main__':
    runScriptJson = {"linkType": "2", "promotionLinkType": "1", "shopType": "1",
                     "orderTerminal": "1", "operationType": "1", "builtInType": "sdk",
                     "desType": "getcopon", "sdkType": "unionSdk", "orderplatform": "android",
                     "bitType": "32", "orderBusinessType": "2", "orderCommodityType": "4"}
    # PCExecuteTest(runScriptJson)
    es = executeScript(runScriptJson)
    print(es.getTerminalSN())
from config.VarConfig import *
from action.AppAction import *
from util.ParseExcel import ParseExcel
from testScripts.ExecuteTest import executeScriptWithPC,executeScriptWithMobile

class OrderTerminalFactory(object):
    def __init__(self,runScriptJson):
        self.jsonDict = runScriptJson

    def selectTerminal(self):
        # 选择下单终端：orderTerminal
        # 1:PC端  2:M端  3:小程序端  4:App端  5:APP端跨M  6:PC端跨M 7:PC端跨App端
        execS = executeScript(runScriptJson)
        orderTerminalDict = {'1': 'PC端',
                             '2': 'M端',
                             '3': '小程序端',
                             '4': 'App端',
                             '5': 'APP端跨M',
                             '6': 'PC端跨M',
                             '7': 'PC端跨App端'}
        if not isinstance(runScriptJson,dict):
            return None
        TerminalType = runScriptJson.get('orderTerminal')
        return orderTerminalDict.get(TerminalType)()

    def selectExcelSheet(self):
        caseStepSheetName = '1'  # 默认类型为场景集合页或普通商品
        #获取执行脚本终端类型，orderTerminal
        # 1:PC端  2:M端  3:小程序端  4:App端  5:APP端跨M  6:PC端跨M  7:PC端跨App端
        TerminalType = self.jsonDict.get('orderTerminal','1')  #如果不存在该字段，默认PC端执行下单操作
        if TerminalType == '1':
            linkTypeName = self.jsonDict.get("linkType",'1')
            if linkTypeName == '1':
                FilePath = PCorderBusinessFilePath
                caseStepSheetName = orderBusinessDict.get(self.jsonDict.get('orderBusinessType'))
            else:
                FilePath = PCorderCommodityFilePath
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
                else:
                    FilePath = QQorderBusinessFilePath
                caseStepSheetName = orderBusinessDict.get(self.jsonDict.get('orderBusinessType'))
            else:
                if TerminalexecuteScene == '1':
                    FilePath = WchatorderCommodityFilePath
                else:
                    FilePath = QQorderCommodityFilePath
                caseStepSheetName = orderCommodityDict.get(self.jsonDict.get('orderCommodityType'))
        else:
            pass #后续增加跨屏操作
        return FilePath,caseStepSheetName


class TerminalOperate(object):
    #针对移动终端的操作
    def __init__(self,jsonDict):
        self.jsonDict = jsonDict

    def selectMobileTerminal(self):
        # 通过前端入参选择要下单的终端设备
        # "orderplatform": "android","bitType": "32",'manufacturer':'huawei'
        # 预设一个终端设备列表，存储到excel文件中，根据条件进行匹配，或者指定sn号进行选择终端测试机

        try:
            initAllDevice()  # 初始化当前连接的所有终端设备
            sn = self.getTerminalSN()  # 获取指定条件的终端设备sn号
            if not checkDevice(sn):
                getDeviceWithSn(sn)
            return sn
        except Exception as err:
            raise err

    def getTerminalSN(self):
        # 从提供的设备列表中选择对应的移动终端
        if TerminalSn is not None:
            return TerminalSn
        terminalList = []  # 用于存放匹配的设备列表
        terminalObject = ParseExcel()
        print(TerminalFilePath)
        terminalObject.loadWorkBook(TerminalFilePath)
        # 根据用例步骤名获取步骤sheet对象
        stepSheet = terminalObject.getSheetByName('Terminal')
        # 获取步骤sheet中步骤数
        stepNum = terminalObject.getRowsNumber(stepSheet)
        # 获取前端入参
        orderPlatform = self.jsonDict.get('orderplatform', 'android')  # 获取终端系统类型
        bitType = self.jsonDict.get('bitType', '32')  # 获取终端设备位数
        manufacturer = self.jsonDict.get('manufacturer', 'huawei')  # 获取终端厂商名称
        for step in range(2, stepNum + 1):
            stepRow = terminalObject.getRow(stepSheet, step)
            terminalSN = stepRow[terminal_ser - 1].value
            terminalPlatform = stepRow[terminal_platform - 1].value
            terminalBittype = str(stepRow[terminal_bittype - 1].value)
            terminalManufacturer = stepRow[terminal_manufacturer - 1].value
            terminalIsonline = stepRow[terminal_isonline - 1].value
            if terminalPlatform == orderPlatform and terminalBittype == bitType:
                if terminalSN and terminalIsonline == 'Y':
                    terminalList.append(terminalSN)
        return None if len(terminalList) == 0 else terminalList[random.randint(0, len(terminalList) - 1)]

    def selectApp(self,appName):
        # 连接设备并启动指定app环境，返回poco实例对象
        sn = self.selectMobileTerminal()  # 选择连接终端设备
        poco = generatePoco(sn)
        if appName.lower() in appDict:
            start_app(appDict[appName.lower()])
        return poco
        # elif TerminalexecuteScene == '2':
        #     start_app('com.tencent.mobileqq')
        #     poco("com.tencent.mobileqq:id/et_search_keyword").click()
        #     poco("com.tencent.mobileqq:id/et_search_keyword").set_text('我的电脑')
        # else:
        #     pass  # 启动其他应用程序
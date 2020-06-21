from testScripts.ExecuteTest import PCExecuteTest
from config.VarConfig import *

def selectTerminalFactory(runScriptJson):
    # 选择下单终端：orderTerminal    1:PC端  2:M端  3:小程序端  4:App端  5:APP端跨M  6:PC端跨M 7:PC端跨App端
    orderTerminalDict = {'1': PCExecuteTest, '2': 'M端', '3': '小程序端', '4': 'App端', '5': 'APP端跨M', '6': 'PC端跨M', '7': 'PC端跨App端'}
    if not isinstance(runScriptJson,dict):
        return None
    TerminalType = runScriptJson.get('orderTerminal')
    return orderTerminalDict.get(TerminalType)



import os

ChromeDriverFilePath = "c:\\chromedriver"

# 当前文件所在目录的父目录的绝对路径
parentDirPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 异常截图存放目录绝对路径
screenPicturesDir = parentDirPath + "\\exceptionpictures\\"

# 测试数据文件存放绝对路径
PCorderBusinessFilePath = parentDirPath + "\\testData\\pcData\\orderBusinessAction.xlsx"
QQorderBusinessFilePath = parentDirPath + "\\testData\\mobileData\\qqScene\\orderBusinessAction.xlsx"
WchatorderBusinessFilePath = parentDirPath + "\\testData\\mobileData\\wchatScene\\orderBusinessAction.xlsx"
PCorderCommodityFilePath = parentDirPath + "\\testData\\pcData\\orderCommodityAction.xlsx"
QQorderCommodityFilePath = parentDirPath + "\\testData\\mobileData\\qqScene\\orderCommodityAction.xlsx"
WchatorderCommodityFilePath = parentDirPath + "\\testData\\mobileData\\wchatScene\\orderCommodityAction.xlsx"

#登录cookie数据文件绝对路径
mcookieFilePath = parentDirPath + "\\config\\cookies.txt"
webcookieFilePath = parentDirPath + "\\config\\webcookies.txt"

# 测试数据文件中，测试用例表中部分列对应的数字序号
testCase_runTime = 6
testCase_testResult = 7

# web用例步骤表中，部分列对应的数字序号
testStep_testStepDescribe = 2
testStep_keyWords = 3
testStep_locationType = 4
testStep_locatorExpression = 5
testStep_operateValue = 6
testStep_runTime = 7
testStep_testResult = 8
testStep_errorInfo = 9
testStep_errorPic = 10

#要运行的终端序列号
TerminalSn = None
TerminalexecuteScene = '1' #呼起app的环境，1表示从微信环境，2表示从QQ环境，3表示从浏览器环境
TerminalFilePath = parentDirPath + "\\config\\mobileDevices.xlsx"
terminal_ser = 2
terminal_platform = 3
terminal_bittype = 4
terminal_manufacturer = 5
terminal_isonline = 6

#业务或链接字典
orderBusinessDict = {'1':'场景集合页','2':'推荐集合页','3':'h5首购','4':'红人小店','5':'京享礼金',
                     '6':'站内达人文章','7':'京享红包','8':'红包密令','9':'奖励活动'}
orderCommodityDict = {'1':'普通商品','2':'秒杀商品','3':'拼购商品','4':'二合一商品','5':'sem推广_普通商品',
                      '6':'店铺商品','7':'活动商品','8':'其他商品'}

#移动终端用例步骤中，部分列对应的数字序号
mobile_testStepDescribe = 2
mobile_keyWords = 3
mobile_picPath = 4
mobile_threshold = 5
mobile_target_pos = 6
mobile_rgb = 7
mobile_runTime=8
mobile_testResult = 9
mobile_errorInfo = 10
mobile_errorPic = 11
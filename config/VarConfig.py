import os

ChromeDriverFilePath = "c:\\chromedriver"

# 当前文件所在目录的父目录的绝对路径
parentDirPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 异常截图存放目录绝对路径
screenPicturesDir = parentDirPath + "\\exceptionpictures\\"

# 测试数据文件存放绝对路径
dataFilePath = parentDirPath + "\\testData\\orderAction.xlsx"
orderBusinessFilePath = parentDirPath + "\\testData\\orderBusinessAction.xlsx"
orderCommodityFilePath = parentDirPath + "\\testData\\orderCommodityAction.xlsx"

#登录cookie数据文件绝对路径
mcookieFilePath = parentDirPath + "\\config\\cookies.txt"
webcookieFilePath = parentDirPath + "\\config\\webcookies.txt"

# 测试数据文件中，测试用例表中部分列对应的数字序号
testCase_testCaseName = 2
testCase_testStepSheetName = 4
testCase_isExecute = 5
testCase_runTime = 6
testCase_testResult = 7

# 用例步骤表中，部分列对应的数字序号
testStep_testStepDescribe = 2
testStep_keyWords = 3
testStep_locationType = 4
testStep_locatorExpression = 5
testStep_operateValue = 6
testStep_runTime = 7
testStep_testResult = 8
testStep_errorInfo = 9
testStep_errorPic = 10

#业务或链接字典
orderBusinessDict = {'1':'场景集合页','2':'推荐集合页','3':'h5首购','4':'红人小店','5':'京享礼金',
                     '6':'站内达人文章','7':'京享红包','8':'红包密令','9':'奖励活动'}
orderCommodityDict = {'1':'普通商品','2':'秒杀商品','3':'拼购商品','4':'二合一商品','5':'sem推广_普通商品',
                      '6':'店铺商品','7':'活动商品','8':'其他商品'}
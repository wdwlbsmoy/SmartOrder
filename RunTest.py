from testScripts.TerminalSelect import selectTerminalFactory

if __name__ == '__main__':
    #选择商品方式：linkType   1:业务方式  2:链接方式
    #选择推广链接：promotionLinkType   1:线上推广链接  2:手动录入链接
    #选择同店跨店：shopType    1:同屏同店  2:同屏跨店  3：跨屏同店  4：跨屏跨店
    #选择下单终端：orderTerminal    1:PC端  2:M端  3:小程序端  4:App端  5:APP端跨M  6:PC端跨M 7:PC端跨App端
    #选择下单场景：
    # 站内站外操作类型：operationType    1:站内扫一扫  2:站外呼起jdapp  3:站外呼起快应用  4:站外落地页呼起  5:站外呼起走托底逻辑
    #sdk或者唤醒：builtInTye    sdk:SDK  awaken:唤醒
    #des类型：desType    m:m  getcopon:getcopon
    #sdk类型：sdkType    unionSdk:联盟sdk  keplerSdk:开普勒sdk
    #手机类型：orderplatform    ios:ios  android:android  ipad:ipad
    #手机位数：bitType    32:32位  64:64位
    #选择厂商：manufacturer
    #orderBusinessType    1:场景集合页  2:推荐集合页  3:h5首购  4:红人小店  5:京享礼金  6:站内达人文章  7:京享红包  8:红包密令  9:奖励活动
    #orderCommodityType   1:普通商品  2:秒杀商品  3:拼购商品  4:二合一商品  5:sem推广_普通商品  6:店铺商品  7:活动商品  8:其他商品
    runScriptJson = {"linkType":"2","promotionLinkType":"1","shopType":"1",
                     "orderTerminal":"1","operationType":"1","builtInType":"sdk",
                     "desType":"getcopon","sdkType":"unionSdk","orderplatform":"android",
                     "bitType":"32","orderBusinessType":"2","orderCommodityType":"4"}
    orderId = selectTerminalFactory(runScriptJson)
    print("订单号为：%s" %orderId)


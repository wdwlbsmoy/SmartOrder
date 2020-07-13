from action.AppAction import *

#获取当前连接的所有终端设备，并打印序列号
# initAllDevice()

def delOrder(poco):
    #清理账号下待删除的订单
    while True:
        obj = poco("com.jd.lib.ordercenter:id/akb").child("android.widget.FrameLayout").child(
            "android.widget.LinearLayout").child("android.widget.FrameLayout").offspring(
            "com.jd.lib.ordercenter:id/zr").child("android.widget.RelativeLayout").offspring(
            "com.jd.lib.ordercenter:id/ahz").offspring("android.support.v7.widget.RecyclerView").child(
            "com.jd.lib.ordercenter:id/alb")[0].offspring("com.jd.lib.ordercenter:id/alh")
        if obj:
            obj.click()
            poco("com.jingdong.app.mall:id/bq").click()

def delWaitOrder(poco):
    #删除第一个待付款的订单
    poco(text="等待付款").click()
    name = poco("com.jd.lib.ordercenter:id/atm").get_text()
    print(name)
    poco(text="取消订单").click()
    poco("android.widget.FrameLayout").offspring("android:id/content").offspring("com.jd.lib.ordercenter:id/aqb").child(
        "android.widget.LinearLayout")[1].offspring("com.jd.lib.ordercenter:id/t5").click()
    poco("com.jd.lib.ordercenter:id/aq9").click()
    poco("com.jd.lib.ordercenter:id/aks").click()
    poco("com.jingdong.app.mall:id/bq").click()

if __name__ == '__main__':
    from poco.drivers.android.uiautomation import AndroidUiautomationPoco
    poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
    delWaitOrder(poco)
    delOrder(poco)
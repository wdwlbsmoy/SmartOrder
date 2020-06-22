import time
from airtest.core.android.adb import ADB
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtest.core.android import Android

adb = None
poco = None

'''airtest图像识别封装函数列表'''

def initAllDevice():
    #初始化连接当前所有的设备
    global adb
    allDevices = adb.devices()
    try:
        for sn,dev in allDevices:
            connect_device('android:///'+sn)
    except Exception as err:
        raise err
    else:
        print(G.DEVICE_LIST)

def getDeviceWithSn(sn=None):
    #默认sn为None，不指定设备序列号时，默认使用第一个设备
    try:
        if sn is None:
            set_current(0)
            adb.serialno = G.DEVICE.serialno
        else:
            for index in range(len(G.DEVICE_LIST)):
                if G.DEVICE_LIST[index].serialno == sn:
                    set_current(index)
                    break
            else:
                set_current(0)
            adb.serialno = G.DEVICE.serialno
    except Exception as err:
        raise err

def startApp(package_name):
    global adb
    try:
        wake() #唤醒当前设备屏幕
        stopApp(package_name)  #关闭当前设备已经启动的app应用
        time.sleep(1)
        start_app(package_name) #启动指定名称的app应用
    except Exception as err:
        raise err

def stopApp(package_name):
    global adb
    if package_name not in adb.list_app():
        raise Exception('当前设备没有该应用')
    stop_app(package_name)  # 关闭当前设备已经启动的app应用

def installApp(package_name):
    #安装指定名称的app应用或者删除已有的版本，重新安装该应用
    global adb
    try:
        uninstallApp(package_name)
        install(package_name)
    except Exception as err:
        raise err

def uninstallApp(package_name):
    #删除指定名称的app应用
    global adb
    home()  # 返回到设备主页面
    if package_name in adb.list_app():
        uninstall(package_name)

def executeCmd(cmd):
    #在目标设备上执行指定命令行cmd
    shell(cmd)

def snapShot(filename=None,msg=""):
    #截取设备当前界面截图，并返回截图路径
    return snapshot(filename=filename, msg=msg, quality=ST.SNAPSHOT_QUALITY)

def touchTarget(v,times=1,**kwargs):
    #触摸点击设备屏幕中指定位置（Template instance or absolute coordinates (x, y)）,返回坐标位置
    return touch(v, times=1, **kwargs)

def doubleClick(v):
    #对设备屏幕中的指定位置进行双击（Template instance or absolute coordinates (x, y)），并返回坐标位置
    return double_click(v)

def swipeTarget(v1,v2=None,vector=None,**kwargs):
    #在屏幕v1位置滑动到v2位置，并返回初始和结束位置的坐标
    return swipe(v1, v2=v2, vector=vector, **kwargs)

def pinchTarget(inOrOut='in', center=None, percent=0.5):
    #执行搓动放大或缩小操作，默认为缩小，搓动中心为当前屏幕中心
    pinch(in_or_out=inOrOut, center=center, percent=percent)

def keyBoardInput(keyname,**kwargs):
    #执行键盘输入操作
    keyevent(keyname, **kwargs)

def textInput(text,enter=True,**kwargs):
    #对屏幕控件输入文本内容
    text(text, enter=True, **kwargs)

def waitAndTouch(v, timeout=None, interval=0.5, intervalfunc=None,times=1,**kwargs):
    #等待目标出现并触摸点击，默认超时时间为20秒，每隔0.5秒查看一次
    if wait(v, timeout=timeout, interval=interval, intervalfunc=intervalfunc):
        touchTarget(v, times=times, **kwargs)

def existsAndTouch(v,times=1,**kwargs):
    #判断目标存在并触摸点击
    if exists(v):
        touchTarget(v,times=times,**kwargs)

def findAllTarget(v):
    #从当前屏幕中找出所有匹配的目标对象,返回坐标列表
    return find_all(v)

'''poco封装函数列表'''

def generatePoco(sn=None,use_airtest_input=True, screenshot_each_action=False):
    if sn is None:
        dev = None
    else:
        dev = Android(sn)  #指定sn选择目标设备
    poco = AndroidUiautomationPoco(device=dev,use_airtest_input=use_airtest_input,
                                   screenshot_each_action=screenshot_each_action)
    return poco

if __name__ == '__main__':
    adb = ADB()
    initAllDevice()
    getDeviceWithSn()
    print('com.tencent.mobileqq' in  adb.list_app())

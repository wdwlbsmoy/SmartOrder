from selenium.webdriver.support.ui import WebDriverWait

def highLightElement(driver,element):
    # 封装的高亮显示页面元素的方法
    driver.execute_script("arguments[0].setAttribute('style',\
    arguments[1]);", element,"background:green; border:2px solid red;")

# 获取单个页面元素对象
def getElement(driver, locationType, locatorExpression,times=None):
    if times is None:
        count = 0  # 定义初始计数次数，如果超过3次，则认为失败
        waitTime = 30
    else:
        count = 3
        waitTime = 10
    while True:
        try:
            element = WebDriverWait(driver, waitTime).until\
                (lambda x: x.find_element(by=locationType, value = locatorExpression))
            # highLightElement(driver, element)
            return element
        except Exception as e:
            if count < 3:
                count += 1
                continue
            raise e

# 获取多个相同页面元素对象，以list返回
def getElements(driver, locationType, locatorExpression,times=None):
    if times is None:
        count = 0 #定义初始计数次数，如果超过3次，则认为失败
        waitTime = 30
    else:
        count = 3
        waitTime = 10
    while True:
        try:
            elements = WebDriverWait(driver, waitTime).until\
                (lambda x:x.find_elements(by=locationType, value = locatorExpression))
            return elements
        except Exception as err:
            if count < 3:
                count += 1
                continue
            raise err

if __name__ == '__main__':
    from selenium import webdriver
    # 进行单元测试
    driver = webdriver.Chrome(executable_path="c:\\chromedriver.exe")
    driver.get("http://www.baidu.com")
    searchBox = getElement(driver, "id", "kw")
    # 打印页面对象的标签名
    print(searchBox.tag_name)
    aList = getElements(driver, "tag name", "a")
    print(len(aList))
    driver.quit()

from selenium import webdriver
import os,sys,time
import requests
# from config.VarConfig import cookieFilePath

def setCookie(driver,file,*args):
    with open(file, 'r') as fp:
        for line in fp:
            cooDict = eval(line.strip())
            if 'expiry' in cooDict:
                del cooDict['expiry']
            driver.add_cookie(cooDict)

def getTwoCookies():
    brower = webdriver.Chrome(executable_path="c:\\chromedriver.exe")
    brower.get("https://union.jd.com/")
    # setCookie(brower)
    # brower.find_element_by_xpath('//*[@id="app"]//div[@class="btn-area"]/div').click()
    time.sleep(5)
    for item in brower.get_cookies():
        print(item)
    print("=====================================")
    os.system('pause')
    time.sleep(2)
    for item in brower.get_cookies():
        print(item)

if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path="c:\\chromedriver.exe")
    driver.maximize_window()
    driver.get("https://union.jd.com/")
    file = r'D:\John\work\airtestLearning\need.txt'
    setCookie(driver,file)
    driver.get("https://union.jd.com/")
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="app"]//a[@href="/overview"]').click()

    url = 'https://union.jd.com/api/goods/search'
    for index in range(1,4):
        rr = driver.get_cookies()
        print(rr)
        cookieValue = ''
        for item in rr:
            cookieValue += item['name'] + '=' + item['value']
        headers = {
            "Content-Type": "application/json",
            "Cookie": cookieValue,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            "referer": "https://union.jd.com/proManager/index?pageNo="+str(index)
        }
        formValue = '{"pageNo":'+str(index)+',"pageSize":60,"searchUUID":"97995e9c26d0415c9372713218041f42","data":{"bonusIds":null,"categoryId":null,"cat2Id":null,"cat3Id":null,"deliveryType":0,"fromCommissionRatio":null,"toCommissionRatio":null,"fromPrice":null,"toPrice":null,"hasCoupon":0,"isHot":null,"isPinGou":0,"isZY":0,"isCare":0,"lock":0,"orientationFlag":0,"sort":null,"sortName":null,"key":"","searchType":"st3","keywordType":"kt0"}}'
        print(formValue)
        print(headers)
        time.sleep(2)
        res = requests.post(url,data=formValue,headers=headers)
        print(res)
        print(res.json())
        print('==============')
        # if res.status_code == 200:
        #     for ii in res.json()['data']['unionGoods']:
        #         print(ii)
        #     print('================')
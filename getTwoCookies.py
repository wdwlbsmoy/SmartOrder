from selenium import webdriver
import os,sys,time
from config.VarConfig import cookieFilePath

def setCookie(driver,*args):
    with open(cookieFilePath, 'r') as fp:
        for line in fp:
            cooDict = eval(line.strip())
            del cooDict['expiry']
            driver.add_cookie(cooDict)

brower = webdriver.Chrome(executable_path="c:\\chromedriver.exe")
brower.get("https://u.jd.com/OQwo2t")
setCookie(brower)
brower.find_element_by_xpath('//*[@id="app"]//div[@class="btn-area"]/div').click()
time.sleep(5)
for item in brower.get_cookies():
    print(item)
print("=====================================")
os.system('pause')
time.sleep(2)
for item in brower.get_cookies():
    print(item)
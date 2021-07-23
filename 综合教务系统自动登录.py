from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime

student_no='PB20000000' #学号
ustcmis_password='******' #密码
req_timeout=10

def central_auth_login(driver):
    driver.implicitly_wait(req_timeout)
    driver.get('https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fjw.ustc.edu.cn%2Fucas-sso%2Flogin')
    driver.find_element_by_name("username").send_keys(student_no)
    driver.find_element_by_name("password").send_keys(ustcmis_password)
    driver.find_element_by_name("button").click()
    print('已登录！')

driver = webdriver.Chrome()
central_auth_login(driver)
select(driver)
driver.close()

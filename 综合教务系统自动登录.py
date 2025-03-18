from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import datetime

student_no='PB2' #学号
ustcmis_password='1' #密码
req_timeout=10

def central_auth_login(driver):
    driver.implicitly_wait(req_timeout)
    driver.get('https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fjw.ustc.edu.cn%2Fucas-sso%2Flogin')
    driver.find_element(By.NAME,"username").send_keys(student_no)
    driver.find_element(By.NAME,"password").send_keys(ustcmis_password)
    driver.find_element(By.NAME,"button").click()
    print('已登录！')

driver = webdriver.Edge()
central_auth_login(driver)

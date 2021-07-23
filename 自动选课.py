from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime

student_no='PB20000000' #学号
ustcmis_password='******' #密码
req_timeout=10
sel_time=12 #选课开放时间（时）
courses=['011040.01'] #课程号列表

def central_auth_login(driver):
    driver.implicitly_wait(req_timeout)
    driver.get('https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fjw.ustc.edu.cn%2Fucas-sso%2Flogin')
    driver.find_element_by_name("username").send_keys(student_no)
    driver.find_element_by_name("password").send_keys(ustcmis_password)
    driver.find_element_by_name("button").click()
    print('已登录！')

def select(driver):
    driver.find_element_by_css_selector("[class='primaryLi noSubMenus']").click()
    driver.switch_to_frame('e-home-iframe-1')
    addr=driver.find_element_by_link_text('进入选课').get_attribute('href')
    driver.get(addr)
    driver.find_element_by_css_selector("[class='btn btn-default close-modal bulletin-prompt']").click()
    driver.find_element_by_link_text('全部课程').click()
    for course in courses:
        driver.find_element_by_id('global_filter').clear()
        driver.find_element_by_id('global_filter').send_keys(course)
        driver.find_element_by_id('global_filter').send_keys(Keys.ENTER)
        driver.find_element_by_css_selector("[class='btn btn-primary course-select']").click()
        time.sleep(3)
        driver.find_element_by_css_selector("[class='btn btn-default close-modal']").click()
        print(course,'已经选！')

while True:
    now_time = datetime.datetime.now().hour
    if now_time>=sel_time:
        break

driver = webdriver.Chrome()
central_auth_login(driver)
select(driver)
driver.close()

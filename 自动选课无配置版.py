from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import datetime

student_no=input('输入学号：') #学号
ustcmis_password=input('输入密码：') #密码
req_timeout=20 #隐式等待时限（秒）
sel_time=int(input('输入几点开始选课，24小时制：')) #选课开放时间（时）
tmp=""
courses=[] #课程号列表
change_from=[] #要换的课程号
change_to=[] #对应的目标课程号
while tmp!=" ":
    tmp=input('输入要选的课程号，输完按回车，输入空格进入换班环节：')
    if tmp!=" ":
        courses.append(tmp)
        print('课程',tmp,'已被录入。')
tmp=""
while tmp!=" ":
    tmp=input('输入要换的课程号，输空格开始运行脚本：')
    if tmp!=" ":
        change_from.append(tmp)
        tmp=input('输入目标班的课程号：')
        change_to.append(tmp)
        print('本程序将会尝试将',change_from[-1],'换为',tmp,'。')

driver = webdriver.Chrome()
driver.implicitly_wait(req_timeout)

def central_auth_login(driver): #登录教务系统
    driver.get('https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fjw.ustc.edu.cn%2Fucas-sso%2Flogin')
    driver.find_element_by_name("username").send_keys(student_no)
    driver.find_element_by_name("password").send_keys(ustcmis_password)
    driver.find_element_by_name("button").click()
    print('已登录')

def select(driver): #选课、换班，先换班后选课
    driver.find_element_by_css_selector("[class='primaryLi noSubMenus']").click()
    print('正在寻找子框架，请勿在页面内操作！')
    driver.switch_to_frame('e-home-iframe-1')
    addr=driver.find_element_by_link_text('进入选课').get_attribute('href')
    driver.get(addr)
    driver.find_element_by_css_selector("[class='btn btn-default close-modal bulletin-prompt']").click() #点击提示页面的确定按钮，如果已经选择不再提示，则去掉这一行代码以及后面相同的代码
    driver.find_element_by_link_text('全部课程').click()
    print('等待选课开始...')
    while True:
        now_time = datetime.datetime.now().hour
        if now_time>=sel_time:
            break
    
    print('已进入选课！')
    if len(change_from)!=0:
        print('正在尝试换班...')
    for i in range(0,len(change_from)): #换班
        driver.find_element_by_id('global_filter').clear()
        driver.find_element_by_id('global_filter').send_keys(change_from[i])
        driver.find_element_by_id('global_filter').send_keys(Keys.ENTER) #开始搜索要换班的课程
        driver.find_element_by_xpath("//div[@id='all-lessons']//button[@class='btn btn-primary dropdown-toggle']").click() #点击换班按钮
        driver.find_element_by_link_text('单课换班').click()
        if driver.title!='请选择新课堂':
            while driver.title!='请选择新课堂':
                driver.get(addr)
                driver.find_element_by_css_selector("[class='btn btn-default close-modal bulletin-prompt']").click() #点击提示页面的确定按钮，如果已经选择不再提示，则去掉这一行代码以及后面相同的代码
                driver.find_element_by_link_text('全部课程').click()
                driver.find_element_by_id('global_filter').clear()
                driver.find_element_by_id('global_filter').send_keys(change_from[i])
                driver.find_element_by_id('global_filter').send_keys(Keys.ENTER) #开始搜索要换班的课程
                driver.find_element_by_xpath("//div[@id='all-lessons']//button[@class='btn btn-primary dropdown-toggle']").click() #点击换班按钮
        driver.find_element_by_id('lessonCode-filter').clear() #清空输入框
        driver.find_element_by_id('lessonCode-filter').send_keys(change_to[i]) #输入要换到的课程号
        driver.find_element_by_id('filter-btn').click()
        driver.find_element_by_xpath("//tr[not(@class)]//button[@class='btn btn-primary change-class']").click()
        if driver.title=='本科生分层换班申请表': #处理申请表
            driver.find_element_by_id('applyReason').send_keys('比较喜欢这位老师的上课风格')
            driver.find_element_by_id('save-btn').click()
        else:
            driver.find_element_by_css_selector("[data-bb-handler='ok']").click()
        driver.get(addr)
        driver.find_element_by_css_selector("[class='btn btn-default close-modal bulletin-prompt']").click()
        driver.find_element_by_link_text('全部课程').click()
        print('已经尝试把',change_from[i],'换为',change_to[i])
    if(len(change_from)!=0):
        print('换班结束！')
        
    if(len(courses)!=0):
        print('正在尝试选课...')
    for course in courses: #选课
        driver.find_element_by_id('global_filter').clear()
        driver.find_element_by_id('global_filter').send_keys(course)
        driver.find_element_by_id('global_filter').send_keys(Keys.ENTER)
        driver.find_element_by_css_selector("[class='btn btn-primary course-select']").click()
        driver.find_element_by_css_selector("[class='btn btn-default close-modal']").click()
        print('已经尝试选',course)
    if(len(courses)!=0):
        print('选课结束！')
        
central_auth_login(driver)
select(driver)
driver.close()

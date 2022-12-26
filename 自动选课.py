from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import datetime

student_no='PB21111706' #学号
ustcmis_password='159' #密码
req_timeout=20 #隐式等待时限（秒）
sel_time=12 #选课开放时间（时）
courses=[] #课程号列表
change_from=['PHYS1010.05'] #要换的课程号
change_to=['PHYS1010.01'] #对应的目标课程号
reason='期望通过这门课的学习，对相关知识形成一个较深刻的认识。知道老师的口碑评价非常好，特别希望能有机会听到老师的课。'

driver = webdriver.Edge()
driver.implicitly_wait(req_timeout)

def central_auth_login(driver): #登录教务系统
    driver.get('https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fjw.ustc.edu.cn%2Fucas-sso%2Flogin')
    driver.find_element(By.NAME,"username").send_keys(student_no)
    driver.find_element(By.NAME,"password").send_keys(ustcmis_password)
    #等待输入验证码
    while True:
        if driver.title=='中国科学技术大学综合教务系统':
            break
    print('已登录')

def select(driver): #选课、换班，先换班后选课
    driver.find_element(By.CSS_SELECTOR,"[class='primaryLi noSubMenus']").click()   #点击选课
    driver.switch_to.frame('e-home-iframe-1')   #切换到选课页面
    addr=driver.find_element(By.LINK_TEXT,'进入选课').get_attribute('href') #获取选课页面的地址
    driver.get(addr)        #进入选课页面
    driver.find_element(By.CSS_SELECTOR,"[class='btn btn-default close-modal bulletin-prompt']").click() #点击提示页面的确定按钮，如果已经选择不再提示，则去掉这一行代码以及后面相同的代码
    driver.find_element(By.LINK_TEXT,'全部课程').click() #点击全部课程
    while True:
        now_time = datetime.datetime.now().hour #获取当前时间
        #print('当前时间：',now_time)
        if now_time>=sel_time:  #如果当前时间大于等于选课开放时间
            break   #跳出循环
    
    for i in range(0,len(change_from)): #换班
        driver.find_element(By.ID,'global_filter').clear()  #清空搜索框
        driver.find_element(By.ID,'global_filter').send_keys(change_from[i])    #输入要换班的课程号
        driver.find_element(By.ID,'global_filter').send_keys(Keys.ENTER) #开始搜索要换班的课程
        driver.find_element(By.XPATH,"//div[@id='all-lessons']//button[@class='btn btn-primary dropdown-toggle']").click() #点击换班按钮
        driver.find_element(By.LINK_TEXT,'单课换班').click()    #点击单课换班
        if driver.title!='请选择新课堂':
            while driver.title!='请选择新课堂':
                driver.get(addr)
                driver.find_element(By.CSS_SELECTOR,"[class='btn btn-default close-modal bulletin-prompt']").click() #点击提示页面的确定按钮，如果已经选择不再提示，则去掉这一行代码以及后面相同的代码
                driver.find_element(By.LINK_TEXT,'全部课程').click()    #点击全部课程
                driver.find_element(By.ID,'global_filter').clear()  #清空搜索框
                driver.find_element(By.ID,'global_filter').send_keys(change_from[i])    #输入要换班的课程号
                driver.find_element(By.ID,'global_filter').send_keys(Keys.ENTER) #开始搜索要换班的课程
                driver.find_element(By.XPATH,"//div[@id='all-lessons']//button[@class='btn btn-primary dropdown-toggle']").click() #点击换班按钮
        driver.find_element(By.ID,'lessonCode-filter').clear() #清空输入框
        driver.find_element(By.ID,'lessonCode-filter').send_keys(change_to[i]) #输入要换到的课程号
        driver.find_element(By.ID,'filter-btn').click() #开始搜索要换到的课程
        driver.find_element(By.XPATH,"//tr[not(@class)]//button[@class='btn btn-primary change-class']").click()    #点击换班按钮
        if driver.title=='本科生分层换班申请表': #处理申请表
            driver.find_element(By.ID,'applyReason').send_keys(reason)  #输入换班原因
            driver.find_element(By.ID,'save-btn').click()   #点击保存按钮
        else:
            driver.find_element(By.CSS_SELECTOR,"[data-bb-handler='ok']").click()   #点击确定按钮
        driver.get(addr)    #返回主页
        driver.find_element(By.CSS_SELECTOR,"[class='btn btn-default close-modal bulletin-prompt']").click()    #点击提示页面的确定按钮，如果已经选择不再提示，则去掉这一行代码以及后面相同的代码
        driver.find_element(By.LINK_TEXT,'全部课程').click()    #点击全部课程
        print('已经尝试把',change_from[i],'换为',change_to[i])  #打印换班信息

    for course in courses: #选课
        driver.find_element(By.ID,'global_filter').clear()  #清空搜索框
        driver.find_element(By.ID,'global_filter').send_keys(course)    #输入要选的课程号
        driver.find_element(By.ID,'global_filter').send_keys(Keys.ENTER)    #开始搜索要选的课程
        driver.find_element(By.CSS_SELECTOR,"[class='btn btn-primary course-select']").click()  #点击选课按钮
        driver.find_element(By.CSS_SELECTOR,"[class='btn btn-default close-modal']").click()    #点击提示页面的确定按钮，如果已经选择不再提示，则去掉这一行代码以及后面相同的代码
        print('已经尝试选！',course)    #打印选课信息

central_auth_login(driver)
select(driver)
#driver.close()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlencode
import time
import os

'''def login_kaggle(url):
    browser = webdriver.Chrome()
    browser.get(url)
    wait = WebDriverWait(browser,100)
    button1 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.site-header-react__user')))
    button1.click()
    button2 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'[href="/account/authenticate/google?isModal=true"]')))
    button2.click()
    input1 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#identifierId')))
    phonenumber='' #输入邮箱或电话号码
    input1.send_keys(phonenumber)
    button3 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#identifierNext')))
    button3.click()
    time.sleep(3)
    input2 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.whsOnd.zHQkBf')))
    password=''  #输入密码
    input2.send_keys(password)
    button4 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.CwaK9')))
    button4.click()
    time.sleep(3)
    return browser'''


def get_train(browser,n,x):    
    '''编写标签列表'''
    label_crime = ['crime']
    #犯罪
    label_CS = ['machine learning', 'deep learning', 'computer science', 'programm', 'programming', 'computers', 'image', 'image data', 'internet software', 'web sites', 'software', 'computing', 'internet']
    #计算机科学
    label_transport = ['transport', 'travel', 'taxi', 'taxi services']
    #交通
    label_economic = ['economic', 'economics', 'finance', 'trade']
    #经济
    label_healthcare = ['health', 'health care', 'biology','healthcare']
    #医疗
    lable_food_and_drink = ['food', 'drink', 'food and drink']
    #饮食
    label_nature = ['energy', 'earth science']
    #自然
    label_sports = ['golf', 'basketball', 'football', 'sports', 'olympic games']
    #运动
    labels_culture = ['literature', 'linguistics', 'writing', 'culture', 'history', 'culture and humanities', 'education']
    #人文
    wait = WebDriverWait(browser,15)
    f = open('urls.txt','r')
    line = f.readline()
    line = line.rstrip('\n')
    line = line.split()
    i = int(line[-1])
    while(i<n):
        line = f.readline()
        if(line.find('page')==0):
            line = line.split()
            i = int(line[-1]) #获得page值，以比较
    print(i)
    line = f.readline()
    while line.rstrip('\n'):
        if(line.find('page')==0):
            line = line.split()
            i = int(line[-1])
            print('==================')
            print(i)  #输出当前运行的页面
            if(i<n+x):
                line = f.readline()
                continue  #仍在范围内，继续循环
            else:
                break #超出范围，跳出循环
        else:
            line = line.rstrip('\n')
            try:
                browser.get(line)
            except:
                pass
            line_ = line
            line = f.readline()
            '''try:
                click1 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.button__anchor-wrapper')))
                click1.click()
                time.sleep(1)
                line =f.readline()
            except:
                file = open('error_urls.txt','a',encoding='utf-8')
                file.write(line+'\n') # 将错误url写入txt'''
        try:
            button = browser.find_elements_by_css_selector('body > main > div > div.site-layout__main-content > div > div > div > div > div.Home_Wrapper-sc-1lm6bf2.ePXBVM > div:nth-child(2) > div > div.content-box__content-section > div > div.Description_Expand-sc-mobr94.fXateZ > span')
            button.click() #若简介能够展开，则展开数据集简介
        except:
            pass
        try:
            Texts = browser.find_elements_by_css_selector('.markdown-converter__text--rendered')#爬取数据集简介文本
            TITLE = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.dataset-header-v2__title')))#数据集标题
            title = TITLE.text
            TAGS = browser.find_element_by_css_selector('body > main > div > div.site-layout__main-content > div > div > div > div > div.Home_Wrapper-sc-1lm6bf2.ePXBVM > div:nth-child(1) > div > div > div > div > div > div.QuickInfo_Tags-sc-b0c3af.bAArvc > div:nth-child(2)')
        except:
            continue
        tags = TAGS.text
        splited_tags = tags.split('\n,\n')#将所有的tag转化成列表
        print(title)
        print(line_)
        print(splited_tags)
        paths = []
        for tag in splited_tags:#通过tags将数据集简介归类，类别写入paths中
            if tag in label_crime:    
                paths.append('犯罪')
            if tag in label_CS:
                paths.append('计算机科学')
            if tag in label_economic:
                paths.append('经济')
            if tag in label_healthcare:
                paths.append('医疗')
            if tag in label_nature:
                paths.append('自然')
            if tag in label_sports:
                paths.append('运动')
            if tag in label_transport:
                paths.append('交通')
            if tag in labels_culture:
                paths.append('人文')
            if tag in lable_food_and_drink:
                paths.append('饮食')
        print(paths)
        print('--------------------')
        #将简介写入相应路径
        flag = 0 #标记是否有No discription yet
        for path in paths:
            try:
                with open('E:/python/朴素贝叶斯文本分类/训练集/' + path + '/{}.txt'.format(title), 'w', errors='ignore', encoding='utf-8') as file:
                    file.write(title+' :')#creat text
                    for Text in Texts:
                        file.write('\n\n'+Text.text)
                        if Text.text.find('No description yet') != -1:
                            flag = 1
                            break
                if flag == 1:
                    os.remove('E:/python/朴素贝叶斯文本分类/训练集/' + path + '/{}.txt'.format(title))
                    print('remove!')            
            except:
                pass

def main():
    n = 138  #访问kaggle的起始页数
    x = 50   #爬取的总页数
    '''browser = login_kaggle(url)'''
    browser = webdriver.Chrome()
    get_train(browser,n,x)

main()

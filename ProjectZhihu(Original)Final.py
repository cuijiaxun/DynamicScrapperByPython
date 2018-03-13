# -*- coding: UTF-8 -*-
import sys
import re
#import MySQLdb
import time
import xlrd
import xlwt
from bs4 import BeautifulSoup
from selenium import webdriver
import regex as re
import requests
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import collections 

#slove the ascii code problem
reload(sys)
sys.setdefaultencoding('utf-8')
#set the style of xls
def setStyle(name,height,bold=False):
    style = xlwt.XFStyle() # 初始化样式
    font = xlwt.Font() # 为样式创建字体
    font.name = name # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height
 
  # borders= xlwt.Borders()
  # borders.left= 6
  # borders.right= 6
  # borders.top= 6
  # borders.bottom= 6
 
    style.font = font
  # style.borders = borders
    return style
#write in the excel file
def writeExcel(AuthorName,authorsHrefs,authorsIntros,authorsLocation,authorsGender):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True)
    sheet1.col(0).width=256 * 20
    sheet1.col(1).width=256 * 60
    sheet1.col(2).width=256 * 40
    sheet1.col(3).width=256 * 20
    sheet1.col(4).width=256 * 20
    row0 = [u'Name',u'Href',u'Introduction',u'Location',u'Gender']
    for i in range(0,len(row0)):
        sheet1.write(0,i,row0[i],setStyle(u'宋体',220,True))
    for i in range(0,len(AuthorName)):
        sheet1.write(i+1,0,AuthorName[i],setStyle(u'宋体',220,True))
    for i in range(0,len(authorsHrefs)):
        sheet1.write(i+1,1,authorsHrefs[i],setStyle(u'宋体',220,True))
    for i in range(0,len(authorsIntros)):
        sheet1.write(i+1,2,authorsIntros[i],setStyle(u'宋体',220,True))
    for i in range(0,len(authorsLocation)):
        sheet1.write(i+1,3,authorsLocation[i],setStyle(u'宋体',220,True))
    for i in range(0,len(authorsGender)):
        sheet1.write(i+1,4,authorsGender[i],setStyle(u'宋体',220,True))
    f.save('Digester.xls')
#get rid of chinese punctuation
def removePunctuation(text):
    return re.sub(ur"\p{P}+", "", text)
   

#class Spider
class Spider:
      def ___init___(self):
          pass
      def signIn(self):
          global driver
          driver=webdriver.Firefox()                
          driver.get("http://www.zhihu.com")       
          time.sleep(2)                            
          driver.find_element_by_xpath("//a[@href='#signin']").click() 
          time.sleep(2)                            
          driver.find_element_by_name('account').send_keys('账号') 
          time.sleep(2)
          driver.find_element_by_name('password').send_keys('密码')
          time.sleep(10)
          #if there is verificationCode...
          #verificationCode=input('please type in verificationCode')
          #driver.find_element_by_name('captcha').send_keys(verificationCode)
          driver.find_element_by_css_selector('div.button-wrapper.command > button').click()
          cookie=driver.get_cookies()
          time.sleep(3)
          
      #get heated questions on food    
      def loadPage(self):
          global driver
          driver.get('https://www.zhihu.com/topic/19551137/hot')
          time.sleep(5)
      
      #decide how mant time does it need to load
      def excuteTime(self,times):
          for i in range(times + 1):
             global driver
             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")#load more
             time.sleep(5)

      def getPage(self):
      
          #analyze the html
          global driver
          html=driver.page_source
          soup1=BeautifulSoup(html,'lxml')
          
          #get authors' information
          authors=soup1.select('a.author-link')
          authorsAll=[]
          authorsHrefs=[]
          
          for author in authors:
              authorsAll.append(author.get_text())
              authorsHrefs.append('http://www.zhihu.com'+author.get('href'))
          
          #introduction
          authorsIntrosUrls=soup1.select('span.bio')
          authorsIntros=[]
          authorsLocation=[]
          authorsGender=[]
          
          for authorsIntrosUrl in authorsIntrosUrls:
              authorsIntros.append( removePunctuation( authorsIntrosUrl.get_text() ) )
             

          
          
          for  authorsHref in authorsHrefs:
              html = requests.get(authorsHref)
              text=html.text
              soup = BeautifulSoup(text,'lxml')
              authorsIntrosUrls=soup.select('span.bio')    
              
                  
              #location
              authorsLocationUrls=soup.find_all('span',class_="location item") 
              #gender
              authorsGenderUrls=soup.find_all('span',class_='item gender')
              
              for authorsLocationUrl in authorsLocationUrls:   
                  authorsLocation.append(authorsLocationUrl.get_text())
              
              for authorsGenderUrl in authorsGenderUrls:
                  y=authorsGenderUrl.i['class'][1].split('-')[2]
                  authorsGender.append(y) 
                  #print y
              
          writeExcel(authorsAll,authorsHrefs,authorsIntros,authorsLocation,authorsGender)  
          #f=open("Digester.txt",'w')  #write in file
          #for authorsAll,authorsHref,authorsIntro in zip(authorsAll,authorsHrefs,authorsIntros):
              #f.write(authorsAll+' ')
              #f.write(authorsHref+' ')
              #f.write(authorsIntro+'\n')
          #f.close()

def sortByCount(d):    
    d = collections.OrderedDict(sorted(d.items(), key = lambda t: -t[1]))  
    return d 
def anaLocation():
    data = xlrd.open_workbook('Digester.xls')
    table = data.sheets()[0]

    Locations=table.col_values(3)
    Location=dict()
    for i in range(0,len(Locations)):
       if Locations[i]!='':
          Location[Locations[i]]=Location.get(Locations[i],0)+1
       else:continue
    Location= sortByCount(Location) 
    #print Location
    key=Location.keys()
    value=Location.values()
    for k in range(10): 
        plt.plot(k, value[k], color = 'r')
        plt.bar(k, value[k], alpha = 0.3, color = 'b')

    _key=[]
    for k in range(10):
        key2=key[k]
        _key.append(key2)

    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['font.sans-serif'] = [u'SimHei']
    #coordinate 
    ax=plt.gca()
    ax.axis([0,10,0,20])
    ax.set_xticks(range(10))
    ax.set_xticklabels((_key))

    for label in plt.gca().xaxis.get_ticklabels():
        legal=('left')


    plt.xlabel(u'地区')
    plt.ylabel(u'数量')
    plt.title(u"吃货地域分布")           
    plt.show()


def anaGender():
    data = xlrd.open_workbook('Digester.xls')
    table = data.sheets()[0]
    Gender=table.col_values(4)
    male=0
    female=0
    unknown=0
    for x in Gender:
        if x=='male':
           male+=1
        elif x=='female':
           female+=1
        else:
           unknown+=1
    #print male, female, unknown
    gender=[male, female, unknown]
    strgender=[u'男', u'女', u'未知']
    #开始画图
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['font.sans-serif'] = [u'SimHei']
    for k in range(3): 
        plt.plot(k,gender[k], color = 'r')
        plt.bar(k, gender[k], alpha = 0.3, color = 'g')
    #coordinate 
    ax=plt.gca()
    ax.axis([0,3,0,100])
    ax.set_xticks(range(3))
    ax.set_xticklabels(strgender)

    for label in plt.gca().xaxis.get_ticklabels():
        legal=('left')


    plt.xlabel(u'性别')
    plt.ylabel(u'数量')
    plt.title(u"吃货数量性别统计")           
    plt.show()
        



def main():
    spider=Spider()
    spider.signIn()
    spider.loadPage()
    spider.excuteTime(10)
    spider.getPage()
    print "done!"

    anaLocation()
    anaGender()
    
    print "done!"
if __name__ == "__main__":
    main()


              
      
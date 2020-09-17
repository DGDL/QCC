import time
import xlwt
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#这个是一个用来控制chrome以无界面模式打开的浏览器
#创建一个参数对象，用来控制chrome以无界面的方式打开
chrome_options = Options()
#后面的两个是固定写法 必须这么写，如果不是这样写，就是自动化
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

#驱动Chrome
driver = webdriver.Chrome(chrome_options=chrome_options)

#设置表格
book = xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet = book.add_sheet('mysheet',cell_overwrite_ok=True)
sheet.write(0,0,'boss')


#开始解析，提取
class analysis():
    def __init__(self,url,name):
        self.url=url
        self.name = name
        print(self.name)
        driver.get(self.url)
        time.sleep(3)
    def Re_Url(self):
        #二级URL
        driver.get(self.url+self.name)
        print (self.url)
        #隐式等待
        time.sleep(3)
        print (driver.page_source)

        #正则三级URL
        pattem = re.compile(r"/firm+[^\s]+\.html*")
        url_link = re.findall(pattem,driver.page_source)
        print(url_link)
        #计数
        shu = 0
        for x in url_link:
            shu+=1
            self.url+=x
            self.write(shu)
    def write(self,x):
        #三级URL
        driver.get(self.url)
        print (x) 
        #隐式等待
        time.sleep(3)
        
        #xpath匹配数据 
        try:
            enterprise_name = driver.find_element_by_xpath("//div[@class='content']//div[@class='company-name']")
            people_name = driver.find_element_by_xpath("//div[@class='content']//div[@class='pull-left']//a")
            contact = driver.find_element_by_xpath("//div[@class='content']/div[@class='content-block']/div[@class='contact-info-wrap']")
            establish_time = driver.find_element_by_xpath("//div[@class='content']//div[@class='basic-wrap']//tbody/tr[2]/td[1]/div[@class='v']")
         #保存数据
            sheet.write(x,0,enterprise_name.text)
            sheet.write(x,1,people_name.text)
            sheet.write(x,2,contact.text)
            sheet.write(x,0,establish_time.text)
        except:
            print("有东西找不到，报错了")

if __name__=='__main__':
    #一级URL
    url = "http://m.qcc.com"
    name="华为"
    print (url)
    Qcc=analysis(url,"/search?key="+name)
    Qcc.Re_Url()
     #保存表格
    book.save('./text.xls')
    """Qcc反爬虫机制很完善，规定时间访问30次，头文件，cookie有时间限制
    破解反爬虫，使用selenium 访问他的手机官网页面（手机没这么快完善，直接提交搜索页面被反），获取信息伪装浏览器（本身就是）
    """


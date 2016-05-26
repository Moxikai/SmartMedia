#_*_coding:utf-8_*_
from selenium import webdriver
import re
from time import sleep
from urllib2 import urlopen
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class Getfile(object):
    def __init__(self,url):
        self.url=url
        self.VID=''
        self.VID_url=''
        self.file_url=''
    #从freeget.co获取vid
    def get_VID_url(self):

        driver = webdriver.Chrome()
        url='http://freeget.co/'
        driver.get(url)
        #录入数据
        driver.find_element_by_id('url-field').send_keys(self.url)
        #点击
        driver.find_element_by_id('extract-button').click()
        try:
            #element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "video-download-button")))
            sleep(0.8)
            driver.find_element_by_xpath('//*[@id="video-download-button"]').click()
            #获取播放链接

            data = driver.find_element_by_xpath('//*[@id="progress-info"]/p[2]/a').get_attribute('href')
        finally:
            driver.quit()
        #解析链接
        if data:
            print '获取播放地址成功:%s'%data
            self.VID_url=data
            #解析出VID值
            pattern=re.compile('(?<=VID=)\S{1,}')
            self.VID=pattern.findall(data)[0]
        else:
            print "获取播放链接失败"
    #获取文件下载地址
    def get_file(self):
        target_str='getfile_jw'
        new_url=self.VID_url.replace('ev',target_str)
        print "新网址为%s"%(new_url)
        res=urlopen(new_url)
        #print res.read()
        #抽取文件下载地址
        pattern = re.compile('(?<=file=)\S{1,}.mp4')
        link = pattern.findall(res.read())
        if link:
            #print "抽取下载地址为%s"% link[0]
            self.file_url=link[0]
    def run(self):
        self.get_VID_url()
        self.get_file()

from .models import Video
class Handler_data():

    def get_viewURL(self):
        data = Video.query.filter(Video.play_url !='').all()
        return data
    def update_playURL(self,id,play_url):
        Video.query.filter(Video.id ==id).update({play_url:play_url})


if __name__ == '__main__':
    pass


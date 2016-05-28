# _*_ coding:utf-8 _*_
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column,CHAR,Integer,DateTime,Text
from sqlalchemy.ext.declarative import declarative_base
import os
#声明基类
Base = declarative_base()
#定义模型
class Video(Base):
    __tablename__ ='videos' #默认使用复数

    id=Column(Text,primary_key=True) #view_key
    title=Column(Text) #标题
    duration=Column(Integer) #时长
    time_created=Column(Text) #上传时间,倒退的模糊时间
    author=Column(Text) #作者
    viewed=Column(Integer) #查看数
    remarked=Column(Integer) #收藏数
    comments=Column(Integer) #评论数
    remarks=Column(Integer) #得分
    view_url=Column(Text) #观看地址
    img_url=Column(Text) #缩略图地址,默认3个,逗号分隔
    VID_url=Column(Text) #获取到的无限制观看地址
    file_url=Column(Text) #临时下载地址
    updated=Column(Text)#爬虫更新时间

#初始化数据库连接
#获取当前文件夹路径
"""
basepath=os.path.abspath(os.path.dirname(__file__))
datapath = os.path.join(basepath,'media.sqlite')
"""
engine =create_engine('sqlite:///'+ '/Users/guangtouling/Documents/SmartMedia/media.sqlite')
#创建会话连接
DBsession = sessionmaker(bind=engine)
#创建数据库
def create_db():
    Base.metadata.create_all(engine)


if __name__ =='__main__':
    create_db()

#_*_ coding:utf-8 _*_
from flask import Blueprint

#实例化一个蓝本对象
main = Blueprint('main',__name__)
from . import views,error


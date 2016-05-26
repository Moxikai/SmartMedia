#_*_coding:utf-8_*_
from flask import Flask,render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from flask_wtf.csrf import CsrfProtect

#以上为导入的模块,注意扩展通过flask.ext导入的
#暂时没有程序实例,因此扩展没有初始化
bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
#表单保护
#csrf = CsrfProtect()

#定义初始化方法,传入配置名称
def create_app(config_name):
    app = Flask(__name__)
    #获取配置
    app.config.from_object(config[config_name])
    #从配置初始化APP,注意init_app()方法没有定义
    #config[config_name].init_app(app)

    #初始化扩展
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    #csrf.init_app(app)
    #蓝本注册到程序APP上
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


if __name__=='__main__':
    print create_app('default')

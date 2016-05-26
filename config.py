#_*_coding:utf-8_*_
import os
#基础路径,获取配置文件所在路径
basedir=os.path.abspath(os.path.dirname(__file__))
#基础配置
class Config:
    #启用跨站攻击保护
    CSRF_ENABLE = True
    #表单密钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    #数据库自动提交更新操作
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    #其他配置
    #初始化方法
    @staticmethod
    def init_app():
        pass
#继承基础配置类
class DevelopmentConfig(Config):
    DEBUG = True
    #邮件发送服务器
    MAIL_SERVER = 'smtp.google.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    #从环境变量中读取发件人的邮箱账号\密码
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    #开发数据库从环境变量中读取,或者使用如下默认路径
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir,'data-dev.sqlite')

#测试配置
class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir,'data-test.sqlite')

#生产环境配置
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir,'data.sqlite')
#统一命名配置
config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
}


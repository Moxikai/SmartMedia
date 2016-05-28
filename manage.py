#!/usr/bin/env python
#_*_coding:utf-8_*_
import os
from app import create_app,db
from app.models import Video
from flask.ext.script import Manager,Shell
from flask.ext.migrate import Migrate,MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

#自定义过滤器
def get_img_list(str):
    list=str.split(';')
    return list[0]
env = app.jinja_env
env.filters['get_img_list']=get_img_list

manager = Manager(app)
migrate=Migrate(app,db)

def make_shell_context():
    return dict(app = app,db = db,Video = Video)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

@manager.command
def test():
     """Run the unit tests."""
     import unittest
     tests = unittest.TestLoader().discover('tests')
     unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
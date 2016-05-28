#_*_coding:utf-8_*_
#from wtforms import Form
from flask.ext.wtf import Form
from wtforms import SubmitField,SelectField,StringField,BooleanField
from wtforms.validators import Required
class NameForm(Form):
    find_type = SelectField(u'查询类型', choices=[('title', '标题'), ('author', '作者')])
    keyword=StringField(unicode(u'请输入查询关键词'),validators=[Required()])
    submit=SubmitField('submit')
class CheckForm(Form):
    choice= BooleanField()
    submit = SubmitField(u'解析')
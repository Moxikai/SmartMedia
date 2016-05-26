#_*_coding:utf-8_*_
from flask import render_template,session,redirect,url_for
from .import main
from .. import db
from ..models import Video
from ..forms import NameForm
from ..parse import Getfile
from flask import request,abort
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#查询首页
@main.route('/',methods=['GET','POST'])
def index():
    #判断参数
    form=NameForm()
    if form.validate_on_submit():
        type=form.find_type.data
        data=form.keyword.data
        #查询参数
        para='%'+data+'%'
        para_encode=unicode(para)
        session['find_type']=type
        session['find_para']=para_encode
        #查询
        return redirect(url_for('main.index_page',id=1))
    return render_template('index.html',form=form)
    #return render_template('3.html')

#处理查询结果,分页
@main.route('/index/<int:id>')
def index_page(id):

    try:
        if session['find_type']=='title':
            paginate=Video.query.filter(Video.title.like(session['find_para'])).paginate(id,12,False)
        elif session['find_type']=='author':
            paginate=Video.query.filter(Video.author.like(session['find_para'])).paginate(id,12,False)
        object_list=paginate.items
        #return render_template('video.html',pagination=paginate,object_list=object_list)
        return render_template('video.html',pagination=paginate,object_list=object_list)
    except Exception:
        #没有历史查询结果,转到首页
        return redirect(url_for('main.index'))

@main.route('/parse/<string:url_id>')
def parse(url_id):
    pass
    #获取播放地址
    videos=Video.query.filter(Video.id==url_id).all()

    video=videos[0]
    getfile=Getfile(video.url)
    getfile.run()
    play_url=getfile.VID_url
    file_url=getfile.file_url
    if play_url:
        #更新列
        Video.query.filter(Video.id==url_id).update({Video.download_url:file_url,
                                                   Video.play_url:play_url})
        #设置VID到session
        session['VID']=video.play_url
        session['file_url']=video.download_url
        session['title']=video.title
        return render_template('play.html',VID=session['VID'],file_url=session['file_url'],title=session['title'])
    else:
        return unicode(u'<h1>没有解析到网址</h1>')

@main.route('/play/<string:url_id>')
def play(url_id):
    if url_id !='pre':
        videos=Video.query.filter(Video.id==url_id).all()
        video=videos[0]
        #设置session
        pattern=re.compile('(?<=VID=)\S{1,}')
        session['VID']=pattern.findall(video.play_url)[0]
        #更新文件地址
        getfile=Getfile(video.play_url)
        getfile.get_file()
        session['file_url']=getfile.file_url
        #更新到数据库
        Video.query.filter(Video.id==url_id).update({Video.download_url:session['file_url']})
        session['title']=video.title
        return render_template('play.html',VID=session['VID'],file_url=session['file_url'],title=session['title'])
    else:
        #没有播放记录,直接跳转到首页
        try:
            return render_template('play.html',VID=session['VID'],file_url=session['file_url'],title=session['title'])
        except Exception:
            return redirect(url_for('main.index'))
#查询同一作者上传
@main.route('/author/<string:name>')
def author(name):
    if name:
        para_encode=unicode(name)
        session['find_type']='author'
        session['find_para']=para_encode
        return redirect(url_for('main.index_page',id=1))

    else:
        return redirect(url_for('main.index'))
@main.route('/playlist/<int:id>')
def getplaylist(id=1):

    try:
        paginate=Video.query.filter(Video.play_url !='').paginate(id,12,False)
        object_list=paginate.items
        return render_template('playlist.html',pagination=paginate,object_list=object_list)
    except Exception:
        return redirect(url_for('main.index'))

if __name__ == '__main__':
    pass

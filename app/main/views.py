#_*_coding:utf-8_*_
from flask import render_template,session,redirect,url_for
from .import main
from .. import db
from ..models import Video
from ..forms import NameForm,CheckForm
from parse.parse import Getfile
from flask import request,abort,flash
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
        session['find_type']=type
        session['find_para']=data
        #查询
        return redirect(url_for('main.index_page',id=1))
    return render_template('index.html',form=form)
    #return render_template('3.html')

#处理查询结果,分页
@main.route('/index/<int:id>',methods=['GET','POST'])
def index_page(id):
    #获取选择的view_url
    if request.method == 'POST':
        view_urls=(request.form.getlist('get_video_id'))
        for view_url in view_urls:
            getfile=Getfile(view_url)
            getfile.run()
            VID_url=getfile.VID_url
            file_url=getfile.file_url
            VID=getfile.VID
            if VID_url:
                #更新列
                Video.query.filter(Video.view_url==view_url).update({Video.file_url:file_url,
                                                           Video.VID_url:VID_url})
    #查询参数按照空格分割
    para_list=session['find_para'].split(' ')
    list_encode=[]
    for para in para_list:
        #剔除空格
        if para !='':
            para='%'+para+'%'
            para_encode=unicode(para)
            list_encode.append(para_encode)
    #paginate=Video.query.filter(Video.title.like(session['find_para'])).paginate(id,12,False)
    try:
        ob=Video.query
        for i in list_encode:
            if session['find_type']=='title':
                ob = ob.filter(Video.title.like(i))
            elif session['find_type']=='author':
                ob = ob.filter(Video.author.like(i))
        paginate = ob.paginate(id,12,False)
        object_list = paginate.items
        if len(object_list) > 0:
            #return render_template('video.html',pagination=paginate,object_list=object_list)
            return render_template('video.html',pagination=paginate,object_list=object_list)
        else:
            flash('提示:多个关键词以空格分开,如果看到此消息请修改关键词')
            return redirect(url_for('main.index'))
    except Exception:
        flash('对不起,出错了!')

@main.route('/parse/<string:url_id>')
def parse(url_id):
    pass
    #获取播放地址
    videos=Video.query.filter(Video.id==url_id).all()

    video=videos[0]
    getfile=Getfile(video.view_url)
    getfile.run()
    VID_url=getfile.VID_url
    file_url=getfile.file_url
    VID=getfile.VID
    if VID_url:
        #更新列
        Video.query.filter(Video.id==url_id).update({Video.file_url:file_url,
                                                   Video.VID_url:VID_url})
        #设置VID到session
        session['VID']=VID
        session['file_url']=video.file_url
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
        session['VID']=pattern.findall(video.VID_url)[0]
        #更新文件地址
        getfile=Getfile(video.VID_url)
        getfile.get_file()
        session['file_url']=getfile.file_url
        #更新到数据库
        Video.query.filter(Video.id==url_id).update({Video.file_url:session['file_url']})
        session['title']=video.title
        return render_template('play.html',VID=session['VID'],file_url=session['file_url'],title=session['title'])
    else:
        #没有播放记录,直接跳转到首页
        flash('没有播放记录!')
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
        paginate=Video.query.filter(Video.VID_url !='').paginate(id,12,False)
        object_list=paginate.items
        return render_template('playlist.html',pagination=paginate,object_list=object_list)
    except Exception:
        flash('没有可以播放的视频,请自行解析!')
        return redirect(url_for('main.index'))

if __name__ == '__main__':
    pass

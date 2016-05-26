#_*_ coding:utf-8 _*_
from . import db
class Video(db.Model):
    pass
    #表名称
    __tablename__='videos'
    id =db.Column(db.CHAR,primary_key=True)
    title=db.Column(db.CHAR)
    duration=db.Column(db.VARCHAR(40))
    time_created=db.Column(db.VARCHAR(40))
    author=db.Column(db.VARCHAR(40))
    viewed=db.Column(db.Integer)
    remarked=db.Column(db.Integer)
    comments=db.Column(db.Integer)
    remarks=db.Column(db.Integer)
    url=db.Column(db.Text)
    imgs=db.Column(db.Text)
    play_url=db.Column(db.Text)
    download_url=db.Column(db.Text)

    def __init__(self,id,title,duration,time_created,author,
                 viewed,remarked,comments,remarks,url,imgs,play_url,download_url):
        self.id=id
        self.title=title
        self.duration=duration
        self.time_created=time_created
        self.author=author
        self.viewed=viewed
        self.remarked=remarked
        self.comments=comments
        self.remarks=remarks
        self.url=url
        self.imgs=imgs
        self.play_url=play_url
        self.download_url=download_url
    def __repr__(self):
        return '<Video %r>'% self.title
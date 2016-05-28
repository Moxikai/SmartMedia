#_*_ coding:utf-8 _*_
from . import db
class Video(db.Model):
    pass
    #表名称
    __tablename__='videos'
    id =db.Column(db.Text,primary_key=True)
    title=db.Column(db.Text)
    duration=db.Column(db.Integer)
    time_created=db.Column(db.Text)
    author=db.Column(db.Text)
    viewed=db.Column(db.Integer)
    remarked=db.Column(db.Integer)
    comments=db.Column(db.Integer)
    remarks=db.Column(db.Integer)
    view_url=db.Column(db.Text)
    img_url=db.Column(db.Text)
    VID_url=db.Column(db.Text)
    file_url=db.Column(db.Text)
    updated=db.Column(db.Text)
    """
    def __init__(self,id,title,duration,time_created,author,
                 viewed,remarked,comments,remarks,view_url,img_url,VID_url,file_url,updated):
        self.id=id
        self.title=title
        self.duration=duration
        self.time_created=time_created
        self.author=author
        self.viewed=viewed
        self.remarked=remarked
        self.comments=comments
        self.remarks=remarks
        self.view_url=view_url
        self.img_url=img_url
        self.VID_url=VID_url
        self.file_url=file_url
        self.updated = updated
    def __repr__(self):
        return '<Video %r>'% self.title
    """
# -*- coding: utf-8 -*-
from django.db import models
import time
from django.utils import timesince,html
from MiniMicroBlog.settings import *
import PIL
from StringIO import StringIO
from MiniMicroBlog.utils import formatter,encrypt

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models import signals
from django.dispatch import dispatcher


class PostWay(models.Model):
    name = models.CharField('方式名称',max_length=20)

    def __unicode__(self):
        return self.name

    def save(self):
        return super(PostWay,self).save()

    class Meta:
        verbose_name='分类'
        verbose_name_plural='分类'


class Status(models.Model):
    kind = models.CharField('消息状态',max_length=20)

    def __unicode__(self):
        return self.kind

    def save(self):
        return super(Status,self).save()

    class Meta:
        verbose_name='消息状态'
        verbose_name_plural='消息状态'


class User(models.Model):
    username=models.CharField('用户名',max_length=20)
    userpwd=models.CharField('密码',max_length=50)
    realname=models.CharField('姓名',max_length=20)
    email=models.EmailField('邮件')
    photo=models.ImageField('头像',upload_to='face/%Y/*m/%d',default='',blank=True)
    url=models.CharField('个人主页',max_length=100,default='',blank=True)
    aboutme=models.TextField('关于我',max_length=500,default='',blank=True)
    #about_me=models.TextField('(详)关于我',max_length=500,default='',blank=True)
    regtime=models.DateTimeField('注册时间',auto_now=True)
    friend=models.ManyToManyField('self',verbose_name='朋友')

    def __unicode__(self):
        return self.username

    def formattime(self):
        return self.regtime.strftime('%Y-%m-%d %H:M:%S')

    def shortcut(self):
        return formatter.substr(self.aboutme,20)

    def save(self,modify_pwd=True):
        return super(User,self).save()

    class Meta:
        verbose_name=u'用户'
        verbose_name_plural=u'用户'




class Shuoshuo(models.Model):
    message=models.TextField('消息',max_length=500)
    uptime=models.DateTimeField('发布时间',auto_now=True)
    postway=models.ForeignKey(PostWay,verbose_name='方式')
    user=models.ForeignKey(User,verbose_name='发布人')

    events=generic.GenericRelation('Event')

    def __unicode__(self):
        return self.message

    def description(self):
        return u'你的好友 %s 发表了说说"%s"' % (self.user.username,self.message)

    def shortcut(self):
        return formatter.substr(self.message,30)

    def fomattime(self):
        return self.uptime.strftime('%Y-%m-%d %H:%M:%S')

    def postwayname(self):
        return self.postway.name

    def username(self):
        return self.user.username

    def save(self):
        self.message=formatter.contentTinyUrl(self.message)
        self.message=html.escape(self.message)
        super(Shuoshuo,self).save()

    class Meta:
        verbose_name=u'说说'
        verbose_name_plural=u'说说'

class Comment(models.Model):
    comment=models.TextField('留言',max_length=500)
    uptime=models.DateTimeField('留言时间',auto_now=True)
    shuoshuo=models.ForeignKey(Shuoshuo,verbose_name='说说')
    user=models.ForeignKey(User,verbose_name='留言人')

    def __unicode__(self):
        return self.comment

    def shortcut(self):
        return formatter.substr(self.comment,30)

    def fomattime(self):
        return self.uptime.strftime('%Y-%m-%d %H:%M:%S')

    def username(self):
        return self.user.username

    def save(self):
        self.comment=formatter.contentTinyUrl(self.comment)
        self.comment=html.escape(self.comment)
        super(Comment,self).save()

    class Meta:
        verbose_name=u'留言'
        verbose_name_plural=u'留言'


class MsgText(models.Model):
    user=models.ForeignKey(User,verbose_name='发送人')
    msgtext=models.TextField('内容',max_length=500,blank=False)
    sendtime=models.DateTimeField('发送时间',auto_now=True)

    def __unicode__(self):
        return self.msgtext

    def senduser(self):
        return self.user.username

    def save(self):
        return super(MsgText,self).save()

    class Meta:
        verbose_name=u'消息内容'
        verbose_name_plural=u'消息内容'


class Message(models.Model):
    user=models.ForeignKey(User,verbose_name='收信人')
    msgtext=models.ForeignKey(MsgText,verbose_name='消息内容')
    status=models.ForeignKey(Status,verbose_name='状态')

    def __unicode__(self):
        return self.user.username

    def recvuser(self):
        return self.user.username

    def kind(self):
        return  self.status.kind

    def message(self):
        return self.msgtext.msgtext

    def save(self):
        return super(Message,self).save()

    class Meta:
        verbose_name=u'消息'
        verbose_name_plural=u'消息'


class Event(models.Model):
    '''
    class ContentType(models.Model):
        name=models.CharField(max_length=100)
        app_label=models.CharField(max_length=100)
        model=models.CharField(_('python model class name'),max_length=100)
        objects=ContentTypeManager()
    '''
    user=models.ForeignKey(User)
    content_type=models.ForeignKey(ContentType)
    object_id=models.PositiveIntegerField()
    event=generic.GenericForeignKey('content_type','object_id')
    created=models.DateTimeField(u'说说发表时间',auto_now_add=True)

    def __unicode__(self):
        return u'%s的说说：%s'% (self.user,self.description())

    def description(self):
        return self.event.description()


#def shuoshuo_save(sender,instance,signal,*args,**kwargs):
def shuoshuo_save(sender,instance,created,*args,**kwargs):
    shuoshuo=instance
    #if (shuoshuo.updated-shuoshuo.created).seconds <1:
    if created:
        event=Event(user=shuoshuo.user,event=shuoshuo)
        #time.sleep(0.1)
        event.save()

#dispatcher.connect(shuoshuo_save,signal=signals.post_save,sender=Shuoshuo)
signals.post_save.connect(shuoshuo_save,sender=Shuoshuo)








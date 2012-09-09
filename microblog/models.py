# -*- coding: utf-8 -*-
from django.db import models
import time
from django.utils import timesince,html
from MiniMicroBlog.settings import *
import PIL
from StringIO import StringIO
from MiniMicroBlog.utils import formatter,encrypt

class PostWay(models.Model):
    name = models.CharField('方式名称',max_length=20)

    def __unicode__(self):
        return self.name

    def save(self):
        return super(PostWay,self).save()

    class Meta:
        verbose_name='分类'
        verbose_name_plural='分类'


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

    def __unicode__(self):
        return self.message

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










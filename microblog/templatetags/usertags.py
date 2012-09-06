# -*- coding:utf-8 -*-
from django.template import Library
from microblog.models import *
from settings import *

register=Library()

def getPhotoUrl(size,content):
    '''
    自定义过滤器，返回对应图片大小，但是得保存过多冗余图片，暂不使用，考虑图片缩放或现在的笨方法
    '''
    if content:
        return MEDIA_URL + 'photo/%d/%s' % (size,content)
    else:
        return DEFAULT_PHOTO % size

def photo32(content):
    return getPhotoUrl(32,content)

def photo41(content):
    return getPhotoUrl(41,content)

def photo(content):
    return getPhotoUrl(75,content)

register.filter('photo',photo)
register.filter('photo41',photo41)
register.filter('photo32',photo32)

def userUrl(username):
    return '%suser/%s' % (APP_DOMAIN,username)

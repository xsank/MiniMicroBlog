#-*- coding:utf-8 -*-

import sys,os
import time
from StringIO import StringIO
from PIL import Image
from settings import *
#import  ImageFilter

def uploadPhoto(data,name):
    _state={
        'success':False,
        'message':'',
        }
    if data.size>0:
        base_im=Image.open(data)
        size100 = (75,75)
        size_array=(size100,)
        file_name = name+time.strftime("%Y_%m_%d") + '.png'
        file_root_path = '%sphoto/' % (MEDIA_ROOT)

        for size in size_array:
            file_middle_path = '%d/' % size[0]
            file_path = os.path.abspath(file_root_path + file_middle_path)
            im = base_im
            im = make_thumb(im,size[0])

            if not os.path.exists(file_path):
                os.makedirs(file_path)

            im.save('%s/%s' % (file_path,file_name),'PNG')


        _state['success'] = True
        _state['message'] =  file_name
    else:
        _state['success'] = False
        _state['message'] = '还未选择要上传的文件。'

    return _state

def make_thumb(im, size=75):
    width, height = im.size
    if width == height:
        region = im
    else:
        if width > height:
            delta = (width - height)/2
            box = (delta, 0, delta+height, height)
        else:
            delta = (height - width)/2
            box = (0, delta, width, delta+width)
        region = im.crop(box)

    thumb = region.resize((size,size), Image.ANTIALIAS)
    return thumb

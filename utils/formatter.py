# -*- coding:utf-8 -*-
import re,urllib
from MiniMicroBlog.settings import *
from django.shortcuts import render_to_response
from django.template import context
from django.core.paginator import Paginator,InvalidPage

def tinyUrl(url):
    apiurl="http://tinyurl.com/api-create.php?url="
    tinyurl=urllib.urlopen(apiurl+url).read()
    return tinyurl

def contentTinyUrl(content):
    regex_url=r'http:\/\/([\w.]+\/?)\S*'
    for match in re.finditer(regex_url, content):
        url = match.group(0)
        content = content.replace(url,tinyUrl(url))
    return content

def substr(content,length,add_dot=True):
    if(len(content)>length):
        content=content[:length]
        if(add_dot):
            content=content[:len(content)-3]+'...'
    return content

def pagebar(objects,page_index,name='',template='sidebar/pagebar.html'):
    page_index=int(page_index)
    paginator=Paginator(objects,PAGE_SIZE)
    #if(name):
    #    template='sidebar/pagebar.html'
    return render_to_response(
        template,{
            'paginator': paginator,
            'name' : name,
            'has_pages': paginator.num_pages > 1,
            'has_next': paginator.page(page_index).has_next(),
            'has_prev': paginator.page(page_index).has_previous(),
            'page_index': page_index,
            'page_next': page_index + 1,
            'page_prev': page_index - 1,
            'page_count': paginator.num_pages,
            'row_count' : paginator.count,
            'page_nums': range(paginator.num_pages+1)[1:],
        }).content

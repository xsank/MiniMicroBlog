#-*- coding:utf-8 -*-

from models import *
from forms import *
from datetime import datetime
from django.http import HttpResponseRedirect,HttpResponse,Http404,HttpResponseServerError
from django.template import RequestContext,Context,loader
from django.shortcuts import render_to_response,get_object_or_404
from django.views.generic import list_detail
from django.contrib.auth.decorators import login_required
from utils import mailer,formatter,encrypt,upload,mail
import random,string

def signup(request):
    if request.method=='POST':
        form= RegistForm(request.POST)
        if form.is_valid():
            user=User(
                username=form.clean_username(),
                email=form.clean_email(),
                realname=form.cleaned_data['realname'],
                userpwd=encrypt.encodeMD5(form.clean_checkpassword()),
                photo="",
                url="",
                aboutme="",
                regtime=datetime.now()
            )
            user.save()
            #mailer.sendRegistSuccessMail(user)
            return HttpResponseRedirect('/register/success/')
    else:
        form=RegistForm()
    variables=RequestContext(request,{'form':form})
    return render_to_response('login/signup.html',variables)

def login(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.clean_username()
            try:
                form.clean_password()
            except :
                pass
            request.session['islogin']=True
            request.session['username']=username
            request.session['userid']=User.objects.get(username=request.session['username']).id
            return HttpResponseRedirect('/home/1/')
    else:
        form=LoginForm()
    variables=RequestContext(request,{'form':form})
    if request.META['PATH_INFO'] == '/login/':
        return render_to_response('login/signin.html',variables)
    else:
        return render_to_response('login/index.html',variables)

def logout(request):
    request.session.clear()
    return HttpResponseRedirect('/')

def loadhome(request,pageindex=1):
    #for i in request.session.keys():
    #    print request.session[i]
    if request.session:
        userinfo=User.objects.get(id=request.session['userid'])
        friendlist=userinfo.friend.all()
        mylist=Shuoshuo.objects.filter(user=userinfo).order_by('-id')
        pagebar=formatter.pagebar(mylist,pageindex,'home','microblog/pagebar.html')
        offsetindex=int(int(pageindex)-1)*PAGE_SIZE
        lastindex=PAGE_SIZE*int(pageindex)
        mylist=mylist[offsetindex:lastindex]
        return  render_to_response('microblog/home.html',{
            'session':request.session,
            'userinfo':userinfo,
            'list':mylist,
            'friendlist':friendlist,
            'pagebar':pagebar,}
        )
    else:
        return HttpResponseRedirect('/')

def loadsquare(request,pageindex=1):
    if request.session:
        userinfo=User.objects.get(id=request.session['userid'])
        friendlist=userinfo.friend.all()
        otherlist=Shuoshuo.objects.all().order_by('-id')
        pagebar=formatter.pagebar(otherlist,pageindex,'square','microblog/pagebar.html')
        offsetindex=(int(pageindex)-1)*PAGE_SIZE
        lastindex=PAGE_SIZE*int(pageindex)
        otherlist=otherlist[offsetindex:lastindex]
        return render_to_response('microblog/square.html',{
            'session':request.session,
            'userinfo':userinfo,'list':otherlist,
            'friendlist':friendlist,
            'pagebar':pagebar,}
        )
    else:
        return HttpResponseRedirect('/')

def loadusers(request,pageindex=1):
    if request.session:
        userinfo=User.objects.get(id=request.session['userid'])
        userlist=User.objects.all().order_by('-id')
        friendlist=userinfo.friend.all()
        pagebar=formatter.pagebar(friendlist,pageindex,'find','microblog/pagebar.html')
        offsetindex=(int(pageindex)-1)*PAGE_SIZE
        lastindex=PAGE_SIZE*int(pageindex)
        friendlist=friendlist[offsetindex:lastindex]
        return render_to_response('microblog/findwho.html',{
            'session':request.session,
            'userlist':userlist,
            'userinfo':userinfo,
            'friendlist':friendlist,
            'pagebar':pagebar,}
        )
    else:
        return HttpResponseRedirect('/')

def loadfollowuser(request,pageindex=1):
    if request.session:
        userinfo=User.objects.get(id=request.session['userid'])
        friendlist=userinfo.friend.all()
        pagebar=formatter.pagebar(friendlist,pageindex,'find','microblog/pagebar.html')
        offsetindex=(int(pageindex)-1)*PAGE_SIZE
        lastindex=PAGE_SIZE*int(pageindex)
        friendlist=friendlist[offsetindex:lastindex]
        return render_to_response('microblog/followuser.html',{
            'session':request.session,
            'userinfo':userinfo,
            'friendlist':friendlist,
            'pagebar':pagebar,}
        )
    else:
        return HttpResponseRedirect('/')

def loadusershuoshuo(request,username,pageindex=1):
    if request.session:
        userinfo=User.objects.get(id=request.session['userid'])
        friendlist=userinfo.friend.all()
        selectuser=get_object_or_404(User,username=username)
        shuoshuolist=Shuoshuo.objects.filter(user=selectuser).order_by('-id')
        pagebar=formatter.pagebar(shuoshuolist,pageindex,'user/'+username,'microblog/pagebar.html')
        offsetindex=int(int(pageindex)-1)*PAGE_SIZE
        lastindex=PAGE_SIZE*int(pageindex)
        shuoshuolist=shuoshuolist[offsetindex:lastindex]
        return  render_to_response('microblog/square.html',{
            'session':request.session,
            'userinfo':userinfo,
            'list':shuoshuolist,
            'friendlist':friendlist,
            'pagebar':pagebar,}
        )
    else:
        return HttpResponseRedirect('/')

def setting(request):
    if request.session:
        userinfo=User.objects.get(id=request.session['userid'])
        friendlist=userinfo.friend.all()
        if request.method=='POST':
            userinfo.realname=request.POST['realname']
            userinfo.email=request.POST['email']
            userinfo.aboutme=request.POST['aboutme']
            userinfo.url=request.POST['url']
            userinfo.photo=request.FILES.get('photo',None)
            if userinfo.photo:
                uploadstate=upload.uploadPhoto(userinfo.photo,userinfo.username)
                if uploadstate['success']:
                    userinfo.photo=uploadstate['message']
            userinfo.save()
        return render_to_response('microblog/setting.html',{
            'session':request.session,
            'friendlist':friendlist,
            'userinfo':userinfo})
    else:
        return HttpResponseRedirect('/')

def changepwd(request):
    if request.session:
        error={}
        user=User.objects.get(id=request.session['userid'])
        friendlist=user.friend.all()
        if request.method=='POST':
            if encrypt.encodeMD5(request.POST['oldpassword']) != user.userpwd:
                error['wrong']=u'原始密码错误！'
            if len(request.POST['newpassword']) <6:
                error['short']=u'新密码少于6位'
            if request.POST['newpassword'] != request.POST['checkpassword']:
                error['nomatch']=u'密码不一致！'
            if not error:
                user.userpwd=encrypt.encodeMD5(request.POST['newpassword'])
                user.save()
                error['no']=u'修改成功！'
        return render_to_response('microblog/changepwd.html',{
            'session':request.session,
            'friendlist':friendlist,
            'error':error,'userinfo':user})
    else:
        return HttpResponseRedirect('/')

def sendpwd(request):
    if request.method=='POST':
        form=ResetForm(request.POST)
        if form.is_valid():
            email=form.clean_email()
            userinfo=User.objects.get(email=email)
            newpwd=''.join(random.sample(string.ascii_letters+string.digits,8))
            userinfo.userpwd=encrypt.encodeMD5(newpwd)
            userinfo.save()
            mail.send_mail_password(userinfo,newpwd)
            return HttpResponseRedirect('/reset/success/')
    else:
        form=ResetForm()
    variables=RequestContext(request,{'form':form})
    return render_to_response('login/reset.html',variables)

def publish(request):
    if request.session:
        error={}
        user=User.objects.get(id=request.session['userid'])
        friendlist=user.friend.all()
        if request.method=='POST':
            lenm=len(request.POST['message'])
            if lenm<3 or lenm>100:
                error['wrong']=u'你写的不正常，刷的吧！！！'
            if not error:
                shuoshuo=Shuoshuo(
                    message=request.POST['message'],
                    postway_id=1,
                    user_id=request.session['userid'],
                )
                shuoshuo.save()
                error['no']=u'发表成功！'
        return render_to_response('microblog/home.html',{
            'session':request.session,
            'friendlist':friendlist,
            'error':error,
            'userinfo':user})
        #return HttpResponseRedirect('/home/1/')
    else:
        return HttpResponseRedirect('/')

def ssdetail(request,ssid):
    if request.session:
        userinfo=User.objects.get(id=request.session['userid'])
        shuoshuo=get_object_or_404(Shuoshuo,id=ssid)
        return render_to_response('microblog/shuoshuodetail.html',{
            #'userinfo':userinfo,
            'session':request.session,
            'shuoshuo':shuoshuo,
        })
    else:
        return HttpResponseRedirect('/')

def ssdelete(ssid):
    shuoshuo=get_object_or_404(Shuoshuo,id=ssid)
    shuoshuo.delete()

def addfriend(userinfo,username):
    friend=User.objects.get(username=username)
    userinfo.friend.add(friend)

def deletefriend(userinfo,username):
    friend=User.objects.get(username=username)
    userinfo.friend.remove(friend)

def systeminfo(request,way,param):
    if request.session:
        userinfo=User.objects.get(id=request.session['userid'])
        friendlist=userinfo.friend.all()
        message=""
        if way=="follow":
            addfriend(userinfo,param)
            message=u"你选择关注了"+param+u"同学！"
        if way=="unfollow":
            deletefriend(userinfo,param)
            message=u"你选择放弃关注"+param+u"同学！"
        if way=="delshuoshuo":
            ssdelete(param)
            message=u"你自己的说说已经成功删除了！"
        return render_to_response('microblog/systeminfo.html',{
            'session':request.session,
            'message':message,
            'userinfo':userinfo,
            'friendlist':friendlist,
        })
    else:
        return HttpResponseRedirect('/')














# -*- coding:utf-8 -*-
from django.core.mail import send_mail

FROM_MAIL='MiniMicroBlog@163.com'
MAIL_FOOT=u'''
<br/><br/><br/>
MiniMicroBlog BETA版
<br/>
<a href="http://www.xsank.com">xsank.com</a>
'''

def sendRegistSuccessMail(info):
    subject=u'注册成功'
    body=u'''
    你好！<b>%s</b><br />
    恭喜你，注册成功！<br />
    以下是你的注册信息，请注意保护！<br />
    <ul>
        <li>用户名：%s</li>
        <li>密码：%s</li>
    </ul>
    ''' % (info['realname'],info['username'],info['password'])
    recipient_list=[info['email']]
    send(subject,body,recipient_list)

def send(subject,body,recipient_list):
    body+=MAIL_FOOT
    send_mail(subject,body,FROM_MAIL,recipient_list,fail_silently=True)

def run(request):
    sendRegistSuccessMail(
        {
            'username':'xsank',
            'password':'123123',
            'email':'MiniMicroBlog@163.com',
            'realname':'xsank',
        }
    )

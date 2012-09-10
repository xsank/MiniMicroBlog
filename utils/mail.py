# -*- coding:utf-8 -*-

from django.core.mail import send_mail

FROM_EMAIL='minisns@sina.com'

MAIL_FOOT=u'''

来自xsank菜鸟

http://minisns.sinaapp.com
'''

def send_mail_password(userinfo,newpwd):
    subject=u'你的密码，请保密！'
    body=u'''
    你好，我们通过你的邮箱将新的密码发送给你，请查收！

        你的用户名：%s
        你的新密码：%s

    请妥善保管你的密码，防止别人使用！
    ''' % (userinfo.username,newpwd)
    recipient_list=[userinfo.email]
    send(subject,body,recipient_list)

def send(subject,body,recipient_list):
    body+=MAIL_FOOT
    send_mail(subject,body,FROM_EMAIL,recipient_list,fail_silently=False)

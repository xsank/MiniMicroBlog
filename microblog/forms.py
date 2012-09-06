#-*- coding:utf-8 -*-

from django import  forms
from captcha.fields import CaptchaField
from microblog.models import User
from utils import encrypt
import re

class RegistForm(forms.Form):
    username=forms.CharField(max_length=20,label=('昵称(必填)'),required=True)
    realname=forms.CharField(max_length=20,label=('真实姓名(必填)'),required=True)
    email=forms.EmailField(label=('邮箱(必填)'),required=True)
    password=forms.CharField(label='密码',widget=forms.PasswordInput(),required=True)
    checkpassword=forms.CharField(label='确认密码',widget=forms.PasswordInput(),required=True)

    def clean_username(self):
        username=self.cleaned_data['username']
        if not re.search(r'^\w+$',username):
            raise forms.ValidationError(u'用户名只能包含字母数字和下划线！')
        if User.objects.filter(username=username):
            raise forms.ValidationError(u'用户名已经存在！')
        return username

    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError(u'此邮箱已注册！')
        return email

    def clean_checkpassword(self):
        password=self.cleaned_data.get('password',None)
        checkpassword=self.cleaned_data.get('checkpassword',None)
        pwdlength=len(password)
        if pwdlength < 6:
            raise forms.ValidationError(u'密码不能少于6位！')
        if password!=checkpassword:
            raise forms.ValidationError(u'密码不匹配！')
        return password


class LoginForm(forms.Form):
    username=forms.CharField(max_length=20,label=('用户名'),required=True)
    password=forms.CharField(label='密码',widget=forms.PasswordInput(),required=True)

    def clean_username(self):
        username=self.cleaned_data['username']
        if not User.objects.filter(username=username):
            raise forms.ValidationError(u'用户名不存在存在！注册否？')
        return username

    def clean_password(self):
        username=self.cleaned_data.get('username','')
        password=encrypt.encodeMD5(self.cleaned_data['password'])
        if User.objects.filter(username=username):
            if password != User.objects.get(username=username).userpwd:
                raise forms.ValidationError(u'密码错误！')
        return ""


class ChangePwdForm(forms.Form):
    oldpassword=forms.CharField(label='旧密码',widget=forms.PasswordInput(),required=True)
    newpassword=forms.CharField(label='新密码',widget=forms.PasswordInput(),required=True)
    checkpassword=forms.CharField(label='确认密码',widget=forms.PasswordInput(),required=True)

    def clean_data(self):
        oldpassword=self.cleaned_data['oldpassword']
        newpassword=self.cleaned_data['newpassword']
        checkpassword=self.cleaned_data['checkpassword']
        lenpwd=len(newpassword)
        if lenpwd <6:
            raise forms.ValidationError(u'密码不能少于6位！')










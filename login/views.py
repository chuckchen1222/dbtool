# -*- coding: UTF-8 -*-
"""
Author: chzhang@tripadvisor.com
Date: 2019-03-13
Version: 20190313
"""


from django.shortcuts import render,redirect
from . import models
from .forms import UserForm
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.models import User
import ldap 
from logexec.models import ExecLogging


def index(request):
    menus = models.Menu.objects.filter(is_active='True').order_by('id')
    context = {'menus': menus}
    return render(request,'login/index.html',context)


def login(request):
    if request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "Please Check!"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = authenticate(username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = username
                    ExecLogging.objects.create(user=request.session['user_name'], exec_command=json.dumps({ 'user_id': user_id,'login': "logined" }))
                    return redirect('/index/')
                else:
                    message = "Username or Password not correct!"
            except Exception as e:
                print (e)
                message = "User not exist."
        return render(request, 'login/login.html', locals())
 
    login_form = UserForm()
    return render(request, 'login/login.html', locals())
 
def logout(request):
    if not request.session.get('is_login',None):
        return redirect('/index/')
    request.session.flush()
 
    return redirect('/index/')
 

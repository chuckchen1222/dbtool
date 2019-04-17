"""
Author: chzhang@tripadvisor.com
Date: 2019-03-13
Version: 20190324
"""

from django.shortcuts import render,redirect

def isLogin(func_name):
    def wrapper(request,*args,**kwargs):
        if request.session.get('is_login'):
            return func_name(request,*args,**kwargs)
        else:
            return redirect("/user/login/")
    return wrapper
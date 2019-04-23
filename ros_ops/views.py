from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
"""
Author: chzhang@tripadvisor.com
Date: 2019-03-13
Version: 20190411
"""
import urllib.request
from login.functions.islogin import isLogin
from .functions.rosadmin import getAllRosList, getRosStatus, getRosStatusDone, allROSInfo
from logexec.models import ExecLogging
import json
import ssl

@csrf_exempt
@isLogin
def rosList(request):
    error = []
    roslist = getAllRosList()
    if request.method == "POST":
        dbname = request.POST['dbname']
        action = request.POST['exec']
        user=request.session['user_name']
        allros = allROSInfo()
        if user not in ('sli', 'bcui', 'fkang', 'chzhang'):
            error.append('Permission Deny!')
            context = { 'allros': allros, 'roslist': roslist, 'error': error}
            return render(request, 'ros_ops/roslist.html', context)
        if action == 'redump':
            url = 'http://192.168.4.79:5000/ros_dump/%s' % dbname
        elif action == 'restoretobaitu':
            url = 'https://jks01s.daodao.com/view/content-sync/job/ros_restore/buildWithParameters?token=ros_restore&ROS_NAME=%s&RELEASE_TYPE=prerelease' % dbname
        elif action == 'restoretolive':
            url = 'https://jks01s.daodao.com/view/content-sync/job/ros_restore/buildWithParameters?token=ros_restore&ROS_NAME=%s&RELEASE_TYPE=production' % dbname
        ssl._create_default_https_context = ssl._create_unverified_context
        urllib.request.urlopen(url)
        ExecLogging.objects.create(user=request.session['user_name'], exec_command=json.dumps({ 'dbname': dbname, 'action': action }))
        context = { 'allros': allros, 'roslist': roslist, 'error': error }
        return render(request, 'ros_ops/roslist.html', context)

    allros = allROSInfo()
    context = {'roslist':roslist, 'allros': allros, 'error': error }
    return render(request, 'ros_ops/roslist.html', context)

# ajax 刷新
@isLogin
def refreshStatus(request):
    error = []
    roslist = getAllRosList()
    allros = allROSInfo()
    context = {'roslist':roslist, 'allros': allros, 'error': error }
    return render(request, 'ros_ops/listtable.html', context)


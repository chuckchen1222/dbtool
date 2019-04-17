from django.shortcuts import render,redirect

# Create your views here.
"""
Author: chzhang@tripadvisor.com
Date: 2019-03-13
Version: 20190320
"""
from login.functions.islogin import isLogin
from db_ops.models import Host, Database
from .forms import NewServerForms, DropServerForms

@isLogin
def serverList(request):
    serverlist = Host.objects.select_related('dc_id').order_by('dc_id').order_by('id')
    context = {'serverlist': serverlist}
    return render(request, 'server_ops/serverlist.html', context)

@isLogin
def addServer(request):
    error = []
    if request.method == "POST":
        forms = NewServerForms(request.POST)
        if forms.is_valid():
            full_hostname = forms.cleaned_data['full_hostname']
            short_hostname = forms.cleaned_data['short_hostname']
            v_hostname = forms.cleaned_data['v_hostname']
            ip_addr_t = forms.cleaned_data['ip_addr']
            ip_addr = ip_addr_t+'/32'
            vip_addr_t = forms.cleaned_data['vip_addr']
            vip_addr = vip_addr_t+'/32'
            dc_id_id = forms.cleaned_data['dc_id_id']
            Host.objects.create(full_hostname=full_hostname, short_hostname=short_hostname, v_hostname=v_hostname, 
                                ip_addr=ip_addr, vip_addr=vip_addr, dc_id_id=dc_id_id)
            serverlist = Host.objects.select_related('dc_id').order_by('dc_id').order_by('id')
            context = {'serverlist': serverlist, 'addserver': full_hostname}
            return render(request, 'server_ops/serverlist.html' , context)
    forms = NewServerForms()
    return render(request, 'server_ops/serveradd.html', {'forms': forms})

@isLogin
def dropServer(request):
    error = []
    if request.method == "POST":
        forms = DropServerForms(request.POST)
        if forms.is_valid():
            full_hostname = forms.cleaned_data['full_hostname']
            Host.objects.filter(full_hostname=full_hostname).delete()
            serverlist = Host.objects.select_related('dc_id').order_by('dc_id').order_by('id')
            context = {'serverlist': serverlist, 'dropserver': full_hostname}
            return render(request, 'server_ops/serverlist.html' , context)
    forms = DropServerForms()
    return render(request, 'server_ops/serverdrop.html', {'forms': forms})

@isLogin
def serverDBList(request, servername):
    server_v_hostname = Host.objects.filter(short_hostname = servername).values_list("v_hostname")
    dblist = Database.objects.filter(v_hostname = server_v_hostname[0][0]).order_by('dbsize')
    context = { 'servername': server_v_hostname[0][0], 'dblist': dblist }
    return render(request, 'server_ops/serverdblist.html',context)

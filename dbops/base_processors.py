"""
Author: chzhang@tripadvisor.com
Date: 2019-03-13
Version: 20190324
"""
from login.models import Toolsbar,ToolsbarDropDown

def toolsBar(request):
    navbarlist = Toolsbar.objects.filter(is_active='True').order_by('id')
    return {"navbarlist": navbarlist}

def toolsBardropdown(request):
    dropdownlist = ToolsbarDropDown.objects.all().order_by('toolsbar_id_id')
    return { 'dropdownlist': dropdownlist }

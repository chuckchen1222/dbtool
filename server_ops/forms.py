# encoding: utf-8
"""
Author: chzhang@tripadvisor.com
Date: 2019-04-10
Version: 20190410
"""
from django import forms
from django.forms import widgets
from django.forms import fields

class NewServerForms(forms.Form):
    full_hostname = forms.CharField(label="Full Hostname", max_length=128, widget=forms.TextInput())
    short_hostname = forms.CharField(label="Short Hostname", max_length=128, widget=forms.TextInput())
    v_hostname = forms.CharField(label="V Hostname", max_length=128, widget=forms.TextInput())
    ip_addr = forms.CharField(label="IP Addr", max_length=128, widget=forms.TextInput())
    vip_addr = forms.CharField(label="VIP", max_length=128, widget=forms.TextInput())
    dc_id_id = forms.fields.ChoiceField(label="DataCenter" ,choices=[(1,"c"),(2,"t"),(3,"sc"),(4,"mb"),(5,"mc")],widget=forms.widgets.Select)


class DropServerForms(forms.Form):
    full_hostname = forms.CharField(label="Full Hostname", max_length=128, widget=forms.TextInput())
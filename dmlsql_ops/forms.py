# encoding: utf-8
"""
Author: chzhang@tripadvisor.com
Date: 2019-03-27
Version: 20190327
"""
from django import forms
from django.forms import widgets
from django.forms import fields


class liveExecuteDML(forms.Form):
    dbname = forms.CharField(label="DB Name", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sql = forms.CharField(label="SQL", max_length=10000, widget=forms.Textarea(attrs={'cols': 100, 'rows': 20 }))

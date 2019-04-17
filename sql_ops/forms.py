# encoding: utf-8
"""
Author: chzhang@tripadvisor.com
Date: 2019-03-13
Version: 20190313
"""
from django import forms
from django.forms import widgets
from django.forms import fields

class QueryForms(forms.Form):
    dbname = forms.CharField(label="DB name", max_length=128, widget=forms.TextInput())
    env = forms.fields.ChoiceField(label="EVN type",choices=((1, 'Mainline'), (2, 'Baitu'),(3,'livesite')), widget=forms.widgets.RadioSelect)
    sql = forms.CharField(label="SQL", max_length=3000, widget=forms.Textarea(attrs={'cols': 100, 'rows': 3 }))
    is_explain = forms.fields.ChoiceField(label="SQL Explain", choices=((1,"YES"),(0,"NO")), initial=1, widget=forms.widgets.Select)

class OtherQueryForms(forms.Form):
    dbtype = forms.fields.ChoiceField(label="DB Type" ,choices=[(1,"PostgreSQL"),(2,"MySQL"),(3,"MS SQLServer")],widget=forms.widgets.Select)
    hostname = forms.CharField(label="Host Name", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    port = forms.IntegerField(label="Port", min_value=1000,max_value=9999, widget=forms.TextInput(attrs={'class': 'form-control'}))
    dbname = forms.CharField(label="DB Name", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="User Name", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Pass Word", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    sql = forms.CharField(label="SQL", max_length=3000, widget=forms.Textarea(attrs={'cols': 100, 'rows': 3 }))

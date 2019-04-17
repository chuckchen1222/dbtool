# encoding: utf-8
"""
Author: chzhang@tripadvisor.com
Date: 2019-03-27
Version: 20190327
"""
from django import forms
from django.forms import widgets
from django.forms import fields

# required=False

class dbwSchemaChange():
    env = forms.CharField(label="ENV", max_length=128, widget=forms.TextInput())
    dbname = forms.CharField(label="DB name", max_length=128, widget=forms.TextInput())
    sql = forms.CharField(label="SQL", max_length=10000, widget=forms.Textarea(attrs={'cols': 100, 'rows': 3 }))

class TableSyncTrigger():
    env = forms.CharField(label="DB name", max_length=128, widget=forms.TextInput())
    dbname = forms.CharField(label="DB name", max_length=128, widget=forms.TextInput())
    table = forms.CharField(label="DB name", max_length=128, widget=forms.TextInput())

class dbrSchemaChange():
    env = forms.CharField(label="ENV", max_length=128, widget=forms.TextInput())
    dbname = forms.CharField(label="DB name", max_length=128, widget=forms.TextInput())
    sql = forms.CharField(label="SQL", max_length=3000, widget=forms.Textarea(attrs={'cols': 100, 'rows': 3 }))

class rosSchemaChange():
    env = forms.CharField(label="ENV", max_length=128, widget=forms.TextInput())
    dbname = forms.CharField(label="DB name", max_length=128, widget=forms.TextInput())
    sql = forms.CharField(label="SQL", max_length=3000, widget=forms.Textarea(attrs={'cols': 100, 'rows': 3 }))

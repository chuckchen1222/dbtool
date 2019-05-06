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
# env = forms.fields.ChoiceField(label="ENV" ,choices=[(1,"All"),(2,"Just Live"),(3,"Baitu & Dev")],widget=forms.widgets.Select)

class DbwSchemaChange(forms.Form):
    env = forms.fields.ChoiceField(label="ENV" ,choices=[(1,"All"),(2,"Just Live"),(3,"Baitu & Dev")],widget=forms.widgets.Select)
    dbname = forms.CharField(label="DB Name", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sql = forms.CharField(label="SQL", max_length=10000, widget=forms.Textarea(attrs={'cols': 100, 'rows': 20 }))

class TableSyncTrigger(forms.Form):
    dbname = forms.CharField(label="DB Name", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    table = forms.CharField(label="Table Name", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))

class DbrSchemaChange(forms.Form):
    dbname = forms.CharField(label="DB Name", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sql = forms.CharField(label="SQL", max_length=10000, widget=forms.Textarea(attrs={'cols': 100, 'rows': 20 }))

class RosDDSchemaChange(forms.Form):
    env = forms.fields.ChoiceField(label="ENV" ,choices=[(1,"All"),(2,"Just Live"),(3,"Baitu & Dev")],widget=forms.widgets.Select)
    dbname = forms.CharField(label="DB Name", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sql = forms.CharField(label="SQL", max_length=10000, widget=forms.Textarea(attrs={'cols': 100, 'rows': 20 }))

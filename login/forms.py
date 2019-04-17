# encoding: utf-8
"""
Author: chzhang@tripadvisor.com
Date: 2019-03-13
Version: 20190313
"""

from django import forms

class UserForm(forms.Form):
    username = forms.CharField(label="Username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


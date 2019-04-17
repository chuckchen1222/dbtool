# -*- coding: UTF-8 -*-
"""
Author: chzhang@tripadvisor.com
Date: 2019-03-13
Version: 20190314
"""

from django.db import models

# Create your models here.

class User(models.Model):
    '''  '''
 
    gender = (
        ('male','male'),
        ('female','female'),
    )
 
    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32,choices=gender,default='male')
    c_time = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.name
 
    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class Toolsbar(models.Model):
    name = models.CharField(max_length=128,unique=True)
    url = models.CharField(max_length=128,unique=True)
    is_dropdown = models.BooleanField()
    is_active = models.BooleanField()
    comment = models.CharField(max_length=1024,blank=True)

class Menu(models.Model):
    name = models.CharField(max_length=128,unique=True)
    url = models.CharField(max_length=128,unique=True)
    is_active = models.BooleanField()
    comment = models.CharField(max_length=1024,blank=True)

class ToolsbarDropDown(models.Model):
    name = models.CharField(max_length=128,unique=True)
    url = models.CharField(max_length=128,unique=True)
    is_active = models.BooleanField()
    comment = models.CharField(max_length=1024,blank=True)
    toolsbar_id = models.ForeignKey(Toolsbar, on_delete=models.CASCADE)


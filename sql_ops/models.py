# encoding: utf-8
"""
Author: chzhang@tripadvisor.com
Date: 2019-03-13
Version: 20190313
"""

from django.db import models

# Create your models here.

class ExecHistory(models.Model):
    username = models.CharField(max_length=128)
    exec_time = models.DateTimeField()
    exec_query = models.CharField(max_length=2000)
    


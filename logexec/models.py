from django.db import models

from django.contrib.postgres.fields import JSONField

# Create your models here.

"""
Author: chzhang@tripadvisor.com
Date: 2019-03-13
Version: 20190326
"""

class ExecLogging(models.Model):
    user = models.CharField(max_length=256)
    exec_command = JSONField(null=True)
    exec_time = models.DateTimeField(auto_now_add=True)

class HisExecLogging(models.Model):
    user = models.CharField(max_length=256)
    exec_command = JSONField(null=True)
    exec_time = models.DateTimeField()



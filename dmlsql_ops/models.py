from django.db import models

"""
Author: chzhang@tripadvisor.com
Date: 2019-05-07
Version: 20190507
"""

# Create your models here.

class BackupData(models.Model):
    dbname = models.CharField(max_length=256)
    exec_sql = models.TextField()
    back_data = models.TextField(null=True)
    execed_time = models.DateTimeField(auto_now_add=True)
    is_executed = models.BooleanField(default=False, null=True)

class SqlFile(models.Model):
    dbname = models.CharField(max_length=256)
    filename = models.CharField(max_length=512, null=True)
    file_path = models.CharField(max_length=512, null=True)
    is_executed = models.BooleanField(default=False, null=True)
    created_time = models.DateTimeField(auto_now_add=True)

class SqlExecHistory(models.Model):
    dbname = models.CharField(max_length=256)
    execed_sql = models.TextField(null=True)
    sqlfile_id = models.ForeignKey(SqlFile, on_delete=models.CASCADE, null=True)
    is_executed = models.BooleanField(default=False, null=True)
    exec_result = models.TextField(null=True)
    execed_time = models.DateTimeField(auto_now_add=True)
    backupdata_ids = models.TextField(null=True)

from django.db import models

"""
Author: chzhang@tripadvisor.com
Date: 2019-03-13
Version: 20190313
"""

# import DC, Host, DB model for foreign keys.
from db_ops.models import Database

# Create your models here.

class Tables(models.Model):
    table_name = models.CharField(max_length=256)
    schema_name = models.CharField(max_length=256)
    table_size = models.CharField(max_length=256)
    rows_count = models.BigIntegerField()
    sync_trigger = models.BooleanField(default=False, null=True)
    last_analyze = models.CharField(max_length=256, null=True)
    last_vacuum = models.CharField(max_length=256, null=True)
    comment = models.CharField(max_length=1000, null=True)
    db_id = models.ForeignKey(Database, on_delete=models.CASCADE)
    class Meta:
        index_together = ['schema_name', 'table_name', 'db_id']

class Columns(models.Model):
    column_name = models.CharField(max_length=256, null=True)
    column_type = models.CharField(max_length=256, null=True)
    comment = models.CharField(max_length=1000, null=True)
    is_notnull = models.BooleanField(default=False, null=True)
    table_id = models.ForeignKey(Tables, on_delete=models.CASCADE, db_index=True)

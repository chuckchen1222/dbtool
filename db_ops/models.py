from django.db import models

"""
Author: chzhang@tripadvisor.com
Date: 2019-03-13
Version: 20190313
"""

# Create your models here.

class Datacenter(models.Model):
    DCNAME_CHOICES = (
        ('t', 't'),
        ('c', 'c'),
        ('sc','sc'),
        ('mb','mb'),
        ('mc','mc'),
    )

    dcname = models.CharField(max_length=10, choices=DCNAME_CHOICES)
    addr = models.CharField(max_length=128)
    is_live = models.BooleanField(default=False)


class Host(models.Model):
    full_hostname = models.CharField(max_length=256)
    short_hostname = models.CharField(max_length=256)
    v_hostname = models.CharField(max_length=256)
    ip_addr = models.CharField(max_length=18)
    vip_addr = models.CharField(max_length=18)
    dc_id = models.ForeignKey(Datacenter, on_delete=models.CASCADE)
    is_master = models.BooleanField(default=False, null=True)

class Database(models.Model):
    dbname = models.CharField(max_length=256)
    port = models.IntegerField(default=5432)
    dbsize = models.CharField(max_length=256)
    env = models.CharField(max_length=256)
    topology = models.CharField(max_length=256)
    cname = models.CharField(max_length=256, null=True)
    v_hostname = models.CharField(max_length=256)
    is_pgsync = models.BooleanField()
    pgsync_mode = models.CharField(max_length=256, null=True)


class Pgsync(models.Model):
    dbname = models.CharField(max_length=256)
    master_db_id = models.ForeignKey(Database, on_delete=models.CASCADE, related_name="master_db_id")
    slave_db_id = models.ForeignKey(Database, on_delete=models.CASCADE, related_name="slave_db_id")

class BackupInfo(models.Model):
    dbname = models.CharField(max_length=256)
    backupdir = models.CharField(max_length=256)
    backupdate = models.DateField()



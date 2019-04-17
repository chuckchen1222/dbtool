"""dbops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

"""
Author: chzhang@tripadvisor.com
Date: 2019-03-13
Version: 20190327
"""


from django.contrib import admin
from django.urls import path, include

from login import views as login_views
from db_ops import views as db_views
from sql_ops import views as sql_views
from server_ops import views as server_views
from table_ops import views as table_views
from ros_ops import views as ros_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'index/', login_views.index),
    path(r'user/login/', login_views.login),
    path(r'user/logout/', login_views.logout),
    path(r'db_ops/dblist/', db_views.dbList),
    path(r'db_ops/tablelist/<servername>/<dbname>/', db_views.DBTableList),
    path(r'sql/ddquery/', sql_views.query),
    path(r'sql/otherquery/', sql_views.otherDBQuery),
    path(r'server_ops/serverlist/',server_views.serverList),
    path(r'server_ops/serveradd/',server_views.addServer),
    path(r'server_ops/serverdrop/',server_views.dropServer),
    path(r'server_ops/dblist/<servername>/', server_views.serverDBList),
    path(r'table_ops/<servername>/<dbname>/<tablename>/', table_views.tableColList),
    path(r'table_ops/tablesearch/', table_views.tableSearch),
    path(r'table_ops/tablelist/', table_views.tableList),
    path(r'ros_ops/admin/', ros_views.rosList),
    path(r'ros_ops/admin/refreshstatus/', ros_views.refreshStatus),
]

Applications:
login:


server_ops:
1. server列表
2. server增删
3. Server - DB 列表


db_ops:
1. DB列表
2. DB - Table 列表

table_ops:
1. 搜索表

sql_ops:
1. 查询DD数据库
2. 查询其他数据库(PG, MySQL, MS SQL Server)

ros_ops:
1. ros DB列表
2. 操作。调用sync01s中的dump_ros_api 和 jks01s中的 restore ros

schema_ops:
1. 执行schema change

dml_ops:
1. 对线上dbw环境执行 dml操作。
SQL语句 or 文件

logexec:
1. 操作日志（登录，操作，SQL query，Change）

other dir:
libs: 
init: 数据库初始化SQL（menu，toolbar，dropdown）



启动: 
增加 --insecure参数, 否则无法读取到static文件。
python manage.py runserver 0.0.0.0:5000 --insecure >> /root/dbtool_log/dbtool.log 2>&1 &

部署:
Nginx + uwsgi
0. Prepare
关闭防火墙
setenforce 0
vim /etc/selinux/config 
SELINUX = disabled

systemctl stop firewalld
systemctl diable firewalld

(
ufw status
ufw disable
)

1. 安装
yum -y install epel-release python-devel nginx
pip install supervisor uwsgi

2.
vim /etc/supervisord.conf
#######################
[supervisord]
logfile = /tmp/supervisord.log
logfile_maxbytes = 50MB
logfile_backups=10
loglevel = info
pidfile = /tmp/supervisord.pid
nodaemon = false
minfds = 1024
minprocs = 200
umask = 022
user = root
identifier = supervisor
directory = /tmp
nocleanup = true
childlogdir = /tmp
strip_ansi = false
environment = KEY1="value1",KEY2="value2"

[supervisorctl]
logfile = /tmp/supervisord.log
logfile_maxbytes = 50MB
logfile_backups=10
loglevel = info
pidfile = /tmp/supervisord.pid
nodaemon = false
minfds = 1024
minprocs = 200
umask = 022
user = root
identifier = supervisor
directory = /tmp
nocleanup = true
childlogdir = /tmp
strip_ansi = false
environment = KEY1="value1",KEY2="value2"

[program:dbops]
command=/usr/python/bin/uwsgi --ini /home/site/dbops/uwsgi.ini
directory=/home/site/dbops
startsecs=0
stopwaitsecs=0
autostart=true
autorestart=true
stderr_logfile=/var/log/supervisord_dbops.err.log
stdout_logfile=/var/log/supervisord_dbops.out.log

#######################
/usr/python/bin/supervisord -c /etc/supervisord.conf

3. 
vim /etc/nginx/nginx.conf
# 改user
user root; 
# 新加如下内容
    upstream django{
        server 127.0.0.1:8001;
    }

    server {
        listen        5000;
        # 访问域名
        server_name   dbtool.test.com;
        charset       urf-8;
        client_max_body_size    75M;
        location /static{
            alias /home/site/dbops/static;
        }
        location / {
            uwsgi_pass  127.0.0.1:8001;
            include     /etc/nginx/uwsgi_params;
        }
    }

service nginx restart

4. 
访问dbtool.test.com:5000/index/
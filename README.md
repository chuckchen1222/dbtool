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

启动: 
增加 --insecure参数, 否则无法读取到static文件。
python manage.py runserver 0.0.0.0:5000 --insecure >> /root/dbtool_log/dbtool.log 2>&1 &


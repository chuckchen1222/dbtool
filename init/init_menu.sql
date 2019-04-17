--login_menu;
insert into login_menu values ( 2, 'DB Server','/server_ops/serverlist/','t','live');
insert into login_menu values ( 3, 'Database','/db_ops/dblist/','t','live');
insert into login_menu values ( 4, 'Table Search','/table_ops/tablesearch/','t','live');
insert into login_menu values ( 5, 'SQL Query','/sql/ddquery/','t','live');
insert into login_menu values ( 6, 'ROS ADMIN','/ros_ops/admin/','t','live');
insert into login_menu values (11, 'Schema Change','../test/SchemaChange','f','test');


--login_toolsbar;
insert into login_toolsbar values ( 2,'DB Server','/server_ops/serverlist/','f','t','live');
insert into login_toolsbar values ( 3,'Database','/db_ops/dblist/','f','t','live');
insert into login_toolsbar values ( 4,'Table Search','/table_ops/tablesearch/','f','t','live');
insert into login_toolsbar values ( 5,'SQL Query','/sql/ddquery/','t','t','live');
insert into login_toolsbar values ( 6,'ROS ADMIN','/ros_ops/admin/','f','t','live');
insert into login_toolsbar values (11,'Schema Change','../test/SchemaChange','f','f','test');


--login_toolsbardropdown;
insert into login_toolsbardropdown values (1,'Query DaoDao DB','/sql/ddquery/','t','test','5');
insert into login_toolsbardropdown values (2,'Query Any DB','/sql/otherquery/','t','test','5');

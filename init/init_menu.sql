--login_menu;
insert into login_menu values ( 2, 'DB Server','/server_ops/serverlist/','t','live');
insert into login_menu values ( 3, 'Database','/db_ops/dblist/','t','live');
insert into login_menu values ( 4, 'Table Search','/table_ops/tablesearch/','t','live');
insert into login_menu values ( 5, 'SQL Query','/sql/ddquery/','t','live');
insert into login_menu values ( 6, 'ROS ADMIN','/ros_ops/admin/','t','live');
insert into login_menu values (11, 'Schema Change','/schema_ops/dbwschemachange/','f','test');


--login_toolsbar;
insert into login_toolsbar values ( 2,'DB Server','/server_ops/serverlist/','f','t','live');
insert into login_toolsbar values ( 3,'Database','/db_ops/dblist/','f','t','live');
insert into login_toolsbar values ( 4,'Table Search','/table_ops/tablesearch/','f','t','live');
insert into login_toolsbar values ( 5,'SQL Query','/sql/ddquery/','t','t','live');
insert into login_toolsbar values ( 6,'ROS ADMIN','/ros_ops/admin/','f','t','live');
insert into login_toolsbar values (11,'Schema Change','/schema_ops/dbwschemachange/','t','t','test');


--login_toolsbardropdown;
insert into login_toolsbardropdown values (1,'Query DaoDao DB','/sql/ddquery/','t','live','5');
insert into login_toolsbardropdown values (2,'Query Any DB','/sql/otherquery/','t','live','5');
insert into login_toolsbardropdown values (3,'DBW Schema Change','/schema_ops/dbwschemachange/','t','live','11');
insert into login_toolsbardropdown values (4,'Create Sync Trigger','/schema_ops/createtablesynctrigger/','t','live','11');
insert into login_toolsbardropdown values (5,'DBR Schema Change','/schema_ops/dbrschemachange/','t','test','11');
insert into login_toolsbardropdown values (6,'DD ROS Schema Change','/schema_ops/rosddschemachange/','t','test','11');



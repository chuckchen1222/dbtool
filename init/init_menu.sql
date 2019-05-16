--login_menu;
insert into login_menu values ( 2, 'DB Server','/server_ops/serverlist/','t','live');
insert into login_menu values ( 3, 'Database','/db_ops/dblist/','t','live');
insert into login_menu values ( 4, 'Table Search','/table_ops/tablesearch/','t','live');
insert into login_menu values ( 5, 'SQL Query','/sql/ddquery/','t','live');
insert into login_menu values ( 6, 'ROS ADMIN','/ros_ops/admin/','t','live');
insert into login_menu values (11, 'Schema Change','/schema_ops/dbwschemachange/','f','live');
insert into login_menu values (12,'DML in Live','/dmlsql_ops/liveexecdml/','t','live');
insert into login_menu values (21,'Monitor PGSync Lag','http://monitor03c:3000/d/JbNUiOsmz/db-my-pgsync-lag-overview?refresh=5s&orgId=1',
                            't','live and jump to grafana');


--login_toolsbar;
insert into login_toolsbar values ( 2,'DB Server','/server_ops/serverlist/','f','t','live');
insert into login_toolsbar values ( 3,'Database','/db_ops/dblist/','f','t','live');
insert into login_toolsbar values ( 4,'Table Search','/table_ops/tablesearch/','f','t','live');
insert into login_toolsbar values ( 5,'SQL Query','/sql/ddquery/','t','t','live');
insert into login_toolsbar values ( 6,'ROS ADMIN','/ros_ops/admin/','f','t','live');
insert into login_toolsbar values (11,'Schema Change','/schema_ops/dbwschemachange/','t','t','live');
insert into login_toolsbar values (12,'DML in Live','/dmlsql_ops/liveexecdml/','t','t','live');

--login_toolsbardropdown;
insert into login_toolsbardropdown values (1,'Query DaoDao DB','/sql/ddquery/','t','live','5');
insert into login_toolsbardropdown values (2,'Query Any DB','/sql/otherquery/','t','live','5');
insert into login_toolsbardropdown values (3,'DBW Schema Change','/schema_ops/dbwschemachange/','t','live','11');
insert into login_toolsbardropdown values (4,'Create Sync Trigger','/schema_ops/createtablesynctrigger/','t','live','11');
insert into login_toolsbardropdown values (5,'DBR Schema Change','/schema_ops/dbrschemachange/','f','test','11');
insert into login_toolsbardropdown values (6,'DD ROS Schema Change','/schema_ops/rosddschemachange/','f','test','11');
insert into login_toolsbardropdown values (7, 'Exec DML SQL','/dmlsql_ops/liveexecdml/','t','live',12);
insert into login_toolsbardropdown values (8, 'Exec DML SQL FILE','/dmlsql_ops/liveexecdmlfile/','t','live',12);

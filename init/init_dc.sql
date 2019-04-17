--select 'insert into db_ops_datacenter values (' || id || ',''' || dcname || ''',''' || addr|| ''',''' || is_live || ''');' from db_ops_datacenter order by id;

 insert into db_ops_datacenter values (1,'c','Tianjin','true');
 insert into db_ops_datacenter values (2,'t','Yanjiao','false');
 insert into db_ops_datacenter values (3,'s','Support Cage','false');
 insert into db_ops_datacenter values (4,'mb','Mini Beijing','false');
 insert into db_ops_datacenter values (5,'mc','Mini China','false');
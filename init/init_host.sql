--select 'insert into db_ops_host values (' || id || ',''' || full_hostname || ''',''' ||  short_hostname || ''',''' || v_hostname || ''',''' || ip_addr || ''',''' || vip_addr || ''',''' || is_master || ''',''' || dc_id_id || ''');' from db_ops_host order by id;

 insert into db_ops_host values (1,'dbw01ac.daodao.com','dbw01ac','dbw01c','192.168.1.143/32','192.168.1.149/32','true','1');
 insert into db_ops_host values (2,'dbw01bc.daodao.com','dbw01bc','dbw01c','192.168.1.144/32','192.168.1.149/32','false','1');
 insert into db_ops_host values (3,'dbw02ac.daodao.com','dbw02ac','dbw02c','192.168.1.145/32','192.168.1.147/32','true','1');
 insert into db_ops_host values (4,'dbw02bc.daodao.com','dbw02bc','dbw02c','192.168.1.146/32','192.168.1.147/32','false','1');
 insert into db_ops_host values (5,'dbw03ac.daodao.com','dbw03ac','dbw03c','192.168.1.169/32','192.168.1.176/32','true','1');
 insert into db_ops_host values (6,'dbw03bc.daodao.com','dbw03bc','dbw03c','192.168.1.170/32','192.168.1.176/32','false','1');
 insert into db_ops_host values (7,'dbw04ac.daodao.com','dbw04ac','dbw04c','192.168.1.177/32','192.168.1.179/32','false','1');
 insert into db_ops_host values (8,'dbw04bc.daodao.com','dbw04bc','dbw04c','192.168.1.178/32','192.168.1.179/32','false','1');
 insert into db_ops_host values (9,'dbw05ac.daodao.com','dbw05ac','dbw05c','192.168.1.203/32','192.168.1.205/32','true','1');
 insert into db_ops_host values (10,'dbw05bc.daodao.com','dbw05bc','dbw05c','192.168.1.204/32','192.168.1.205/32','false','1');
 insert into db_ops_host values (11,'dbw06ac.daodao.com','dbw06ac','dbw06c','192.168.1.157/32','192.168.1.159/32','true','1');
 insert into db_ops_host values (12,'dbw06bc.daodao.com','dbw06bc','dbw06c','192.168.1.158/32','192.168.1.159/32','false','1');
 insert into db_ops_host values (13,'dbr01c.daodao.com','dbr01c','dbr01c','192.168.1.203/32','192.168.5.140/32','true','1');
 insert into db_ops_host values (14,'dbr02c.daodao.com','dbr02c','dbr02c','192.168.1.204/32','192.168.5.140/32','true','1');
 insert into db_ops_host values (15,'dbw01at.daodao.com','dbw01at','dbw01t','192.168.13.53/32','192.168.13.55/32','true','2');
 insert into db_ops_host values (16,'dbw01bt.daodao.com','dbw01bt','dbw01t','192.168.13.54/32','192.168.13.55/32','false','2');
 insert into db_ops_host values (17,'dbw02at.daodao.com','dbw02at','dbw02t','192.168.13.56/32','192.168.13.58/32','true','2');
 insert into db_ops_host values (18,'dbw02bt.daodao.com','dbw02bt','dbw02t','192.168.13.57/32','192.168.13.58/32','false','2');
 insert into db_ops_host values (19,'dbw03at.daodao.com','dbw03at','dbw03t','192.168.13.59/32','192.168.13.61/32','true','2');
 insert into db_ops_host values (20,'dbw03bt.daodao.com','dbw03bt','dbw03t','192.168.13.60/32','192.168.13.61/32','false','2');
 insert into db_ops_host values (21,'dbw04at.daodao.com','dbw04at','dbw04t','192.168.13.90/32','192.168.13.92/32','false','2');
 insert into db_ops_host values (22,'dbw04bt.daodao.com','dbw04bt','dbw04t','192.168.13.91/32','192.168.13.92/32','false','2');
 insert into db_ops_host values (23,'dbw05at.daodao.com','dbw05at','dbw05t','192.168.13.153/32','192.168.13.157/32','true','2');
 insert into db_ops_host values (24,'dbw05bt.daodao.com','dbw05bt','dbw05t','192.168.13.154/32','192.168.13.157/32','false','2');
 insert into db_ops_host values (25,'dbw06at.daodao.com','dbw06at','dbw06t','192.168.13.170/32','192.168.13.172/32','true','2');
 insert into db_ops_host values (26,'dbw06bt.daodao.com','dbw06bt','dbw06t','192.168.13.171/32','192.168.13.172/32','false','2');
 insert into db_ops_host values (27,'dbr01t.daodao.com','dbr01t ','dbr01t','192.168.13.51/32','192.168.13.51/32','true','2');
 insert into db_ops_host values (28,'dbr02t.daodao.com','dbr02t ','dbr02t','192.168.13.52/32','192.168.13.51/32','true','2');
 insert into db_ops_host values (29,'rivendellac.daodao.com','rivendellac','rivendell','192.168.4.43/32','192.168.4.87/32','true','3');
 insert into db_ops_host values (30,'rivendellbc.daodao.com','rivendellbc','rivendell','192.168.4.44/32','192.168.4.87/32','false','3');
 insert into db_ops_host values (31,'tm01ac.daodao.com','tm01ac','tm01c','192.168.4.182/32','192.168.4.14/32','true','3');
 insert into db_ops_host values (32,'tm01bc.daodao.com','tm01bc','tm01c','192.168.4.183/32','192.168.4.14/32','false','3');
 insert into db_ops_host values (33,'tm04ac.daodao.com','tm04ac','tm04c','192.168.4.50/32','192.168.4.153/32','true','3');
 insert into db_ops_host values (34,'tm04bc.daodao.com','tm04bc','tm04c','192.168.4.147/32','192.168.4.153/32','false','3');
 insert into db_ops_host values (35,'syncdb01c.daodao.com','syncdb01c','syncdb01c','192.168.4.19/32','192.168.4.132/32','true','3');
 insert into db_ops_host values (36,'sync03s.daodao.com','sync03s  ','sync03s','192.168.4.142/32','192.168.4.142/32','false','3');
 insert into db_ops_host values (37,'dbwvm01as.daodao.com','dbwvm01as','dbwvm01s','192.168.4.56/32','192.168.4.51/32','true','3');
 insert into db_ops_host values (38,'dbwvm01bs.daodao.com','dbwvm01bs','dbwvm01s','192.168.4.57/32','192.168.4.51/32','false','3');
 insert into db_ops_host values (39,'dbwvm02as.daodao.com','dbwvm02as','dbwvm02s','192.168.4.73/32','192.168.4.75/32','true','3');
 insert into db_ops_host values (40,'dbwvm02bs.daodao.com','dbwvm02bs','dbwvm02s','192.168.4.74/32','192.168.4.75/32','false','3');
 insert into db_ops_host values (41,'dbwvm03as.daodao.com','dbwvm03as','dbwvm03s','192.168.4.228/32','192.168.4.230/32','true','3');
 insert into db_ops_host values (42,'dbwvm03bs.daodao.com','dbwvm03bs','dbwvm03s','192.168.4.229/32','192.168.4.230/32','false','3');
 insert into db_ops_host values (43,'dbwvm04as.daodao.com','dbwvm04as','dbwvm04as','192.168.3.53/32','192.168.3.53/32','true','3');
 insert into db_ops_host values (47,'rtdb01s.daodao.com','rtdb01s','rtdb01s','192.168.4.158/32','192.168.4.158/32','true','3');
 insert into db_ops_host values (48,'dbw01as.daodao.com','dbw01as','dbw01s','192.168.4.32/32','192.168.4.60/32','true','3');
 insert into db_ops_host values (49,'dbw02as.daodao.com','dbw02as','dbw02s','192.168.4.246/32','192.168.4.131/32','true','3');
 insert into db_ops_host values (50,'dbw01mb.daodao.com','dbw01mb','dbw01mb','10.135.33.76/32','10.135.33.76/32','true','4');
 insert into db_ops_host values (51,'dbr01mb.daodao.com','dbr01mb','dbr01mb','10.135.33.75/32','10.135.33.75/32','true','4');
 insert into db_ops_host values (53,'dbr01mc.daodao.com','dbr01mc','dbr01mc','10.11.26.68/32','10.11.26.68/32','true','5');
 insert into db_ops_host values (54,'dbw01mc.daodao.com','dbw01mc','dbw01mc','10.11.26.66/32','10.11.26.66/32','false','5');
 insert into db_ops_host values (55,'dbros01as.daodao.com','dbros01as','dbros01s','192.168.4.120/32','192.168.4.249/32','true','3');
 insert into db_ops_host values (56,'dbros01bs.daodao.com','dbros01bs','dbros01s','192.168.4.66/32','192.168.4.249/32','false','3');
 insert into db_ops_host values (59,'dbw03s.daodao.com','dbw03as','dbw03s','192.168.4.245/32','192.168.4.138/32','true','3');
 insert into db_ops_host values (60,'dbw01bs.daodao.com','dbw01bs','dbw01s','192.168.4.250/32','192.168.4.60/32','false','3');
 insert into db_ops_host values (61,'dbw02bs.daodao.com','dbw02bs','dbw02s','192.168.4.237/32','192.168.4.131/32','false','3');
 insert into db_ops_host values (62,'tm01s.daodao.com','tm01s','tm01s','192.168.4.130/32','192.168.4.130/32','true','3');
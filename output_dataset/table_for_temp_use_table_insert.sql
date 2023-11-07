
-- Oracle: table <table_for_temp_use>: sql table insertion commands from row 1 to row 6
-- Oracle: 表 <table_for_temp_use>: 从第1条数据到第6条数据的插入语句
INSERT INTO table_for_temp_use (TABLE_AFFILIATION,YEAR,TRAN_NUMBER,REMARK) 
VALUES('西北','2003','1233','原始');
INSERT INTO table_for_temp_use (TABLE_AFFILIATION,YEAR,TRAN_NUMBER,REMARK) 
VALUES('西北','2005','2343','现代');
INSERT INTO table_for_temp_use (TABLE_AFFILIATION,YEAR,TRAN_NUMBER,REMARK) 
VALUES('西北','2004','3212','转变');
INSERT INTO table_for_temp_use (TABLE_AFFILIATION,YEAR,TRAN_NUMBER,REMARK) 
VALUES('西南','2003','1233','原始');
INSERT INTO table_for_temp_use (TABLE_AFFILIATION,YEAR,TRAN_NUMBER,REMARK) 
VALUES('西南','2005','2343','现代');
INSERT INTO table_for_temp_use (TABLE_AFFILIATION,YEAR,TRAN_NUMBER,REMARK) 
VALUES('西南','2004','3212','转变');
COMMIT;

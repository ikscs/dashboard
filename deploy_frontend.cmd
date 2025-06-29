@echo on

SET SERV_USER=yuriy
SET SERVER=172.16.10.72
SET SRC=dashboard\dist\
SET DST=/opt/ikscs/api4_dashboard/ 

scp -r %SRC%/* %SERV_USER%@%SERVER%:%DST%



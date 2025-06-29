@echo on

SET SERV_USER=yuriy
SET SERVER=172.16.10.72
SET SRC=backend
SET DST=/opt/docker/django/app

scp -r %SRC%/* %SERV_USER%@%SERVER%:%DST%

ssh %SERV_USER%@%SERVER% "docker restart django_app"



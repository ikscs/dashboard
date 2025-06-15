rem npm run build

@echo on

SET SERV_USER=yuriy
SET SERVER=188.93.118.18
SET SRC=dist
SET DST=hr

SET DST=/opt/ikscs/react1/dist/%DST%

powershell -Command "(gc dist/index.html) -replace '/assets/', 'assets/' | Out-File -encoding ASCII dist/index.html"

ssh %SERV_USER%@%SERVER% "mkdir -p %DST% && rm -r %DST%/*"
scp -r %SRC%/* %SERV_USER%@%SERVER%:%DST%

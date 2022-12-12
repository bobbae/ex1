
## server

Invoke-WebRequest -Uri "https://dl.min.io/server/minio/release/windows-amd64/minio.exe" -OutFile "minio.exe"
setx MINIO_ROOT_USER admin
setx MINIO_ROOT_PASSWORD password
mkdir data
.\minio.exe server .\Data --console-address ":9001"

## client

Invoke-WebRequest -Uri "https://dl.minio.io/client/mc/release/windows-amd64/mc.exe" -OutFile "mc.exe"
.\mc.exe alias set myminio/ http://MINIO-SERVER MYUSER MYPASSWORD

.\mc admin info myminio
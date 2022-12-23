https://courses.cs.washington.edu/courses/csep544/11au/resources/postgresql-instructions.html

create user 'user';
alter user "user" with superuser;
alter user "user" with createrole;
alter user "user" with createdb;
alter user "user" with replication;
alter user "user" with bypassrls;

\du;

create database nms;

# psql -U user nms
POSTGRES_USER=user
POSTGRES_PASSWORD=pass
POSTGRES_DB=nms

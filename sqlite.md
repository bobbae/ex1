## Export to CSV

```

sqlite3 chinook.db
sqlite> .headers on
sqlite> .mode csv
sqlite> .output data.csv
sqlite> SELECT customerid,
   ...>        firstname,
   ...>        lastname,
   ...>        company
   ...>   FROM customers;
sqlite> .quit

```

## Shell script

```
#!/bin/bash
sqlite3 chinook.db <<EOF
.headers on
.mode csv
.output customers.csv
select * from customers;
.quit
EOF
```

## Import into Postgres

```


From SqliteStudio find DDL for tables. 
Or sqlite3 CLI use --> .schema tableName;
Then modify to create tables in Psql.


CREATE TABLE albums (
    AlbumId  INTEGER        PRIMARY KEY 
                            NOT NULL,
    Title    VARCHAR (160) NOT NULL,
    ArtistId INTEGER        NOT NULL,
    FOREIGN KEY (
        ArtistId
    )
    REFERENCES artists (ArtistId) ON DELETE NO ACTION
                                  ON UPDATE NO ACTION
);

CREATE TABLE artists (
    ArtistId INTEGER        PRIMARY KEY 
                            NOT NULL,
    Name     VARCHAR (120) 
);




COPY artists(ArtistId, Name)
FROM 'C:\sqlite\artists.csv'
DELIMITER ','
CSV HEADER;

COPY artists2(ArtistId, Name)
FROM 'C:\sqlite\artists.csv'
DELIMITER ','
CSV HEADER;

COPY albums(AlbumId, Title, ArtistId)
FROM 'C:\sqlite\albums.csv'
DELIMITER ','
CSV HEADER;

```


## command line
```
sqlite3 -header -csv chinook.db "select * from artists;" > artists.csv

```


## The problem
We use a docker container based on a postgresql 
([3dcitydb-docker-postgis](https://github.com/tum-gis/3dcitydb-docker-postgis/tree/master/v4.0.2) that is [based on](https://github.com/tum-gis/3dcitydb-docker-postgis/blob/master/v4.0.2/Dockerfile#L7) the 
[standard postgres container](https://hub.docker.com/_/postgres/)).
When the container is stoped and then restarted the database is temporarily
(and sometimes definitively) not available.

### Some wrong clues
This unavailibility manifests itself in various forms dependending on the client
that tries to access the database.
For example the error message will sometimes be (refer below) 
```
Connection to 134.214.143.170:5432 refused. Check that the hostname and port are
correct and that the postmaster is accepting TCP/IP connections
```
which might suggest that some pesky firewall gets in the way or that de
containerized database was not launched at all.

Yet it is easy to check that the problem is not of this nature and is not at 
IP/port connectivity level by doing e.g.
```
docker run -v `pwd`/:/InputConfig -it --entrypoint /bin/bash tumgis/3dcitydb-impexp:4.2.3

apt-get update
apt-get install postgresql postgresql-contrib
psql -h 134.214.143.170 -p 5432 -U postgres -d citydb-full_lyon-2009 -c "\dt"
# provide postgres as password
.... 
# and you will get some answer from the database
```
thus proving that the database server can be contacted.


### Further problem illustration with tumgis/3dcitydb-impexp:4.2.3 as client

The following single call suffices to reproduce the error:
```
docker run -v `pwd`/:/InputConfig -v `pwd`/junk/LYON_2009_Stripped:/InputFiles -it tumgis/3dcitydb-impexp:4.2.3 -config /InputConfig/3dCityDBImpExpConfig2009.xml -import /InputFiles/LYON_1ER_BATI_2009_splited_stripped.gml
```

The logged error messages differ according to the "history" of the database
container (previously launched or not) and its invocation context (database
files mounted from host or within the container):
  - just to make sure notice that when the database is indeed not launched at all 
    then one gets the **correct** error message which is
    ```
    org.citydb.ImpExpException: Connection to database could not be established.
    [...]
    Caused by: org.postgresql.util.PSQLException:
      Connection to 134.214.143.170:5432 refused. Check that the hostname and port are
      correct and that the postmaster is accepting TCP/IP connections
    ```
  - when the database was previously launched, then stopped (thus producing
    an `<output>/postgres-data/` directory) and then restarted then one gets
    two possible error messages. The first one goes
    ```
    org.citydb.ImpExpException: Connection to database could not be established.
    [...]
    Caused by: org.postgresql.util.PSQLException: FATAL: the database system is starting up
    ```
    and then second one is
    ```
    org.citydb.ImpExpException: Connection to database could not be established.
    [...]
    Caused by: java.sql.SQLException: Failed to retrieve version information from
              the 3D City Database instance.
    [...]
    Caused by: org.postgresql.util.PSQLException: ERROR: schema "citydb_pkg" does not exist
    ```
- when `<output>/postgres-data/` directory does NOT exist then one gets
  ```
  org.citydb.ImpExpException: Connection to database could not be established.
  org.citydb.cli.ImpExpCli.initDBPool(ImpExpCli.java:304)
  org.citydb.cli.ImpExpCli.doImport(ImpExpCli.java:90)
  org.citydb.ImpExp.doMain(ImpExp.java:552)
  org.citydb.ImpExp.main(ImpExp.java:153)
  Caused by:
      org.postgresql.util.PSQLException: The connection attempt failed.
      org.postgresql.core.v3.ConnectionFactoryImpl.openConnectionImpl(ConnectionFactoryImpl.java:297)
      org.postgresql.core.ConnectionFactory.openConnection(ConnectionFactory.java:49)
      org.postgresql.jdbc.PgConnection.<init>(PgConnection.java:217)
      org.postgresql.Driver.makeConnection(Driver.java:458)
      org.postgresql.Driver.connect(Driver.java:260)
      org.apache.tomcat.jdbc.pool.PooledConnection.connectUsingDriver(PooledConnection.java:319)
      org.apache.tomcat.jdbc.pool.PooledConnection.connect(PooledConnection.java:212)
      org.apache.tomcat.jdbc.pool.ConnectionPool.createConnection(ConnectionPool.java:744)
      org.apache.tomcat.jdbc.pool.ConnectionPool.borrowConnection(ConnectionPool.java:676)
      org.apache.tomcat.jdbc.pool.ConnectionPool.getConnection(ConnectionPool.java:198)
      org.apache.tomcat.jdbc.pool.DataSourceProxy.getConnection(DataSourceProxy.java:132)
      org.citydb.database.connection.DatabaseConnectionPool.getConnection(DatabaseConnectionPool.java:200)
      org.citydb.database.adapter.AbstractUtilAdapter.getDatabaseInfo(AbstractUtilAdapter.java:89)
      org.citydb.database.connection.DatabaseConnectionPool.connect(DatabaseConnectionPool.java:159)
      org.citydb.cli.ImpExpCli.initDBPool(ImpExpCli.java:286)
  Caused by:
      java.io.EOFException
      org.postgresql.core.PGStream.receiveChar(PGStream.java:372)
      org.postgresql.core.v3.ConnectionFactoryImpl.enableSSL(ConnectionFactoryImpl.java:416)
      org.postgresql.core.v3.ConnectionFactoryImpl.tryConnect(ConnectionFactoryImpl.java:140)
      org.postgresql.core.v3.ConnectionFactoryImpl.openConnectionImpl(ConnectionFactoryImpl.java:197)
      ... 17 more
      [12:33:57 ERROR] Aborting...
  ```

### Problem illustration with the Tiler as client
The Tiler runs ok (parsing of difference files) until it requires access to the database. Then the error message is then of the form:
```
File "Tilers/CityTiler/CityTemporalTiler.py", line 464, in <module> main()
File "Tilers/CityTiler/CityTemporalTiler.py", line 439, in main
     cursors = open_data_bases(cli_args.db_config_path)
File "/py3dtiles.git/Tilers/CityTiler/database_accesses.py", line 78, in open_data_bases
     cursors.append(open_data_base(file_path))
File "/py3dtiles.git/Tilers/CityTiler/database_accesses.py", line 47, in open_data_base
     keepalives_count=5
File "/usr/local/lib/python3.7/site-packages/psycopg2/__init__.py", line 127, in connect
     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
     psycopg2.OperationalError: could not connect to server: Connection refused
     Is the server running on host "134.214.143.170" and accepting
     TCP/IP connections on port 5432?
Exiting  TemporalTiler  with success.
```
And we have already seen that IP/port connectivity is not the cause of the problem. 

## Further collected hints

### Shuting down logs (after database creation)
Here are the logs when 
 - the container was started with an empty database which triggers a database
   initialization (`The database cluster will be initialized` gets logged) 
   gracefully ending with the following logs 
   ```
   09:41:54.270 UTC [47] LOG:  starting PostgreSQL 12.2 (Debian 12.2-2.pgdg100+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 8.3.0-6) 8.3.0, 64-bit
   09:41:54.272 UTC [47] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
   09:41:54.317 UTC [48] LOG:  database system was shut down at 09:41:52 UTC
   09:41:54.336 UTC [47] LOG:  database system is ready to accept connections
                               done
                               server started
   ```
 - then the container is required to stop (with a docker level timeout set to 120 seconds)
    ```
    09:42:24.425 UTC [47] LOG:  received fast shutdown request
    09:42:24.427 UTC [47] LOG:  aborting any active transactions
    09:42:24.429 UTC [47] LOG:  background worker "logical replication launcher" (PID 54) exited with exit code 1.
    09:42:24.465 UTC [83] FATAL:  terminating connection due to administrator command
    09:42:24.465 UTC [83] LOG:  could not send data to client: Broken pipe
    09:42:24.471 UTC [49] LOG:  shutting down..
    09:42:26.993 UTC [47] LOG:  database system is shut down done
                                server stopped
                                PostgreSQL init process complete; ready for start up.
    09:42:27.025 UTC [1] LOG:  starting PostgreSQL 12.2 (Debian 12.2-2.pgdg100+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 8.3.0-6) 8.3.0, 64-bit
    09:42:27.026 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 543209:42:27.026 UTC [1] LOG:  listening on IPv6 address "::", port 5432\r\n
    09:42:27.029 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
    09:42:27.132 UTC [86] LOG:  database system was shut down at 09:42:25 UTC
    09:42:27.154 UTC [1] LOG:  database system is ready to accept connections
    09:42:42.971 UTC [1] LOG:  received smart shutdown request
    09:42:42.976 UTC [1] LOG:  background worker "logical replication launcher" (PID 92) exited with exit code 1'
    ```

Some remarks:
 * notice that although the database was cleanly halted (log entry at 
   `09:42:26.993`) it immediatly restarts (at entry `09:42:27.025`) 
 * setting a timeout was suggested by this 
   [github issue](https://github.com/docker-library/postgres/issues/544#issuecomment-455738848)
 * according to this [StackOverflow thread](https://stackoverflow.com/questions/58952919/postgresql-background-worker-logical-replication-launcher-exited-with-exit-co) 
   the log message `background worker "logical replication launcher" (PID 54) exited with exit code 1` can be joyfully disregarded. 

### Restarting the database container (empty database after above clean shutdown)
Just after the above clean shutdown (at least one could believe it was clean),
we restart the container and get the following logs
```
PostgreSQL Database directory appears to contain a database; Skipping initialization
14:45:13.525 UTC [1] LOG:  starting PostgreSQL 12.2 (Debian 12.2-2.pgdg100+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 8.3.0-6) 8.3.0, 64-bit
14:45:13.525 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
14:45:13.525 UTC [1] LOG:  listening on IPv6 address "::", port 5432
14:45:13.528 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
14:45:13.605 UTC [27] LOG:  database system was interrupted; last known up at 09:47:28 UTC
14:45:15.061 UTC [28] FATAL:  the database system is starting up
14:45:16.060 UTC [29] FATAL:  the database system is starting up
14:45:17.064 UTC [30] FATAL:  the database system is starting up
14:45:18.066 UTC [31] FATAL:  the database system is starting up
14:45:18.298 UTC [27] LOG:  database system was not properly shut down; automatic recovery in progress  14:45:18.368 UTC [27] LOG:  redo starts at 0/27E68E8
14:45:18.368 UTC [27] LOG:  invalid record length at 0/27E6998: wanted 24, got 0
14:45:18.368 UTC [27] LOG:  redo done at 0/27E6920
14:45:18.513 UTC [1] LOG:  database system is ready to accept connections
14:46:09.125 UTC [1] LOG:  received smart shutdown request
14:46:09.133 UTC [1] LOG:  background worker "logical replication launcher" (PID 37) exited with exit code 1
```
Hence the process goes:
 * because the database considers it was not cleanly interrupted
(at `14:45:18.298`) 
 * it restores it integrity and thus 
 * only accepts connections after some delay (at `14:45:18.513`).

### Restarting a 1Tb database container (after above clean shutdown)
Now the above integrity restauration delay is "quite" short (less that a second of 
elapsed time) because the database what empty.
But with some bigger contents then this process can be lengthier. The log below
illustrates what happens for a Tb of data (a single vintage of all Lyon bouroughs):
```
14:51:16.004 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
14:51:16.117 UTC [28] LOG:  database system was interrupted; last known up at 14:43:58 UTC
14:51:16.515 UTC [29] FATAL:  the database system is starting up
            <repeated many times>
14:51:22.654 UTC [28] LOG:  database system was not properly shut down; automatic recovery in progress
14:51:22.734 UTC [28] LOG:  redo starts at 0/560DC680
14:51:23.520 UTC [36] FATAL:  the database system is starting up
            <repeated many times> 
14:53:20.664 UTC [144] FATAL:  the database system is starting up
14:53:20.985 UTC [1] LOG:  received smart shutdown request
14:53:21.028 UTC [145] LOG:  shutting down
```
i.e. after more than two minutes the database is still starting up.

In the meantime a Python written client started (after waiting for an arbitrary two 
minutes delay hardcoded in the souce) pulling querries and crashing with the message
(already mentionned above)
```
16:53:10 INFO     docker-stdout> b'Database configuration file passed through mounted /Input
                  Launching command : [\'python3\', \'Tilers/CityTiler/CityTiler.py\', \'/Input/CityTilerDBConfigStatic2009.yml\']
  Traceback (most recent call last):
    File "Tilers/CityTiler/CityTiler.py", line 208, in <module>
      main()
    File "Tilers/CityTiler/CityTiler.py", line 184, in main
      cursor = open_data_base(args.db_config_path)
    File "/py3dtiles.git/Tilers/CityTiler/database_accesses.py", line 47, in open_data_base
      keepalives_count=5
    File "/usr/local/lib/python3.7/site-packages/psycopg2/__init__.py", line 127, in connect
      conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
  psycopg2.OperationalError: FATAL:  the database system is starting up
```
After the client died the main script requires the database to shut down
(ten seconds later at `4:53:20.985` in the first log).


## The analysis
The above mentionned docker "timeout trick" (suggested by this 
[github](https://github.com/docker-library/postgres/issues/544#issuecomment-455738848))
was not of much help.
The database running in its container displays a nice
```
14:45:32.495 UTC [1] LOG:  received smart shutdown request
14:45:32.504 UTC [1] LOG:  background worker "logical replication launcher" (PID 93) exited with exit code 1
```
yet when the database restarts it enters in some integrity rebuild that lasts 
for some unknown (but probably proportional to the database size) length of
time... 
In the meantime the database clients cannot connect the database,fail poorly
bringing the pipeline down.

## Hints for solving the problem
This "slow starting postgresql startup in a docker container" seems to be a well known
issue as illustrated by 
 * [this StackOverflow thread](https://stackoverflow.com/questions/55762687/slow-postgresql-startup-in-docker-container)
 * [this github issue](https://github.com/bitnami/bitnami-docker-postgresql/issues/79)
 * [this StackExchange thread](https://dba.stackexchange.com/questions/193301/macos-homebrew-database-system-was-not-properly-shut-down-automatic-recovery-i)

The experts here seem to counsel looking into something like
`docker exec <...> pg_ctl stop`...
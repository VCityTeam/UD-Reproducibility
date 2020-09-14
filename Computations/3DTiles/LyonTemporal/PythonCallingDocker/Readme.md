## Pre-requisites
 - [install Python3.7](https://www.python.org/)

## Configuration step
Edit the `demo_configuration.py` configuration file in order to setup
 - the required output directory,
 - the concerned vintages (currently only 2009, 2012 and 2015 are available from
   Grand Lyon open data) 
 - the considered boroughs,
 - the database configurations corresponding to each considered vintage 
   (these databases will hold the integrated citygml data). 

Notes:
 * in order to configure `PG_HOST` i.e. the IP number of the host machine, you
   might use (on a linux machine) the `hostname -I` command.
 * the `PG_HOST`, although present in three configuration files, must be the same shared IP number value for the three configuration files. This is because the three (3dCity) databases used by the worklow run on the same host...

## Installing dependencies

### The direnv method (recommendable)
```
$ git rev-parse --show-toplevel
$ cd Computations/3DTiles/LyonTemporal/PythonCallingDocker
$ ln -s .envrc.tpl .envrc
$ direnv allow
(venv)$          # You are all set
```

### The hands on method
Create a python virtual environment and activate it
```
$ git rev-parse --show-toplevel
$ cd Computations/3DTiles/LyonTemporal/PythonCallingDocker
$ virtualenv -p python3 venv
$ . venv/bin/activate
(venv)$ pip install -r requirements.txt
```

## Running the unit tests
In order to test the containers:
```
$ git rev-parse --show-toplevel
$ cd Computations/3DTiles/LyonTemporal/PythonCallingDocker
(venv)$ pip install pytest pytest-ordering pytest-dependency
(venv)$ pytest
```

## Running the workflow
Be it with the single run of the full workflow or with the manual 
steps (refer bellow) the resulting file hierarchies will be located
in the `junk` sub-directory (as configured by the `output_dir` variable
of `demo_configuration.py`, refer above).

### Running the full workflow
```
$ cd Computations/3DTiles/LyonTemporal/PythonCallingDocker
(venv)$ python run_demo_full_worflow.py
```

### Manual step by step run
The following manual steps should be applied in order:
```
$ cd Computations/3DTiles/LyonTemporal/PythonCallingDocker
(venv)$ python run_demo_lyon_metropole_dowload_and_sanitize.py   # result in junk/stage_1
(venv)$ python run_demo_split_buildings.py                       # result in junk/stage_2
(venv)$ python run_demo_strip_attributes.py                      # result in junk/stage_3 
(venv)$ python run_demo_extract_building_dates.py                # result in junk/stage_4
(venv)$ python run_demo_3dcitydb_server.py                       # Just a test: no output
(venv)$ python run_demo_load_3dcitydb.py                         # result in junk/stage_5
(venv)$ python run_demo_temporal_tiler.py                        # result in junk/stage_6
```

## Developers notes
 * Debugging of a container
   ```
   docker run -v `pwd`/junk/LYON_1ER_2009/:/Input -v `pwd`/junk_split/:/Output -it liris:3DUse /bin/bash
   root@ splitCityGMLBuildings --input-file /Input/LYON_1ER_BATI_2009.gml --output-file LYON_1ER_BATI_2009_splited.gml --output-dir /Output/
   ```

## Issues

### Bug: extractBuildingDates stage fails on Villeurbanne data
The following run fails
```
docker run -v `pwd`:/Input --workdir /root/3DUSE/Build/src/utils/cmdline/ -t liris:3DUse extractBuildingDates --first_date 2009 --first_file /Input/junk/VILLEURBANNE_2009/VILLEURBANNE_BATI_2009.gml --second_date 2012 --second_file /Input/junk/VILLEURBANNE_2012/VILLEURBANNE_BATI_2012.gml --output_dir /Input/junk/2009_2012_Differences/VILLEURBANNE_2009-2012/
```
with the message:
```
CityGML first file loaded :/Input/junk/VILLEURBANNE_2009/VILLEURBANNE_BATI_2009.gml
CityGML second file loaded :/Input/junk/VILLEURBANNE_2012/VILLEURBANNE_BATI_2012.gml
Model 1: 
    Converting building: 455/455 
Done.
Model 2: 
    Converting building: 447/447 
Done.
Internal buildings pre-processing...
ERROR 1: TopologyException: found non-noded intersection between LINESTRING (1.8489e+06 5.17487e+06, 1.84892e+06 5.17488e+06) and LINESTRING (1.84891e+06 5.17488e+06, 1.84892e+06 5.17488e+06) at 1848907.2497562491 5174876.2345244605 191.31213515757889
```
This error seems related with postgis or gdal according to threads like:
 * [R wrapping of gdal](https://stackoverflow.com/questions/13662448/what-does-the-following-error-mean-topologyexception-found-non-nonded-intersec)
 * [r-spatial/sf issue](https://github.com/r-spatial/sf/issues/860)

### Debugging the importer exporter
 * The following proves that the database server is ok
   ```
   docker run -v `pwd`/:/InputConfig -it --entrypoint /bin/bash tumgis/3dcitydb-impexp:4.2.3

   apt-get update
   apt-get install postgresql postgresql-contrib
   psql -h 134.214.143.170 -p 5432 -U postgres -d citydb-full_lyon-2009 -c "\dt"
   # provide postgres as password
   .... # you will get some answer
   ```

 * The following single call reproduces the error:
    ```
    docker run -v `pwd`/:/InputConfig -v `pwd`/junk/LYON_2009_Stripped:/InputFiles -it tumgis/3dcitydb-impexp:4.2.3 -config /InputConfig/3dCityDBImpExpConfig2009.xml -import /InputFiles/LYON_1ER_BATI_2009_splited_stripped.gml
    ```
 * Further notes:
   - when the databases are not launched the error message is
     ```
     org.citydb.ImpExpException: Connection to database could not be established.
     [...]
     Caused by: org.postgresql.util.PSQLException:
        Connection to 134.214.143.170:5432 refused. Check that the hostname and port are
        correct and that the postmaster is accepting TCP/IP connections
     ```
   - when the databases were previously launched and stopped (and <output>/postgres-data/ 
     directory exists) then two error messages are possible
     ```
     org.citydb.ImpExpException: Connection to database could not be established.
     [...]
     Caused by: org.postgresql.util.PSQLException: FATAL: the database system is starting up
     ```
     or
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

### Debugging the Tiler
The Tiler runs ok (parsing of difference files) until it requires access to the databases. The
error message is then of the form:
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

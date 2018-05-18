# Geodata

#### sources of data

https://freegisdata.rtwilson.com/ Contains Gis datasets
https://www.census.gov/2010census/

https://www.europeandataportal.eu/data/dataset


The data has some shapefiles with many layers
http://www5.kingcounty.gov/gisdataportal/
https://gis-kingcounty.opendata.arcgis.com/

**DHS progam data**

http://spatialdata.dhsprogram.com/home/

## developer notes:

#### Speed:

it turns out that PointFromText is perhaps the slowest way of doing this in Postgis. Using a combination of ST_Setsrid and ST_Point is on the magnitude of 7 to 10 times faster at least for versions of PostGIS 1.2 and above. ST_GeomFromText comes in second (replace ST_PointFromText with ST_GeomFromText) at about 3 to 1.5 times slower than ST_SetSRID ST_Point. See about PointFromText on why PointFromText is probably slower. In ST_GeomFromText, there appears to be some caching effects so on first run with similar datasets ST_GeomFromText starts out about 3-4 times slower than the ST_makepoint (ST_Point) way and then catches up to 1.5 times slower. This I tested on a dataset of about 150,000 records and all took - 26 secs for ST_PointFromText fairly consistently, 10.7 secs for first run of GeomFromText then 4.1 secs for each consecutive run, 3.5 secs fairly consistently for setsrid,makepoint on a dual Xeon 2.8 Ghz, Windows 2003 32-bit with 2 gig RAM).

### Geojson

To create json 

ogrinfo -ro point.geojson

### postgis
we can load files in two ways
ref:http://suite.opengeo.org/docs/latest/dataadmin/pgGettingStarted/shp2pgsql.html

##### system

```python

p1 = subprocess.Popen(["cmd", "/C", "shp2pgsql","-a","-s 4326","roads.shp", "roads"], stdout=subprocess.PIPE)
stdout, stderr = p1.communicate()
with open('roads.sql', 'w') as f:
    f.writelines(stdout)

```
or

```python
p1 = subprocess.Popen(["cmd", "/C", "shp2pgsql","-a","-s 4326","roads.shp", "roads"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p2 = subprocess.Popen(['psql',  '-d db'], stdin=p1.stdout,    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p1.stdout.close()
stdout, stderr= p2.communicate()

```


```python

import os, subprocess

# Choose your PostgreSQL version here
os.environ['PATH'] += r';C:\Program Files (x86)\PostgreSQL\8.4\bin'
# http://www.postgresql.org/docs/current/static/libpq-envars.html
os.environ['PGHOST'] = 'localhost'
os.environ['PGPORT'] = '5432'
os.environ['PGUSER'] = 'someuser'
os.environ['PGPASSWORD'] = 'clever password'
os.environ['PGDATABASE'] = 'geometry_database'

base_dir = r"c:\shape_file_repository"
full_dir = os.walk(base_dir)
shapefile_list = []
for source, dirs, files in full_dir:
    for file_ in files:
        if file_[-3:] == 'shp':
            shapefile_path = os.path.join(base_dir, file_)
            shapefile_list.append(shapefile_path)
for shape_path in shapefile_list:
    cmds = 'shp2pgsql "' + shape_path + '" new_shp_table | psql '
    subprocess.call(cmds, shell=True)

```

#### Python

ref:https://gis.stackexchange.com/questions/90085/import-shp-to-postgis-using-python-and-ogr

```python

import os.path import psycopg2
import osgeo.ogr connection = psycopg2.connect("dbname=... user=...") cursor = connection.cursor() cursor.execute("DELETE FROM countries") srcFile = os.path.join("DISTAL-data", "TM_WORLD_BORDERS-0.3","TM_WORLD_BORDERS-0.3.shp") shapefile = osgeo.ogr.Open(srcFile)   layer = shapefile.GetLayer(0)   for i in range(layer.GetFeatureCount()):     feature = layer.GetFeature(i)     name = feature.GetField("NAME").decode("Latin-1")     wkt = feature.GetGeometryRef().ExportToWkt()     cursor.execute("INSERT INTO countries (name,outline) " +"VALUES (%s, ST_GeometryFromText(%s, " +"4326))", (name.encode("utf8"), wkt)) 
connection.commit()

```

### Spatialite
http://www.gaia-gis.it/gaia-sins/spatialite-tutorial-2.3.1.html#t1
 .loadshp shape_regions NewRegions CP1252


 incase you connect this make sure is in path or can be loaded

```python
 import sqlite3

with sqlite3.connect(":memory:") as conn:
    conn.enable_load_extension(True)
    conn.load_extension("mod_spatialite")

```

```python
from osgeo import ogr
from pysqlite2 import dbapi2 as sqlite


myPath = r"D:\testSpatiaLite.sqlite"
conn = sqlite.connect(myPath)
conn.enable_load_extension(True)
curs = conn.cursor()
curs.execute("select load_extension('libspatialite-1.dll')")
curs.execute("""SELECT attribute1, AsText(the_geom) FROM points""")

output = "d:\\points.shp"

out_driver = ogr.GetDriverByName( 'ESRI Shapefile' )
out_ds = out_driver.CreateDataSource(output)
out_srs = None
out_layer = out_ds.CreateLayer("point", out_srs, ogr.wkbPoint)
fd = ogr.FieldDefn('name',ogr.OFTString)
out_layer.CreateField(fd)

for row in curs:
    feature = ogr.Feature(out_layer.GetLayerDefn())
    wkt = row[1]

    point = ogr.CreateGeometryFromWkt(wkt)
    feature.SetGeometry(point)
    feature.SetField('name',row[0])
    out_layer.CreateFeature(feature)
    feature.Destroy()

conn.close()
out_ds.Destroy()

```

all spatialite bindind

```python


# importing pyspatialite
from pyspatialite import dbapi2 as db

# creating/connecting the test_db
conn = db.connect('test_db.sqlite')

# creating a Cursor
cur = conn.cursor()

# testing library versions
rs = cur.execute('SELECT sqlite_version(), spatialite_version()')
for row in rs:
    msg = "> SQLite v%s Spatialite v%s" % (row[0], row[1])
    print msg

# initializing Spatial MetaData
# using v.2.4.0 this will automatically create
# GEOMETRY_COLUMNS and SPATIAL_REF_SYS
sql = 'SELECT InitSpatialMetadata()'
cur.execute(sql)

# creating a POINT table
sql = 'CREATE TABLE test_pt ('
sql += 'id INTEGER NOT NULL PRIMARY KEY,'
sql += 'name TEXT NOT NULL)'
cur.execute(sql)
# creating a POINT Geometry column
sql = "SELECT AddGeometryColumn('test_pt'," sql += "'geom', 4326, 'POINT', 'XY')"
cur.execute(sql)

# creating a LINESTRING table
sql = 'CREATE TABLE test_ln ('
sql += 'id INTEGER NOT NULL PRIMARY KEY,'
sql += 'name TEXT NOT NULL)'
cur.execute(sql)
# creating a LINESTRING Geometry column
sql = "SELECT AddGeometryColumn('test_ln', "
sql += "'geom', 4326, 'LINESTRING', 'XY')"
cur.execute(sql)

# creating a POLYGON table
sql = 'CREATE TABLE test_pg ('
sql += 'id INTEGER NOT NULL PRIMARY KEY,'
sql += 'name TEXT NOT NULL)'
cur.execute(sql)
# creating a POLYGON Geometry column
sql = "SELECT AddGeometryColumn('test_pg', "
sql += "'geom', 4326, 'POLYGON', 'XY')"
cur.execute(sql)

# inserting some POINTs
# please note well: SQLite is ACID and Transactional
# so (to get best performance) the whole insert cycle
# will be handled as a single TRANSACTION
for i in range(100000):
    name = "test POINT #%d" % (i+1)
    geom = "GeomFromText('POINT("
    geom += "%f " % (i / 1000.0)
    geom += "%f" % (i / 1000.0)
    geom += ")', 4326)"
    sql = "INSERT INTO test_pt (id, name, geom) "
    sql += "VALUES (%d, '%s', %s)" % (i+1, name, geom)
    cur.execute(sql)
conn.commit()

# checking POINTs
sql = "SELECT DISTINCT Count(*), ST_GeometryType(geom), "
sql += "ST_Srid(geom) FROM test_pt"
rs = cur.execute(sql)
for row in rs:
    msg = "> Inserted %d entities of type " % (row[0])
    msg += "%s SRID=%d" % (row[1], row[2])
    print msg

# inserting some LINESTRINGs
for i in range(100000):
    name = "test LINESTRING #%d" % (i+1)
    geom = "GeomFromText('LINESTRING("
    if (i%2) == 1:
    # odd row: five points
        geom += "-180.0 -90.0, "
        geom += "%f " % (-10.0 - (i / 1000.0))
        geom += "%f, " % (-10.0 - (i / 1000.0))
        geom += "%f " % (10.0 + (i / 1000.0))
        geom += "%f" % (10.0 + (i / 1000.0))
        geom += ", 180.0 90.0"
    else:
    # even row: two points
        geom += "%f " % (-10.0 - (i / 1000.0))
        geom += "%f, " % (-10.0 - (i / 1000.0))
        geom += "%f " % (10.0 + (i / 1000.0))
        geom += "%f" % (10.0 + (i / 1000.0))
    geom += ")', 4326)"
    sql = "INSERT INTO test_ln (id, name, geom) "
    sql += "VALUES (%d, '%s', %s)" % (i+1, name, geom)
    cur.execute(sql)
conn.commit()

# checking LINESTRINGs
sql = "SELECT DISTINCT Count(*), ST_GeometryType(geom), "
sql += "ST_Srid(geom) FROM test_ln"
rs = cur.execute(sql)
for row in rs:
    msg = "> Inserted %d entities of type " % (row[0])
    msg += "%s SRID=%d" % (row[1], row[2])
    print msg

# inserting some POLYGONs
for i in range(100000):
    name = "test POLYGON #%d" % (i+1)
    geom = "GeomFromText('POLYGON(("
    geom += "%f " % (-10.0 - (i / 1000.0))
    geom += "%f, " % (-10.0 - (i / 1000.0))
    geom += "%f " % (10.0 + (i / 1000.0))
    geom += "%f, " % (-10.0 - (i / 1000.0))
    geom += "%f " % (10.0 + (i / 1000.0))
    geom += "%f, " % (10.0 + (i / 1000.0))
    geom += "%f " % (-10.0 - (i / 1000.0))
    geom += "%f, " % (10.0 + (i / 1000.0))
    geom += "%f " % (-10.0 - (i / 1000.0))
    geom += "%f" % (-10.0 - (i / 1000.0))
    geom += "))', 4326)"
    sql = "INSERT INTO test_pg (id, name, geom) "
    sql += "VALUES (%d, '%s', %s)" % (i+1, name, geom)
    cur.execute(sql)
conn.commit()

# checking POLYGONs
sql = "SELECT DISTINCT Count(*), ST_GeometryType(geom), "
sql += "ST_Srid(geom) FROM test_pg"
rs = cur.execute(sql)
for row in rs:
    msg = "> Inserted %d entities of type " % (row[0])
    msg += "%s SRID=%d" % (row[1], row[2])
    print msg

rs.close()
conn.close()
quit()

```


#### bash

```bash
#!/bin/bash

for f in *.shp
do
    shp2pgsql -I -s <SRID> $f `basename $f .shp` > `basename $f .shp`.sql
done

```

#### shape_importer

```python
#!/user/bin/python2.7

#script for importing US Census Tract File
#works specifically for subfolder 'shapefiles' with x number of subfolders for each state
#requires pyshp library http://code.google.com/p/pyshp/ and psycopg2 postgresql library


import psycopg2
import shapefile
import glob

#loop through each record in shapefile
def process_shapes(shape_records):
  for record in shape_records:
    insert_shape(record)

#create the shape in the database
def insert_shape(new_record):
  tract_latln = new_record.record[10:]
  tract_number = new_record.record[2]
  cur.execute("INSERT INTO tracts(lat, lng, tract_number) VALUES(%s, %s, %s) RETURNING id", 
      (float(tract_latln[0]), float(tract_latln[1]), tract_number))
  insert_points(new_record, cur.fetchone()[0]) 

#insert corrisponding boundary points for a given shape relation
def insert_points(new_record, id):
  for point in new_record.shape.points:
    cur.execute("INSERT INTO tract_points(lat, lng, tract_id) VALUES(%s, %s, %s)", 
        (float(point[0]), float(point[1]), id))


#connect to postgres db
try:
  conn = psycopg2.connect(database="picket_development", user="picket", host="localhost", password="")
except:
  print "Can't connect to database"

cur = conn.cursor()

#loop through each of the subdirectories, open and process each shapefile
for dir in glob.glob('shapefiles/*'):
  file_str = dir[dir.find("/") + 1:]
  sf = shapefile.Reader(dir + "/" + file_str)
  shape_records  = sf.shapeRecords()
  process_shapes(shape_records)
  conn.commit()
```

Joins

http://www.qgistutorials.com/en/docs/performing_table_joins.html
http://revenant.ca/www/postgis/workshop/joins.html
https://www.tutorialspoint.com/postgresql/postgresql_using_joins.htm

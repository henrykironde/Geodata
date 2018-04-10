# Geodata


Voting_Centers_and_Ballot_Sites
-------------------------------

Source : http://hub.arcgis.com/datasets/piercecowa::voting-centers-and-ballot-sites
link: http://pcjericks.github.io/py-gdalogr-cookbook/vector_layers.html#get-shapefile-feature-count


This data has an example package
https://services2.arcgis.com/1UvBaQ5y1ubjUPmd/arcgis/rest/services/Voting_Centers_and_Ballot_Sites/FeatureServer/0

Json Example:
https://services2.arcgis.com/1UvBaQ5y1ubjUPmd/arcgis/rest/services/Voting_Centers_and_Ballot_Sites/FeatureServer/0?f=pjson



boundaries
----------

This dataset is from http://www.bostongis.com/?content_name=postgis_tut01#316
 MassGIS site

 we load the data by running
 `shp2pgsql -s 26986 BOUNDARY_POLY towns > towns.sql`

 and

 `psql -d gisdb -h localhost -U postgres -f towns.sql`
 
 
 #### TOOLS For extravtion 
 
 ```python
 import gzip

archivename="C:/Users/Henry/Downloads/Example.json.gz"


import zipfile
import gzip
import tarfile


import struct
from gzip import FEXTRA, FNAME


def read_gzip_info(gzipfile):
    gf = gzipfile.fileobj
    pos = gf.tell()

    # Read archive size
    gf.seek(-4, 2)
    size = struct.unpack('<I', gf.read())[0]

    gf.seek(0)
    magic = gf.read(2)
    if magic != '\037\213':
        raise IOError('Not a gzipped file')

    method, flag, mtime = struct.unpack("<BBIxx", gf.read(8))

    if not flag & FNAME:
        # Not stored in the header, use the filename sans .gz
        gf.seek(pos)
        fname = gzipfile.name
        if fname.endswith('.gz'):
            fname = fname[:-3]
        return fname, size

    if flag & FEXTRA:
        # Read & discard the extra field, if present
        gf.read(struct.unpack("<H", gf.read(2)))

    # Read a null-terminated string containing the filename
    fname = []
    while True:
        s = gf.read(1)
        if not s or s=='\000':
            break
        fname.append(s)

    gf.seek(pos)
    return ''.join(fname), size

"C:/Users/Henry/Downloads/Example.json.gz"
open_archive_file = gzip.open(archivename, 'r')
print(dir(open_archive_file))

print(open_archive_file.myfileobj)
# open_archive_file = tarfile.open(archivename, 'r')
filename, size = read_gzip_info(open_archive_file)
print(filename)
print(size)

#https://community.esri.com/thread/189469-re-unzip-files-from-directory-tree
#https://teamtreehouse.com/community/python-untar-file-and-change-directory-to-extracted-folder
#https://docs.python.org/2.4/lib/tar-examples.html
 
 ```

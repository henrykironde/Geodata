import sys

sys.path.insert(0, 'Library/Frameworks/GDAL.framework/Versions/2.1/Python/2.7/site-packages')
sys.path.insert(0, 'Library/Frameworks/GDAL.framework/Versions/2.1/Python/2.7/site-packages/osgeo/')

# ref https://gis.stackexchange.com/questions/233654/install-gdal-python-binding-on-mac
from osgeo import gdal
import argparse

import os
import json
import sys
import io
import collections
from collections import OrderedDict
from osgeo import ogr

description = '''
lists information about a raster dataset

'''
usage = '''
This Python wrapper is not intended to replace the command option
It is intended to help you learn how Python bindings work with GDAL

See this link if you need more than this Python wrapper
  http://www.gdal.org/gdalinfo.html

Example,
  gdalinfo.py ../tiff/MY1DMM_CHLORA_2002-07.TIFF

'''

parser = argparse.ArgumentParser(description=description, epilog=usage, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('datasetname')
args = parser.parse_args()

if __name__ == '__main__':

    datasetname = gdal.Open(args.datasetname)
    if datasetname is None:
        print('Could not open %s' % args.datasetname)
        sys.exit(1)

    print ("\nDriver: %s/%s" % (datasetname.GetDriver().ShortName, datasetname.GetDriver().LongName))
    print ("\nSize is %d, %d" % (datasetname.RasterXSize, datasetname.RasterYSize))
    print ("\nBands = %d" % datasetname.RasterCount)
    print ("\nCoordinate System is:", datasetname.GetProjectionRef())
    print ("\nGetGeoTransform() = ", datasetname.GetGeoTransform())
    print ("\nGetMetadata() = ", datasetname.GetMetadata())

    path_to_dir = os.path.join(os.path.expanduser("~"), ".retriever/raw_data/bioclim")


    gis_extension = ".bil"

    allpacks = collections.OrderedDict()
    for path, subdirs, files in os.walk(path_to_dir):

        fi_dict = []
        for file_n in files:
            resource = collections.OrderedDict()
            if file_n.endswith(gis_extension):
                path_to_dir = os.path.abspath(path)
                dir_name = os.path.basename(path_to_dir)

                file_path_source = os.path.join(path_to_dir, file_n)
                source = os.path.normpath(file_path_source)
                allpacks[file_n]["Driver_ShortName"] = datasetname.GetDriver().ShortName
                allpacks[file_n]["Driver_LongName"] = datasetname.GetDriver().LongName
                allpacks[file_n]["XSize"] = datasetname.RasterXSize
                allpacks[file_n]["YSize"] = datasetname.RasterYSize
                allpacks[file_n]["Bands"] = datasetname.RasterCount
                allpacks[file_n]["Coordinate System"] = datasetname.GetProjectionRef()
                allpacks[file_n]["GeoTransform"] = datasetname.GetGeoTransform()

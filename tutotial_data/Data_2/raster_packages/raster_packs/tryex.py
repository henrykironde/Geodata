import os
import json
import sys
import io
from collections import OrderedDict

from osgeo import gdal
from gdalconst import GA_ReadOnly

ENCODING = "latin1"
os.environ['GDAL_DATA'] = r"C:\Users\Henry\PycharmProjects\gdalandgis\gdaltest\data\bio"
gdal.UseExceptions()


gdal.GetDriverByName('EHdr').Register()
i = r"C:\Users\Henry\PycharmProjects\gdalandgis\gdaltest\data\bio\bio1.bil"
t = r"C:\Users\Henry\PycharmProjects\gdalandgis\gdaltest\data\bio\bio1.hdr"

hdf_ds = gdal.Open(i, gdal.gdalconst.GA_ReadOnly)

img = gdal.Open(i, gdal.gdalconst.GA_ReadOnly)
src_ds = img.GetRasterBand(1)
geotransform = img.GetGeoTransform()
print(geotransform, "--k")

print(dir(src_ds))
print()
print("projection", img.GetProjection())
print("driver",img.GetDriver().ShortName)
print("transform", OrderedDict(zip(["xOrigin", "pixelWidth", "rotation_2", "yOrigin", "rotation_4", "pixelHeight"],  img.GetGeoTransform())))
print("colums", img.RasterXSize)
print("rows", img.RasterYSize)
print("band_count",img.RasterCount)

print("llll", dir(img))
print("description", img.GetDescription())
print("no_data_value", src_ds.GetNoDataValue())
print("min",  src_ds.GetMinimum())
print("max",  src_ds.GetMaximum())
print("scale" , src_ds.GetScale())
print("color_table", None if not src_ds.GetRasterColorTable() else True)

print("statistics", OrderedDict(zip(["minimum", "maximum", "mean", "stddev"], src_ds.GetStatistics(True, False))))


# # i = r"C:\Users\Henry\PycharmProjects\gdalandgis\gdaltest\data\bio\land_shallow_topo_2048.tif"
# # files_sc = gdal.Open(i, GA_ReadOnly)
# # print(files_sc)
#
# gdal.GetDriverByName('EHdr').Register()
# i = r"C:\Users\Henry\PycharmProjects\gdalandgis\gdaltest\data\bio\MOD11A1.A2012193.h00v08.005.2012196013548.hdf"
# # files_sc = gdal.Open(i, GA_ReadOnly)



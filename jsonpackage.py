try:
    from osgeo import ogr, osr
except:
    import ogr. osr

import os
import json
import sys
import io
import collections
from collections import OrderedDict
from osgeo import ogr

ENCODING = "latin1"
os.environ['GDAL_DATA'] = "C:\Program Files (x86)\GDAL\gdal-data"

# create json from meta data of the geo source

WKBGeometryType = {
1:"wkbPoint",
2:"wkbLineString",
3:"wkbPolygon",
17:"wkbTriangle",
4:"wkbMultiPoint",
5:"wkbMultiLineString",
6:"wkbMultiPolygon",
7:"wkbGeometryCollection",
15:"wkbPolyhedralSurface",
16:"wkbTIN",
1001:"wkbPointZ",
1002:"wkbLineStringZ",
1003:"wkbPolygonZ",
1017:"wkbTrianglez",
1004:"wkbMultiPointZ",
1005:"wkbMultiLineStringZ",
1006:"wkbMultiPolygonZ",
1007:"wkbGeometryCollectionZ",
1015:"wkbPolyhedralSurfaceZ",
1016:"wkbTINZ",
2001:"wkbPointM",
2002:"wkbLineStringM",
2003:"wkbPolygonM",
2017:"wkbTriangleM",
2004:"wkbMultiPointM",
2005:"wkbMultiLineStringM",
2006:"wkbMultiPolygonM",
2007:"wkbGeometryCollectionM",
2015:"wkbPolyhedralSurfaceM",
2016:"wkbTINM",
3001:"wkbPointZM",
3002:"wkbLineStringZM",
3003:"wkbPolygonZM",
3017:"wkbTriangleZM",
3004:"wkbMultiPointZM",
3005:"wkbMultiLineStringZM",
3006:"wkbMultiPolygonZM",
3007:"wkbGeometryCollectionZM",
3015:"wkbPolyhedralSurfaceZM",
3016:"wkbTinZM",
}


def open_fw(file_name, encoding=ENCODING, encode=True):
    """Open file for writing respecting Python version and OS differences.

    Sets newline to Linux line endings on Python 3
    When encode=False does not set encoding on nix and Python 3 to keep as bytes
    """
    if sys.version_info >= (3, 0, 0):
        if encode:
            file_obj = io.open(file_name, 'w', newline='', encoding=encoding)
        else:
            file_obj = io.open(file_name, 'w', newline='')
    else:
        file_obj = io.open(file_name, 'wb')
    return file_obj


def get_projection(source, driver_name ='ESRI Shapefile'):
    """Get projection from Layer"""

    data_src = get_source(source, driver_name)
    layer = data_src.GetLayer()
    spatial_ref = layer.GetSpatialRef()
    return spatial_ref.ExportToWkt()

    spatial_ref = layer.GetSpatialRef()
    ref = spatial_ref.ExportToWkt()


def get_source(source, driver_name ='ESRI Shapefile'):
    """Open a data source

    if source is of class osgeo.ogr.DataSource read data source else
    consider it a path and open the path return a data source
    """
    if not isinstance(source, ogr.DataSource):
        try:
            driver = ogr.GetDriverByName(driver_name)
            source = driver.Open(source, 0)
            if source is None:
                print('Could not open %s' % (source))
                exit()

        except:
            raise IOError("Data source cannot be opened")
    return source


def create_datapackage(driver_name='ESRI Shapefile' ):
    """Create a data package from a vector data source

    the root dir of the vector file becomes the package name
    """
    allpacks = collections.OrderedDict()
    for path, subdirs, files in os.walk('.'):
        for file_n in files:
            if file_n.endswith(".shp"):
                path_to_dir = os.path.abspath(path)
                dir_name = os.path.basename(path_to_dir)

                file_path_source = os.path.join(path_to_dir, file_n)
                source = os.path.normpath(file_path_source)

                layer_scr = get_source(source, driver_name)
                daLayer = layer_scr.GetLayer()

                allpacks[dir_name] = collections.OrderedDict()
                # spactial ref
                sp_ref = daLayer.GetSpatialRef()
                spatial_ref = "{}".format(str(sp_ref.ExportToWkt()))

                # Json data package dictionary
                allpacks[dir_name]["name"] = daLayer.GetName()
                allpacks[dir_name]["title"] = "The {} dataset".format(daLayer.GetName())
                allpacks[dir_name]["description"] = daLayer.GetDescription()
                allpacks[dir_name]["format"] = "vector" # like  https://specs.frictionlessdata.io/data-resource/ in format: 'csv', 'xls', 'json' here we clasify by type vector or raster
                allpacks[dir_name]["spatial_ref"] = spatial_ref
                allpacks[dir_name]["citation"] = "weaver Pending clarification"
                allpacks[dir_name]["license"] = "Licence for dataset Pending clarification"
                allpacks[dir_name]["driver_name"] ='ESRI Shapefile'
                allpacks[dir_name]["extent"] = OrderedDict(zip(["xMin", "xMax", "yMin", "yMax"], daLayer.GetExtent()))
                allpacks[dir_name]["keywords"] = ["test", "data science", "spatial-data"]
                allpacks[dir_name]["url"] = "FILL"
                allpacks[dir_name]["version"] = "1.0.0"
                allpacks[dir_name]["resources"] = []
                allpacks[dir_name]["retriever"] = "True",
                allpacks[dir_name]["retriever_minimum_version"] = "2.1.0",

                layer = collections.OrderedDict()
                layer["name"] = daLayer.GetName()
                layer["url"] = str(daLayer.GetName())+ "path_to_be_filled"
                layer["geom_type"] = ogr.GeometryTypeToName(daLayer.GetLayerDefn().GetGeomType())
                layer['schema'] = {}
                layer['schema']["fields"] = []
                layerDefinition = daLayer.GetLayerDefn()
                for i in range(layerDefinition.GetFieldCount()):
                    col_obj = collections.OrderedDict()
                    col_obj["name"] = layerDefinition.GetFieldDefn(i).GetName()
                    col_obj["precision"] = layerDefinition.GetFieldDefn(i).GetPrecision()
                    col_obj["type"] = layerDefinition.GetFieldDefn(i).GetTypeName()
                    col_obj["size"] = layerDefinition.GetFieldDefn(i).GetWidth()
                    layer["schema"]["fields"].append(col_obj)
                allpacks[dir_name]["resources"].append(layer)

    for path, subdirs, files in os.walk('.'):
        for file_n in files:
            if file_n.endswith(".shp"):
                path_to_dir = os.path.abspath(path)
                dir_name = os.path.basename(path_to_dir)
                filenamejson = file_n[:-4].replace("-", "_").replace(".", "") + ".json"
                file_path_source = os.path.join(r"C:\Users\Henry\Documents\GitHub\weaver\scripts", filenamejson)
                os.system("git add -f {}".format(file_path_source))

                with open_fw(file_path_source) as output_spec_datapack:
                    json_str = json.dumps(allpacks[dir_name], output_spec_datapack, sort_keys=True, indent=4,
                                          separators=(',', ': '))
                    output_spec_datapack.write(json_str + '\n')

                    output_spec_datapack.close()


create_datapackage()
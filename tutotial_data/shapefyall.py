# # http://www.gis.usu.edu/~chrisg/python/2009/
# # ref:https://pcjericks.github.io/py-gdalogr-cookbook/layers.html
# # import modules
# import os
# import sys
#
# import ogr
#
# # set the working directory
# os.chdir('.')
# print("your current working dir", os.getcwd())
# # open the output text file for writing
# file = open('out.txt', 'w')
#
# # get the shapefile driver
# driver = ogr.GetDriverByName('ESRI Shapefile')
#
#
# # open the data source
# shapefile= "Voting_Centers_and_Ballot_Sites/Voting_Centers_and_Ballot_Sites.shp"
# datasource = driver.Open("Voting_Centers_and_Ballot_Sites/Voting_Centers_and_Ballot_Sites.shp", 0)
# # Zero for read-only and 1 for writeable
#
# if datasource is None:
#     print('Could not open file')
#     sys.exit(1)
#
# # get the data layer
# # index is useful for other data types such
# # as GML, TIGER
# # layer = dataSource.GetLayer()
# # layer = dataSource.GetLayer(0)
#
# layer = datasource.GetLayer()
#
# # Get header values
#
# # source = ogr.Open("a_shapefile.shp")
# # layer = source.GetLayer()
# # ref:https://gis.stackexchange.com/questions/220844/get-field-names-of-shapefiles-using-gdal
# print("\n Get the values of fields in layer")
# schema = []
# ldefn = layer.GetLayerDefn()
# for n in range(ldefn.GetFieldCount()):
#     fdefn = ldefn.GetFieldDefn(n)
#     schema.append(fdefn.name)
# print(schema)
#
#
# # loop through the features in the layer
#
# feature = layer.GetNextFeature()
# print ()
#
# # print(feature.GetFieldAsString('city'))
#
# while feature:
#     # get the attributes
#     city = feature.GetFieldAsString('city')
#     Zip = feature.GetFieldAsString('Zip')
#
#     # get the x,y coordinates for the point
#     geom = feature.GetGeometryRef()
#     x = str(geom.GetX())
#     y = str(geom.GetY())
#
#     # print(x,y, "cordinates for Geom")
#
#     # write info out to the text file
#     file.write(city + ' ' + x + ' ' + y + ' ' + Zip + '\n')
#
#     # destroy the feature and get a new one
#     feature.Destroy()
#     feature = layer.GetNextFeature()
#
# # close the data source and text file
# datasource.Destroy()
# file.close()
#
# ################################################
# ################################################
# ################################################
# # Get Geometry from each Feature in a Layer
#
# layer = datasource.GetLayer()
# for feature in layer:
#     geom = feature.GetGeometryRef()
#     print (geom.Centroid().ExportToWkt())
#
# ################################################
# ################################################
# ################################################
# # Filter by attribute
#
# from osgeo import ogr
# import os
#
# shapefile= "Voting_Centers_and_Ballot_Sites/Voting_Centers_and_Ballot_Sites.shp"
# driver = ogr.GetDriverByName("ESRI Shapefile")
# dataSource = driver.Open(shapefile, 0)
# layer = dataSource.GetLayer()
#
# layer.SetAttributeFilter("City = 'Tacoma'")
#
# for feature in layer:
#     print (feature.GetField("city"))
#
# ################################################
# ################################################
# ################################################
# import os
# for path, subdirs, files in os.walk(r'.'):
#     for file_n in files:
#         # print(path)
#         # print(os.path.normpath(path))
#         print(os.path.basename(path))
#         print(os.path.abspath(path))
#


from osgeo import ogr, osr
import os
shapefile = "tutotial_data/boundaries/BOUNDARY_ARC.shp"
from osgeo import ogr, osr
driver = ogr.GetDriverByName('ESRI Shapefile')
dataset = driver.Open(shapefile, 0)
layer = dataset.GetLayer()
spatialRef = layer.GetSpatialRef()

print (spatialRef.ExportToProj4())
# print (spatialRef.ExportToWkt())
# print (spatialRef.ExportToPrettyWkt())
# print (spatialRef.ExportToPCI())
# print (spatialRef.ExportToUSGS())
# print (spatialRef.ExportToXML())

exit()

# Get the attlibute names
from osgeo import ogr

shapefile = r"C:\Users\Henry\Documents\GitHub\Geodata\tutotial_data\admin\address.shp"
dataSource = ogr.Open(shapefile)
daLayer = dataSource.GetLayer(0)
sp_ref = daLayer.GetSpatialRef()
print(sp_ref)
spatial_ref = "{}".format(str(sp_ref.ExportToWkt()))
print(spatial_ref)
layerDefinition = daLayer.GetLayerDefn()
exit()
for i in range(layerDefinition.GetFieldCount()):
    print(layerDefinition.GetFieldDefn(i).GetName(),"GetName()")
    print(layerDefinition.GetFieldDefn(i).GetDefault(), "GetDefault()")
    print(layerDefinition.GetFieldDefn(i).GetJustify(), "GetJustify()")
    print(layerDefinition.GetFieldDefn(i).GetName(), "GetName()")
    print(layerDefinition.GetFieldDefn(i).GetNameRef(), "GetNameRef()")
    print(layerDefinition.GetFieldDefn(i).GetPrecision(), "GetPrecision()")
    print(layerDefinition.GetFieldDefn(i).GetSubType(), "GetSubType()")
    print(layerDefinition.GetFieldDefn(i).GetType(), "GetType()")
    print(layerDefinition.GetFieldDefn(i).GetTypeName(), "GetTypeName()")
    print(layerDefinition.GetFieldDefn(i).GetWidth(), "GetWidth()")

    # 'GetDefault', 'GetFieldTypeName',
    # 'GetJustify', 'GetName', 'GetNameRef',
    # 'GetPrecision',
    # 'GetSubType', 'GetType', 'GetTypeName', 'GetWidth',
    # print(dir(layerDefinition.GetFieldDefn(i)))
    print()
    print()


exit()
# A note about precision
#
# Only Integer, Integer64, Real, String and Date (not DateTime, just year/month/day)
# field types are supported. The various list, and binary field types cannot be created.
#
# The field width and precision are directly used to establish storage size in the .dbf file.
# This means that strings longer than the field width,
# or numbers that don't fit into the indicated field format will suffer truncation.
#
# Integer fields without an explicit width are treated as width 9, and extended to 10 or 11 if needed.
#
# Integer64 fields without an explicit width are treated as width 18, and extended to 19 or 20 if needed.
#
# Real (floating point) fields without an explicit width are treated as width 24
# with 15 decimal places of precision.
#
# String fields without an assigned width are treated as 80 characters.
#
# ref: http://www.gdal.org/drv_shapefile.html

# print ("Name  -  Type  Width  Precision")
# for i in range(layerDefinition.GetFieldCount()):
#     fieldName =  layerDefinition.GetFieldDefn(i).GetName()
#     fieldTypeCode = layerDefinition.GetFieldDefn(i).GetType()
#     fieldType = layerDefinition.GetFieldDefn(i).GetFieldTypeName(fieldTypeCode)
#     fieldWidth = layerDefinition.GetFieldDefn(i).GetWidth()
#     GetPrecision = layerDefinition.GetFieldDefn(i).GetPrecision()
#
#     print (fieldName + " - " + fieldType+ " " + str(fieldWidth) + " " + str(GetPrecision))

# # Get the attlibute names
# from osgeo import ogr
#
# shapefile = "Voting_Centers_and_Ballot_Sites/Voting_Centers_and_Ballot_Sites.shp"
# dataSource = ogr.Open(shapefile)
# daLayer = dataSource.GetLayer(0)
# layerDefinition = daLayer.GetLayerDefn()
# print (dir(layerDefinition))
# print(layerDefinition.GetName())


from osgeo import ogr, osr
import os
shapefile = "Voting_Centers_and_Ballot_Sites/Voting_Centers_and_Ballot_Sites.shp"
from osgeo import ogr, osr
driver = ogr.GetDriverByName('ESRI Shapefile')
dataset = driver.Open(shapefile, 0)
layer = dataset.GetLayer()
spatialRef = layer.GetSpatialRef()

print (spatialRef.ExportToWkt())
print (spatialRef.ExportToPrettyWkt())
print (spatialRef.ExportToPCI())
print (spatialRef.ExportToUSGS())
print (spatialRef.ExportToXML())

exit()



from osgeo import ogr, osr
import os
os.environ['GDAL_DATA'] = "C:\Program Files (x86)\GDAL\gdal-data"


def get_projection(input_file, driver_name ='ESRI Shapefile'):
    driver = ogr.GetDriverByName(driver_name)
    dataset = driver.Open(input_file, 0)
    # get projection from Layer
    layer = dataset.GetLayer()
    spatialRef = layer.GetSpatialRef()
    dataset = None
    return spatialRef.ExportToWkt()


def reproject_layer(input_file, geom_type, output_file=None, mainref=4326, driver_name ='ESRI Shapefile', inref=None):
    """Reproject a Layer"""
    # 4326 is defualt http://spatialreference.org/ref/epsg/wgs-84/
    # geom_type=ogr.wkbMultiPolygon)

    input_file = os.path.normpath(os.path.abspath(input_file))
    base_path_in = os.path.dirname(input_file)
    input_file_name = os.path.basename(input_file)
    project_file = ""
    ### USE JOIN PATH
    if not output_file:
        output_file = base_path_in + "new" + input_file_name
        project_file = base_path_in   + "new" + input_file_name[:-4] + ".prj"
    else:
        output_file = os.path.normpath(os.path.abspath(output_file))
        base_path_out = os.path.dirname(output_file)
        outfile_name = os.path.basename(output_file)
        project_file = base_path_out   + "new" + outfile_name[:-4] + ".prj"


    driver = ogr.GetDriverByName(driver_name)
    # input SpatialReference
    inSpatialRef = osr.SpatialReference()
    if not inref:
        inref = get_projection(input_file, driver_name=driver_name)

    inSpatialRef.ImportFromWkt(inref)

    # output SpatialReference
    outSpatialRef = osr.SpatialReference()
    outSpatialRef.ImportFromEPSG(mainref)

    # create the CoordinateTransformation
    coordTrans = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)

    # get the input layer
    inDataSet = driver.Open(input_file, 0)
    inLayer = inDataSet.GetLayer()

    # get input layer name to be used when creating output layer
    outLayer = inLayer.GetName()


    # create the output layer
    if os.path.exists(output_file):
        driver.DeleteDataSource(output_file)
    outDataSet = driver.CreateDataSource(output_file)
    outLayer = outDataSet.CreateLayer(outLayer, geom_type=geom_type)

    # add fields
    inLayerDefn = inLayer.GetLayerDefn()
    for i in range(0, inLayerDefn.GetFieldCount()):
        fieldDefn = inLayerDefn.GetFieldDefn(i)
        outLayer.CreateField(fieldDefn)

    # get the output layer's feature definition
    outLayerDefn = outLayer.GetLayerDefn()

    # loop through the input features
    inFeature = inLayer.GetNextFeature()
    while inFeature:
        # get the input geometry
        geom = inFeature.GetGeometryRef()
        # reproject the geometry
        geom.Transform(coordTrans)
        # create a new feature
        outFeature = ogr.Feature(outLayerDefn)
        # set the geometry and attribute
        outFeature.SetGeometry(geom)
        for i in range(0, outLayerDefn.GetFieldCount()):
            outFeature.SetField(outLayerDefn.GetFieldDefn(i).GetNameRef(), inFeature.GetField(i))
        # add the feature to the shapefile or Geofile
        outLayer.CreateFeature(outFeature)
        # dereference the features and get the next input feature
        outFeature = None
        inFeature = inLayer.GetNextFeature()

    # Save and close the files
    inDataSet = None
    outDataSet = None

    # create the prj projection file
    source = osr.SpatialReference()
    file = open(project_file, 'w')
    file.write(outSpatialRef.ExportToWkt())
    file.close()


def reproject_cmd(driver_name, inputfile, outputfile, source_ref, dest_ref):
    """Reproject vector data

    Takes either EPSG codes e.g
    ogr2ogr -f "ESRI Shapefile" original.shp wgs84.shp -s_srs EPSG:27700 -t_srs EPSG:4326

    or other specifications as strings

    ogr2ogr -t_srs '+proj=tmerc +lat_0=21.16666666666667 +lon_0=-158 \
                +k=0.999990 +x_0=500000 +y_0=0 +ellps=GRS80 +units=m +no_defs' \
                output_vector.shp input_vector.shp

    # using EPSG codes
    # http://www.mercatorgeosystems.com/blog-articles/2008/05/30/using-ogr2ogr-to-re-project-a-shape-file/
    # proj.4
    # using https://www.nceas.ucsb.edu/scicomp/recipes/gdal-reproject
    """
    cmd = 'ogr2ogr -f {drv} {input} {output} -s_srs {sr} -t_srs {des}'.format(drv=driver_name, input=inputfile, output=outputfile, sr=source_ref, des=dest_ref)
    # cmd = "ogr2ogr -f "ESRI Shapefile" original.shp wgs84.shp -s_srs EPSG:27700 -t_srs EPSG:4326"

    os.system()

# reproject_layer("C:/Users/Henry/Documents/GitHub/Geodata/vector/regioni2001/reg2001_s.shp", geom_type=ogr.wkbPolygon)


def reproject_raster():
    cmd = "gdalwarp -t_srs EPSG:2784 input_raster.tif output_raster.tif"
    # or
    cmd = "gdalwarp -t_srs '+proj=tmerc +lat_0=21.16666666666667 +lon_0=-158 \
                +k=0.999990 +x_0=500000 +y_0=0 +ellps=GRS80 +units=m +no_defs' \
                input_raster.tif output_raster.tif"


# def reproject_cmd(driver_name, inputfile, outputfile, source_ref, dest_ref):
#     cmd = 'ogr2ogr -f {drv} {input} {out} -s_srs {src} -t_srs {des}'.format(drv=driver_name, input=inputfile, out=outputfile, src=source_ref, des=dest_ref)
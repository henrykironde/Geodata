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


from osgeo import ogr
shapefile= "Voting_Centers_and_Ballot_Sites/Voting_Centers_and_Ballot_Sites.shp"
dataSource = ogr.Open(shapefile)
daLayer = dataSource.GetLayer(0)
layerDefinition = daLayer.GetLayerDefn()


for i in range(layerDefinition.GetFieldCount()):
    print (layerDefinition.GetFieldDefn(i).GetName())

    https://pcjericks.github.io/py-gdalogr-cookbook/layers.html
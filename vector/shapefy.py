# python test shapefiles
import os

try:
    from osgeo import ogr, osr
except:
    import ogr. osr

# Get Shapefile Feature Count


with open("output.txt", "w") as a:
    for path, subdirs, files in os.walk(r'.'):
        for filename in files:
            f = os.path.join(path, filename)
            if f.endswith(".shp"):

                # ============================================
                # ============================================
                # daShapefile = r"Voting_Centers_and_Ballot_Sites/Voting_Centers_and_Ballot_Sites.shp"
                # daShapefile = r"boundaries/BOUNDARY_POLY.shp"
                daShapefile = f
                driver = ogr.GetDriverByName('ESRI Shapefile')

                dataSource = driver.Open(f, 0)  # 0 means read-only. 1 means writeable.

                # Check to see if shapefile is found.
                if dataSource is None:
                    print('Could not open %s' % (daShapefile))
                else:
                    print('Opened %s' % (daShapefile))
                    layer = dataSource.GetLayer()
                    featureCount = layer.GetFeatureCount()
                    print("Number of features in %s: %d" % (os.path.basename(daShapefile), featureCount))
                    # # Get the extent of the file
                    # extent = layer.GetExtent()
                    # print("Extent is {}".format(extent))
                    #
                    # # Get features by index or iterate till end
                    # feature = layer.GetFeature(0)
                    # print("\n")
                    # print(feature.GetGeometryRef().GetX())
                    # print(feature.GetGeometryRef().GetY())

                    # Get layer projection
                    spatialRef = layer.GetSpatialRef()
                    print("The spatial ref is",spatialRef )
                    print ("========\n")
                    # # spatialRef.Exp
                    # # sp = osr.SpatialReference()
                    print(spatialRef.ExportToWkt())
                    # print()
                    # print("ExportToProj4():",spatialRef.ExportToProj4())
                    #
                    # # http://www.gis.usu.edu/~chrisg/python/2009/lectures/ospy_slides2.pdf
                    #
                    #
                    # # ============================================
                    # # ============================================
                    #
                    a.write(f + "\n")
                    a.write("Number of features {}\n".format( featureCount))
                    # a.write("ExportToProj4 {}".format(spatialRef.ExportToProj4()))
                    a.write("\n")
                    a.write("projection {}".format(str(spatialRef.ExportToWkt())))
                    a.write(os.linesep)
                    dbname = os.path.basename(f)
                    os.system("shp2pgsql -I  {filepath} {dbname}  > {filepath}.sql".format(filepath=f, dbname=dbname))
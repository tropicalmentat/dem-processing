import gdal, sys
from gdalconst import *
import numpy as np
import time as tm

start = tm.time()

print 'Extracting Low Elevation Coastal Zones...\n'

#open dataset
fn = 'PANAYdem30m.tif'
ds = gdal.Open(fn, GA_ReadOnly)

if ds == None:
    print 'Cannot find data set.'
    sys.exit(1)
else:
    pass
    
driver = ds.GetDriver()

#retrieve image attributes
cols, rows = ds.RasterXSize, ds.RasterYSize
proj, gt = ds.GetProjection(), ds.GetGeoTransform()
iband = ds.GetRasterBand(1)

#extract LECZ and create separate output datasets
error = 5 

for level in range(2,11,2):
    ods = driver.Create('LECZ_' + str(level) + 'm' + '_UTM51N' + '.tif',cols,rows,GDT_Byte)
    ods.SetProjection(proj)
    ods.SetGeoTransform(gt)
    oband = ods.GetRasterBand(1)

    #blocking
    xbs = 1000
    ybs = 1000

    for i in range(0,rows,ybs):
        if rows > i + ybs:
            numrows = ybs
        else:
            numrows = rows - i
        for j in range(0,cols,xbs):
            if cols > j + xbs:
                numcols = xbs
            else:
                numcols = cols - j

            idata = iband.ReadAsArray(j,i,numcols,numrows)

            sealevel = np.where(idata == 0,1,0)
            lecz = np.where(idata <= (level),level,0)
            output = lecz - sealevel
            oband.WriteArray(output,j,i)
            oband.FlushCache()

    #memory management
    ods = None
    oband = None
    idata = None
    lecz = None
    
#memory management
ds = None
iband = None

print '\nExtraction took %f seconds' % (tm.time()-start)

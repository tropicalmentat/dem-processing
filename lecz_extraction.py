import gdal, sys
from gdalconst import *
import numpy as np
import time as tm
import numpy.ma as ma

start = tm.time()

print 'Extracting Low Elevation Coastal Zones...\n'

# open dataset
fn = 'D:\LUIGI\ICLEI\GIS PROJECT FILES\LOW ELEVATION ZONES\\camsur_dem.tif'
ds = gdal.Open(fn, GA_ReadOnly)

if ds == None:
    print 'Cannot find data set.'
    sys.exit(1)
else:
    pass
    
driver = ds.GetDriver()

# retrieve image attributes
cols, rows = ds.RasterXSize, ds.RasterYSize
proj, gt = ds.GetProjection(), ds.GetGeoTransform()
iband = ds.GetRasterBand(1)

# extract LECZ and create separate output datasets
error = 5  # expected upper-bound error for geographical region

for level in range(2, 11, 2):
    # created data set for each lez level
    ods = driver.Create('LECZ_' + str(level) + 'm' + '_UTM51N' + '.tif',
                        cols, rows, GDT_Byte)
    ods.SetProjection(proj)
    ods.SetGeoTransform(gt)
    oband = ods.GetRasterBand(1)

    idata = iband.ReadAsArray(0, 0, cols, rows)

    lez = np.where(idata < level + 1, idata, 0)  # low elevation zone

    no_data = np.where(idata > 0, False, True)  # locate no-data values and replace them with False

    sl_mask = ma.array(lez, mask=no_data, fill_value=-99)  # create no-data value mask

    oband.WriteArray(sl_mask)
    oband.FlushCache()

    # memory management
    ods = None
    oband = None
    idata = None
    lecz = None
    
# memory management
ds = None
iband = None

print '\nExtraction took %f seconds' % (tm.time()-start)

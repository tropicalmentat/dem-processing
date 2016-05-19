import gdal, sys
from gdalconst import *
import numpy as np
import time as tm
import os
from subprocess import call


def extract_pix(f):

    in_ds = gdal.Open(f, GA_ReadOnly)

    if in_ds == None:
        print 'Cannot find data set.'
        sys.exit(1)
    else:
        pass

    driver = in_ds.GetDriver()

    # retrieve image attributes
    cols, rows = in_ds.RasterXSize, in_ds.RasterYSize
    proj, gt = in_ds.GetProjection(), in_ds.GetGeoTransform()
    in_band = in_ds.GetRasterBand(1)

    # create output raster
    out_ds = driver.Create('high_slope.tif',cols,rows,GDT_Byte)
    out_ds.SetProjection(proj)
    out_ds.SetGeoTransform(gt)
    out_band = out_ds.GetRasterBand(1)
    out_band.SetNoDataValue(0)

    # blocking
    print '\nextracting pixels...'
    xbs = 1000
    ybs = 1000

    for i in range(0,rows,ybs):
        if rows > i + ybs:
            num_rows = ybs
        else:
            num_rows = rows - i
        for j in range(0,cols,xbs):
            if cols > j + xbs:
                num_cols = xbs
            else:
                num_cols = cols - j

            in_data = in_band.ReadAsArray(j,i,num_cols,num_rows)
            val_extract = np.where(in_data>=18,in_data,0)  # extract pixels of interest
            out_band.WriteArray(val_extract,j,i)

    out_band.FlushCache()

    return

def ras2poly(f):
    path, name = os.path.split(f)
    out_name = name.split('.')[0] + '.shp'
    cmd = ['gdal_polygonize', f, out_name]
    call()

if __name__ == "__main__":
    start = tm.time()
    ras = "D:\LUIGI\OML\GIS Project Files\RISK OVERLAYS DAVAO CITY\TOPOGRAPHY AND SOIL EROSION\davao_city_slope.tif"
    extract_pix(ras)
    print '\nExtraction took %f seconds' % (tm.time()-start)

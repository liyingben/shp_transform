# -*- coding: utf-8 -*-
import os
import sys
import shutil
from osgeo import ogr
from osgeo import osr
from osgeo import gdal

srcName = "D:/jiangsushengshuju/DOM/39"
tgtName = "D:/jiangsushengshuju/DOM/39_4326/"
toEPSG = 4528
type = "g2w"

srs = osr.SpatialReference()
srs.SetWellKnownGeogCS('WGS84')


def process_file(spath, tpath):
    old_ds = gdal.Open(spath)
    vrt_ds = gdal.AutoCreateWarpedVRT(old_ds, None, srs.ExportToWkt(), gdal.GRA_Bilinear)
    gdal.GetDriverByName('gtiff').CreateCopy(tpath, vrt_ds)


if __name__ == "__main__":

    if os.path.exists(srcName) is False:
        print "路径错误 %s" % (srcName)
        sys.exit()
    list_of_files = []
    # 目录
    if os.path.isdir(srcName):
        for dirpath, dirnames, filenames in os.walk(srcName):
            for filepath in filenames:
                if filepath.lower().endswith(".tif"):
                    spath = os.path.join(dirpath, filepath)
                    tpath = tgtName + os.path.join(dirpath[len(srcName):], filepath)
                    # print spath

                    tdir = os.path.dirname(tpath)
                    if os.path.exists(tdir) is False:
                        os.makedirs(tdir)
                    list_of_files.append((spath, tpath))
    gdal.TermProgress_nocb(0)
    for i in range(len(list_of_files)):
        process_file(list_of_files[i][0], list_of_files[i][1])
        gdal.TermProgress_nocb((i + 1) / float(len(list_of_files)))

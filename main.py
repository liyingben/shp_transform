# -*- coding: utf-8 -*-
from osgeo import ogr
from osgeo import osr
import os
import sys
import shutil
from coordTransform_utils import gcj02_to_bd09
from coordTransform_utils import bd09_to_gcj02
from coordTransform_utils import wgs84_to_gcj02
from coordTransform_utils import gcj02_to_wgs84
from coordTransform_utils import bd09_to_wgs84
from coordTransform_utils import wgs84_to_bd09


def wkbFlatten(x):
    return x & (~ogr.wkb25DBit)


def tPoint(lng, lat, type):
    if type == 'g2b':
        tcoord = gcj02_to_bd09(lng, lat)
    elif type == 'b2g':
        tcoord = bd09_to_gcj02(lng, lat)
    elif type == 'w2g':
        tcoord = wgs84_to_gcj02(lng, lat)
    elif type == 'g2w':
        tcoord = gcj02_to_wgs84(lng, lat)
    elif type == 'b2w':
        tcoord = bd09_to_wgs84(lng, lat)
    elif type == 'w2b':
        tcoord = wgs84_to_bd09(lng, lat)
    else:
        tcoord = [lng, lat]
    return tcoord


def transformation(geom, type=None):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    if geom is None:
        return

    eGType = wkbFlatten(geom.GetGeometryType())
    if eGType == ogr.wkbPoint:
        tcoord = tPoint(geom.GetX(), geom.GetY(), type)
        geom.SetPoint(0, tcoord[0], tcoord[1])

    elif eGType == ogr.wkbLineString or \
            eGType == ogr.wkbLinearRing:
        for i in range(geom.GetPointCount()):
            tcoord = tPoint(geom.GetX(i), geom.GetY(i), type)
            geom.SetPoint(i, tcoord[0], tcoord[1])

    elif eGType == ogr.wkbPolygon or \
            eGType == ogr.wkbMultiPoint or \
            eGType == ogr.wkbMultiLineString or \
            eGType == ogr.wkbMultiPolygon or \
            eGType == ogr.wkbGeometryCollection:
        for i in range(geom.GetGeometryCount()):
            transformation(geom.GetGeometryRef(i), type)

    return geom


def convert(srcName, tgtName, type=None, toEPSG=4326):
    tgt_spatRef = osr.SpatialReference()
    tgt_spatRef.ImportFromEPSG(toEPSG)
    driver = ogr.GetDriverByName("ESRI Shapefile")
    src = driver.Open(srcName, 0)
    srcLyr = src.GetLayer()
    src_spatRef = srcLyr.GetSpatialRef()
    if os.path.exists(tgtName):
        driver.DeleteDataSource(tgtName)
    tgt = driver.CreateDataSource(tgtName)
    lyrName = os.path.splitext(tgtName)[0]

    poSrcFDefn = srcLyr.GetLayerDefn()
    eGType = poSrcFDefn.GetGeomType()

    # 使用WKB格式声明几何图形
    tgtLyr = tgt.CreateLayer(lyrName, geom_type=eGType)
    featDef = srcLyr.GetLayerDefn()
    trans = osr.CoordinateTransformation(src_spatRef, tgt_spatRef)
    srcFeat = srcLyr.GetNextFeature()

    while srcFeat:
        feature = ogr.Feature(featDef)
        geom = srcFeat.GetGeometryRef()
        if geom is not None:
            geom = transformation(geom, type)
            if toEPSG != 4326:
                geom.Transform(trans)
            feature.SetGeometry(geom)
        tgtLyr.CreateFeature(feature)
        feature.Destroy()
        srcFeat.Destroy()
        srcFeat = srcLyr.GetNextFeature()
    src.Destroy()
    tgt.Destroy()

    # 为了导出投影文件将几何图形转换为Esri的WKT格式
    tgt_spatRef.MorphToESRI()
    prj = open(lyrName + ".prj", "w")
    prj.write(tgt_spatRef.ExportToWkt())
    prj.close()
    srcDbf = os.path.splitext(srcName)[0] + ".dbf"
    tgtDbf = lyrName + ".dbf"
    shutil.copyfile(srcDbf, tgtDbf)

toEPSG = 4326
transformType = "g2w"
srcName = "data/origin-shp/polygon.shp"
tgtName = "data/origin-shp/polygon2.shp"

if __name__ == "__main__":

    if os.path.exists(srcName) is False:
        print "路径错误 %s" % (srcName)
        sys.exit()

    if os.path.isfile(tgtName) and os.path.exists(tgtName) is False:
        print "路径错误 %s" % (tgtName)
        sys.exit()

    # 文件
    if os.path.isfile(srcName):
        convert(srcName, tgtName, transformType, toEPSG)

    # 目录
    if os.path.isdir(srcName):
        for dirpath, dirnames, filenames in os.walk(srcName):
            for filepath in filenames:
                if filepath.lower().endswith(".shp"):
                    spath = os.path.join(dirpath, filepath)
                    tpath = os.path.join(dirpath[len(srcName):], filepath)
                    tpath = tgtName + tpath
                    print spath

                    tdir = os.path.dirname(tpath)
                    if os.path.exists(tdir) is False:
                        os.makedirs(tdir)
                    convert(spath, tpath, type, toEPSG)

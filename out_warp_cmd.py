# -*- coding: utf-8 -*-
import os
import sys
import shutil

srcName = "D:\jiangsushengshuju\DOM"
tgtName = "D:\jiangsushengshuju\DOM4326"
toEPSG = 4528
type = "g2w"
if __name__ == "__main__":

    if os.path.exists(srcName) is False:
        print "路径错误 %s" % (srcName)
        sys.exit()

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

                    print("gdalwarp  -overwrite -r bilinear -dstnodata 999 -dstalpha -t_srs \"EPSG:4326\" %s %s" % (
                    spath, tpath))

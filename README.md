# shp-geotransform

在中国特色GIS主义中，我们拿到的SHP数据一般有WGS84和GCJ02两种坐标系。而在实际的GIS开发（基于SHP文件的空间分析和空间展示）中，我们一般用到的坐标系有WGS84、GCJ02、BD09，而且在很多情况下数据的坐标系和底图坐标系息息相关，坐标系不匹配会出现图层偏移，这就涉及到坐标系转换的问题。


## shp-geotransform是什么

本项目旨在从源头解决坐标系不一致问题，做到一次转换，多次利用。

>`常见地图坐标系科普`： 

* WGS84：国际标准，BingMap、谷歌国外地图、osm地图等国外的地图、GPS芯片或者北斗芯片获取的经纬度
* GCJ02：中国标准，谷歌中国地图、搜搜中国地图、高德地图、阿里云、腾讯地图
* BD09：百度标准，百度地图


## 安装
ubuntu安装GDAL
sudo apt-get install libgdal-dev
sudo apt-get install gdal-bin
sudo apt-get -y install python-gdal
运行shp-transform.py；

       
## 使用

1. 选择放置您的shp文件到origin-shp文件夹中；

2. 设置参数，打开根目录下shp_transform.py：

    参数说明:
    * **toEPSG**：输出shp坐标系统，如：4326;
    * **transformType**：坐标系转换类型，包括g2b,b2g,w2g,g2w,b2w,w2b五种；
    * **srcName**：转入shp文件名或目录，如：polygon.shp;
    * **tgtName**：转出shp文件名或目录，如：polygon2.shp;




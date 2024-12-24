#!/usr/bin/python3
"""
Sample a Digital Elevation Model raster values at points. Primarily intended
as a library; other Python modules can use it to add an elevation attribute
to a file of autogenerated waypoints.

However, it can be used standalone to sample a given DEM (GeoTIFF) at the
points given by a given GeoJSON point layer.

Used from the command line, it expects the points to be a GeoJSON file on the
local filesystem.
"""

import argparse
from osgeo import ogr, gdal, osr
import math
import struct
import logging

log = logging.getLogger(__name__)

def raster_data_format_string(input_datatype: str):
    """
    Returns a format string for unpacking a c-style Struct object based
    on the appropriate GDAL raster band data type. Probably not correct
    for all data types; at the moment we're only concerned with the ones
    likely to be encountered in Digital Elevation Models.
    """
    type_map = {
        "Byte": "b",
        "Int8": "b",
        "UInt16": "<H",
        "Int16": "<h",
        "UInt32": "L",
        "Int32": "l",
        "UInt64": "q",
        "Int64": "Q",
        "Float32": "f",
        "Float64": "d",
    }
    struct_data_type = type_map[input_datatype]
    return struct_data_type


def add_elevation_from_dem(raster_file, points, outfile):
    """
    Arguments:
        DEM raster file as GeoTIFF
        Points as GeoJSON string
    Returns:
        Writes GeoJSON file with added elevation attribute on each point
    """
    r = gdal.Open(raster_file)

    # Create an empty Spatial Reference object
    # and set it to the CRS of the input raster
    rasterSR = osr.SpatialReference()
    rasterSR.ImportFromProj4(r.GetProjection())
    log.info(f"\nRaster Coordinate Reference System: \n{rasterSR}")

    # Get the raster band (if it's a DEM, this should be the only band)
    # TODO this would be a good time to check that it's a single-band
    # raster with values that make sense for a DEM
    band = r.GetRasterBand(1)

    # Determine the data type
    raster_data_type = gdal.GetDataTypeName(band.DataType)
    log.info(f"\nRaster band 1 data type: {raster_data_type}")
    struct_data_type = raster_data_format_string(raster_data_type)
    log.info(
        f"The GDAL data type is {raster_data_type}, which hopefully "
        f"corresponds to a struct {struct_data_type} data type"
    )

    # Create the tranforms between geographical and pixel coordinates
    # The forward transform takes pixel coords and returns geographical coords,
    # the reverse transform... well, you get the idea.
    forward = r.GetGeoTransform()
    reverse = gdal.InvGeoTransform(forward)

    p = ogr.Open(points)
    lyr = p.GetLayer()
    pointSR = lyr.GetSpatialRef()
    pointLD = lyr.GetLayerDefn()
    log.info(f"\nPoint layer Coordinate Reference System: {pointSR.GetName()}")

    transform = osr.CoordinateTransformation(pointSR, rasterSR)

    # Create the GDAL GeoJSON output file infrastructure
    outDriver = ogr.GetDriverByName("GeoJSON")
    outDataSource = outDriver.CreateDataSource(outfile)
    outLayer = outDataSource.CreateLayer("waypoints", pointSR, ogr.wkbPoint)

    # Add an elevation field for easy reference (the point is XYZ but
    # it's nice to have access to the elevation as a property)
    elevation_field = ogr.FieldDefn("elevation", ogr.OFTReal)
    outLayer.CreateField(elevation_field)
    # Add fields from input layer to output layer
    fields = []
    for i in range(pointLD.GetFieldCount()):
        fd = pointLD.GetFieldDefn(i)
        fields.append(fd)
    for fd in fields:
        print(f"Adding field {fd.name} of type {fd.GetTypeName()}.")
        outLayer.CreateField(fd)
    featureDefn = outLayer.GetLayerDefn()

    for feature in lyr:
        geom = feature.GetGeometryRef()
        pointXYRasterCRS = transform.TransformPoint(geom.GetX(), geom.GetY())
        mapX = pointXYRasterCRS[1]
        mapY = pointXYRasterCRS[0]
        pixcoords = gdal.ApplyGeoTransform(reverse, mapX, mapY)
        pixX = math.floor(pixcoords[0])
        pixY = math.floor(pixcoords[1])

        # Check if the pixel coordinates are within the raster bounds
        if 0 <= pixX < r.RasterXSize and 0 <= pixY < r.RasterYSize:
            # Valid coordinates, read the elevation value
            elevation = 0
            try:
                elevationstruct = band.ReadRaster(pixX, pixY, 1, 1)
                ele = struct.unpack(struct_data_type, elevationstruct)[0]
                elevation = round(ele, 1)
                if elevation == -9999 or elevation == -9999.0:
                    # It's almost certainly a nodata value, possibly over water
                    elevation = 0
            except Exception as e:
                log.error(f"Error reading elevation at point ({geom.GetX()}, {geom.GetY()}): {e}")
                elevation = 0
        else:
            # Point is outside the raster bounds, set elevation to 0 or another fallback value
            log.info(f"Point ({geom.GetX()}, {geom.GetY()}) is outside the raster bounds.")
            elevation = 0

        # Create a new point with elevation
        new_point = ogr.Geometry(ogr.wkbPoint)
        new_point.AddPoint(geom.GetX(), geom.GetY(), elevation)
        outFeature = ogr.Feature(featureDefn)
        outFeature.SetGeometry(new_point)
        outFeature.SetField("elevation", elevation)
        for fd in fields:
            val = feature.GetField(fd.name)
            outFeature.SetField(fd.name, val)
        outLayer.CreateFeature(outFeature)
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()

    p.add_argument("inraster", help="input DEM GeoTIFF raster file")
    p.add_argument("inpoints", help="input points geojson file")
    p.add_argument("outfile", help="output GeoJSON file")

    a = p.parse_args()

    inpointsfile = open(a.inpoints, "r")
    points = inpointsfile.read()

    writeout = add_elevation_from_dem(a.inraster, points, a.outfile)

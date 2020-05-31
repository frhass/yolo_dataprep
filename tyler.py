import os
import gdal
import sys
import fiona
from shapely.geometry import shape


# Directories
in_tif = sys.argv[1] # Input raster file
input_filename = os.path.splitext(os.path.basename(in_tif))[0]
in_path = os.path.dirname(os.path.abspath(in_tif)) + "\\"

out_path= str(sys.argv[2])+"\\" # Output folder


# Size of tiles
tile_size_x = 640
tile_size_y = 640

x = in_tif
ds = gdal.Open(in_tif)
band = ds.GetRasterBand(1)
xsize = band.XSize
ysize = band.YSize
output_filename = input_filename+"_"
#print(output_filename)
for i in range(0, xsize, tile_size_x):
    for j in range(0, ysize, tile_size_y):
        com_string = "gdal_translate -srcwin " + str(i) + ", " + str(j) + ", " + str(
            tile_size_x) + ", " + str(tile_size_y) + " " + str(in_path) + str(input_filename) + ".tif" + " " + str(
            out_path) + str(output_filename) + str(i) + "_" + str(j) + ".png"
        #print(com_string)
        os.system(com_string)

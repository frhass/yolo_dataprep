import os
import gdal
import sys
import fiona
from shapely.geometry import shape


# Directories
in_tif = sys.argv[1]
input_filename = os.path.splitext(os.path.basename(in_tif))[0]
in_path = os.path.dirname(os.path.abspath(in_tif)) + "\\"

shape_in = sys.argv[2]

out_path= str(sys.argv[3])+"\\"

#creating label and img folders
label_folder = os.path.join(out_path, "labels")
image_folder = os.path.join(out_path, "images")
if not os.path.exists(label_folder):
    os.makedirs(label_folder)
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# Size of tiles
tile_size_x = 416
tile_size_y = 416

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
            out_path) + "images\\" + str(output_filename) + str(i) + "_" + str(j) + ".png"
        #print(com_string)
        os.system(com_string)
        
        chipfile = str(out_path) + "images\\" + str(output_filename) + str(i) + "_" + str(j) + ".png"
        txtfile = str(out_path) + "labels\\" + str(output_filename) + str(i) + "_" + str(j) + ".txt"
        print("written", chipfile) 
        ds = gdal.Open(chipfile)
        geoTransform = ds.GetGeoTransform()
        minx = geoTransform[0]
        maxy = geoTransform[3]
        maxx = minx + geoTransform[1]*ds.RasterXSize
        miny = maxy + geoTransform[5]*ds.RasterYSize
        txt = open(txtfile,"w+")

        pix_res = geoTransform[1]
        x_res = geoTransform[1]
        y_res = geoTransform[5]
        
        with fiona.open(shape_in) as src:
            for f in src.filter(bbox=(minx, miny, maxx, maxy)):
                centroid = shape(f['geometry']).centroid
                x = centroid.x
                y = centroid.y

                x_index = int((x - minx) / x_res)
                y_index = int((y - maxy) / y_res)
                
                bounds = shape(f['geometry']).bounds
                bb_width = (bounds[2] - bounds[0]) / pix_res 
                bb_height = (bounds[3] - bounds[1]) / pix_res

                # formating bounding boxes to normalized coordinates
                norm_x = x_index / tile_size_x
                norm_y = y_index / tile_size_y
                norm_width = bb_width / tile_size_x
                norm_height = bb_height / tile_size_y
                
                print("box to file..:", "0 " + str(norm_x) + " " + str(norm_y) + " " + str(norm_width) + " " + str(norm_height))
                txt.write("0 " + str(norm_x) + " " + str(norm_y) + " " + str(norm_width) + " " + str(norm_height) + "\n")

        txt.close()


# Deleting empty label files        
for txtfile in os.listdir(label_folder):
    if os.path.getsize(os.path.join(label_folder, txtfile)) == 0:
        os.remove(os.path.join(label_folder, txtfile))

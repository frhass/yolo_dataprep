Preparing geospatial data for training a yolo object detection algortihm. 
Taking a raster tif file and ashapefile with training and converting these to image chips with corosponding labelfiles in darknet format.

Currently, the scripts handles all shapefeatures as same object class (0). If a shapefile is representing another object class, change the "0" at line 79 in the script.  <br />
The pixelsize of the output imagechips is specified at line 26 and 27. The script is set at slicing image to 416x416 pixels, fitting to the requirements of the yolo algoritm. 

The script is executed with the arguments: "input_tif.tif" "object_shapefile.shp" "output_folder"  <br />
Example:  <br />
python data2yolo.py "C:\path\to\tif\input_file.tif" "C:\path\to\object_shapefile\input_file.shp" "C:\path\to\output\folder"

In the output folder, images and labels are put into seperate folders. 

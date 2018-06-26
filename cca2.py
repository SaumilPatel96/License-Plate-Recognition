from skimage import measure
from skimage.measure import regionprops
import matplotlib.pyplot as plt 
import matplotlib.patches as patches
import localization
import numpy as np


# getting and grouping all connected regions
label_image = measure.label(localization.binary_car_image)


#license plate constraints
#plate_dimensions = (0.08 * label_image.shape[0], 0.2 * label_image.shape[0], 0.15 * label_image.shape[1], 0.4 * label_image.shape[1])
plate_dimensions = (0.08 * label_image.shape[0],  0.5 * label_image.shape[0], 0.04 * label_image.shape[1], 0.4* label_image.shape[1])
#plate_dimensions = (0.0 * label_image.shape[0],   label_image.shape[0], 0* label_image.shape[1],  label_image.shape[1])

print label_image.shape
min_height, max_height, min_width, max_width = plate_dimensions
plate_objects_cordinates = []
plate_like_objects = []
plate_pixel_averages = []
maxavg=0
lowestarray=[]
maxestarray=[]
differencearray= []
fig, (ax1,ax2,ax3) = plt.subplots(1,3)
ax1.imshow(localization.binary_car_image, cmap = "gray");

def gethighpixeldensity(label_image,min_value,max_value,region,ax):
	sumpixels = label_image.sum(axis=ax)
	minrange = sumpixels[min_value:]
	maxrange = sumpixels[max_value:]
	sumfrommin = sum(minrange)
	sumfrommax= sum(maxrange)
	totalsum=sumfrommin-sumfrommax
	pixelaverage=totalsum / region
	return pixelaverage

for region in regionprops(label_image):
	if region.area < 50:
		continue
	min_row, min_col, max_row, max_col = region.bbox
	region_height = max_row - min_row
	region_width = max_col - min_col
	if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and ((region_width/float(region_height))>1.5) and (region_width/float(region_height))<2.5:
		print region_width/float(region_height)
		pixelaveragecol=gethighpixeldensity(label_image,min_col,max_col,region_width,0)
		pixelaveragerow=gethighpixeldensity(label_image,min_row,max_row,region_height,1)
		sumpixelscol = label_image.sum(axis=0)
		sumpixelsrow = label_image.sum(axis=1)
		maxest=0
		lowest=999999
		for index,value in enumerate(sumpixelsrow):
			if index+min_row<=max_row:
				if sumpixelsrow[index+min_row]>maxest:
					maxest = sumpixelsrow[index+min_row]
				if sumpixelsrow[index+min_row]<lowest:
					lowest = sumpixelsrow[index+min_row]
		
		maxestarray.append(maxest)
		lowestarray.append(lowest)
		differencearray.append(maxest-lowest)

		ax2.plot(sumpixelscol)
		ax3.plot(sumpixelsrow)
		print "pixel average col ",pixelaveragecol
		print "pixel average row ", pixelaveragerow
		totalavg= (pixelaveragerow + pixelaveragecol) / 2

		plate_pixel_averages.append(pixelaveragecol)
		plate_like_objects.append(localization.binary_car_image[min_row:max_row, min_col:max_col])
		plate_objects_cordinates.append((min_row,min_col,max_row,max_col))
		# rectBorder = patches.Rectangle((min_col, min_row), max_col - min_col,max_row - min_row, edgecolor = 'red', linewidth = 2, fill = False)
		# ax1.add_patch(rectBorder)

		
print differencearray
maxindexrow = differencearray.index(max(differencearray))
maxindexcol = plate_pixel_averages.index(max(plate_pixel_averages))

if (maxindexcol == maxindexrow):
	maxindex = maxindexrow
else:
	maxindex=maxindexcol

print maxindexcol
print maxindexrow

rectBorder = patches.Rectangle((plate_objects_cordinates[maxindex][1], plate_objects_cordinates[maxindex][0]), plate_objects_cordinates[maxindex][3]-plate_objects_cordinates[maxindex][1],plate_objects_cordinates[maxindex][2]-plate_objects_cordinates[maxindex][0], edgecolor = 'red', linewidth = 2, fill = False)
ax1.add_patch(rectBorder)

plt.show()









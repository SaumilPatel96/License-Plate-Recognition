from skimage.io import imread
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt 

car_image = imread("car1.jpg", as_gray = True)

print "Image resolution is ",(car_image.shape)


gray_car_image = car_image * 255
fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4)
#fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.imshow(gray_car_image,cmap="gray")
threshold_value=threshold_otsu(gray_car_image)
binary_car_image = gray_car_image > threshold_value
print "thresh value = ", threshold_value
ax2.imshow(binary_car_image, cmap="gray")


sumpixelscol = gray_car_image.sum(axis=0)
sumpixelsrow = gray_car_image.sum(axis=1)
#sumcol = gray_car_image[1]
ax3.plot(sumpixelscol)
ax4.plot(sumpixelsrow)
#print sumcol

# print horizontal
# print vertical
# ax3.plot(horizontal)
# ax4.plot(vertical)


plt.show()



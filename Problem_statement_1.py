#!/usr/bin/env python

import cv2
import numpy as np

# Make sure that the image is in the same directory as this script
while True :
	img_name = raw_input("Enter the name of the image to be distorted\n")
	img_source = cv2.imread(img_name)
	if img_source is None :
		print "Image file does not exist, try again!"
	else :
		break

size = img_source.shape

# Array of source corner co-ordinates
array_input = np.array([[0,0],[size[1]-1,0],[size[1]-1,size[0]-1],[0,size[0]-1]],dtype=float)

print "\nEnter information about the four coordinates A,B,C,D"
coordinates = ['A','B','C','D']
array_output = np.zeros(shape=(4,2))

for i in range(len(coordinates)):
	print "Enter the X coordinate for point ", coordinates[i]
	x = input()
	print "Enter the Y coordinate for point ", coordinates[i]
	y = input()
	array_output[i] = [x,y]

# Calculate homography between input and output 
homograph, _ = cv2.findHomography(array_input, array_output)

output_size = array_output.max(axis=0) + 100

# Distort Image 
image_output = cv2.warpPerspective(img_source, homograph, (int(output_size[0]),int(output_size[1])))

cv2.imshow("Distorted Image", image_output)
cv2.waitKey(0)
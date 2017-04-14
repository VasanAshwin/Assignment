#!/usr/bin/env python

# The zooming algorithm used is nearest neighbour interpolation. More sophisticated 
# techniques can be used for better image quality of the scaled version. But since that
# is not the motive behind this assignment, it was't given much attention.

# Also, I did use Numpy to manipulate arrays, a diffcult proceduce if only restricted
# to Python Lists. Opencv is used only to load, mouse click and save events.

import cv2
import numpy as np

# Define functions
def mouse_handler(event, x, y, flags, data) :
    if event == cv2.EVENT_LBUTTONDOWN :
        cv2.circle(data['im'], (x,y),3, (0,0,255), 5, 16);
        cv2.imshow("Image", data['im']);
        if len(data['points']) < 1 :
            data['points'].append([x,y])

def get_one_point(im):
    
    # Set up data to send to mouse handler
    data = {}
    data['im'] = im.copy()
    data['points'] = []
    
    #Set the callback function for any mouse event
    cv2.imshow("Image",im)
    cv2.setMouseCallback("Image", mouse_handler, data)
    cv2.waitKey(0)
    
    # Convert array to np.array
    points = np.vstack(data['points']).astype(float)
    
    return points

# Make sure that the image is in the same directory as this script
while True :
	img_name = raw_input("Enter the name of the image to zoom into\n")
	img_source = cv2.imread(img_name)
	if img_source is None :
		print "Image file does not exist, try again!"
	else :
		break

size = img_source.shape

# Get the RGB channels in arrays
b, g, r    = img_source[:, :, 0], img_source[:, :, 1], img_source[:, :, 2]

# Get the scaling factor
while True:
   try:
       scaling_factor = int(raw_input('Enter scaling factor (between 2 and 10) >>> '))
   except ValueError:
       print 'That\'s not a number!'
   else:
       if 1 <= scaling_factor < 10: 
           break
       else:
           print 'Out of range. Try again'

# Scale the channels
b = np.repeat(b, scaling_factor, axis=1)
b = np.repeat(b, scaling_factor, axis=0)

g = np.repeat(g, scaling_factor, axis=1)
g = np.repeat(g, scaling_factor, axis=0)

r = np.repeat(r, scaling_factor, axis=1)
r = np.repeat(r, scaling_factor, axis=0)

# Set variables
new_size = b.shape

while True:
	# Ask for pivot point
	print "Click on the pivot point in the image and press Enter.."
	input_point = get_one_point(img_source)
	# Scale the point according to the scaling factor
	center_point = [x * scaling_factor for x in input_point]
	center_point = center_point[0]
	# Set the point to start clipping from
	start_point = [center_point[0]-int(size[0]/2),center_point[1]-int(size[1]/2)]
	if start_point[0] < 0 or start_point[1] < 0 :
		print "Point too close to the edges"
	else :
		break	

# Convert to int
start_point_x = int(start_point[0])
start_point_y = int(start_point[1])

# Clip the scaled channels to the size of the original photo keeping the point of focus in the center
b_out = b[start_point_x : start_point_x + size[0], start_point_y : start_point_y + size[1]]
g_out = g[start_point_x : start_point_x + size[0], start_point_y : start_point_y + size[1]]
r_out = r[start_point_x : start_point_x + size[0], start_point_y : start_point_y + size[1]]

# Stack the channels together
rgb = np.dstack((b_out, g_out, r_out))

# Save image
cv2.imwrite("Zoomed-image.png", rgb)
print "Zoomed image saved successfully!"

# Display
cv2.imshow("Image", rgb)
cv2.waitKey(0);


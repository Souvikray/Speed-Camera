import cv2
import numpy as np

# maximum corners we want to detect
MAX_NUM_CORNERS = 100
'''
To calculate PPC, take a flat surface for example a coin.Measure the diameter in cm.Then take
a picture of the coin with your camera, crop it out such that the upper and lower border of the
picture has the coin edge.Then check the property of the picture and get the height.This height
is basically the total no of pixels along the diameter of the coin.Now divide it with the
diameter measured earlier.This will give you the PPC.
'''

# capture video from a file
cap = cv2.VideoCapture('ironman3.jpg')  # we pass an image here
# read the first frame
ret, old_frame = cap.read()
# convert the frame to grayscale
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
'''
OpenCV has a function, cv2.goodFeaturesToTrack(). It finds N strongest corners in the image 
based on certain criteria by Shi-Tomasi method.All corners below quality level are rejected. 
Then it sorts the remaining corners based on quality in the descending order. Then function 
takes first strongest corner, throws away all the nearby corners in the range of minimum 
distance and returns N strongest corners.
'''
# get the corner points using Shi-Tomasi algorithm provided by the goodFeaturesToTrack method
prev_pts = cv2.goodFeaturesToTrack(old_gray, MAX_NUM_CORNERS, 0.5, 20, 7)  # (image, max_corners, quality_level, min_distance, block_size)

for pt in prev_pts:
    # This function returns a flattened one-dimensional array
    x, y = pt.ravel()
    # circle the corners on the image
    cv2.circle(old_frame, (x, y), 5, (0, 255, 0), -1)

# show the frame
cv2.imshow("Corners", old_frame)
# wait until the user explicitly closes the window
cv2.waitKey(0)

# destroy all the windows
cv2.destroyAllWindows()
# release any resources
cap.release()


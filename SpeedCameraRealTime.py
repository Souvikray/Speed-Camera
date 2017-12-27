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
# get the pixel per cm (camera specific)
PIXEL_PER_CM = 549
# get the FPM of the camera
FPS = 30
# set a distance threshold
DISTANCE_THRESHOLD = 10
# set a refresh rate such that the speed calculation text clears out after certain frames to avoid messy output
REFRESH_RATE = 10
# track the number of frames
frame_count = 0


# function to calculate the euclidean distance
def euclidean_distance(p, q):
    # convert the coordinates into numpy array
    p = np.array(p)
    q = np.array(q)
    # return the euclidean distance between two points
    return np.linalg.norm(p-q)

# generate random colors for the visualization
# any color in opencv is in BGR format
colors = np.random.randint(0, 255, (MAX_NUM_CORNERS, 3))  # (num1, num2, dimension)
# capture video from a file
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('sampleVideo3.mp4')
#cap = cv2.VideoCapture('bira.jpg')
# read the first frame
ret, old_frame = cap.read()
frame_count += 1
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
prev_pts = cv2.goodFeaturesToTrack(old_gray, MAX_NUM_CORNERS, 0.7, 7, 7)  # (image, max_corners, quality_level, min_distance, block_size)
'''
for pt in prev_pts:
    # This function returns a flattened one-dimensional array
    x, y = pt.ravel()
    # circle the corners on the image
    cv2.circle(old_frame, (x, y), 5, (0, 255, 0), -1)

# show the frame
cv2.imshow("Corners", old_frame)
# wait until the user explicitly closes the window
cv2.waitKey(0)
'''
# We cannot draw the visualizations directly on the frame, so we need to define a mask
# the mask must have the same dimensions as that of the frame
mask = np.zeros_like(old_frame)
# declare a new mask for writing speed result on it
mask_speed = np.zeros_like(old_frame)
while True:
    # get each frame of the video
    ret, frame = cap.read()
    if ret is True:
        # every tenth frame, clear out the mask_speed
        if frame_count % REFRESH_RATE == 0:
            mask_speed.fill(0)
        # increment the frame count by 1
        frame_count += 1
        # convert the frame to grayscale
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # show the frame
        #cv2.imshow("Video", frame)
        '''
        OpenCV provides a function cv2.calcOpticalFlowPyrLK().Here, we track some points 
        in a video.To decide the points, we use cv2.goodFeaturesToTrack(). We take the first 
        frame, detect some Shi-Tomasi corner points in it, then we iteratively track those 
        points using Lucas-Kanade optical flow. For the function cv2.calcOpticalFlowPyrLK() 
        we pass the previous frame, previous points and next frame. It returns next points 
        along with some status numbers which has a value of 1 if next point is found, 
        else zero. We iteratively pass these next points as previous points in next step. 
        '''
        # calcOpticalFlowPyrLK(previous_frame, next_frame, previous_points, search_window_size,
        #                        max_level, termination_criteria, no_of_iterations, epsilon_value)
        next_pts, status, _ = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, prev_pts, (15, 15), 2,
                                                       (cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 10, 0.03))

# ----------------------------------MINOR CHANGE---------------------------------------------------
        # get the next points only if they exist
        # status = 1 means the points exist and 0 means otherwise
        if status.any() == 1:
            next_pts_exist = next_pts[status == 1]
            prev_pts_exist = prev_pts[status == 1]
        # if no next points exist
        else:
            break
# ----------------------------------MINOR CHANGE--------------------------------------------------

        # draw the visualizations
        # we draw a line between the old corner points and the new corner points
        for i, (next, prev) in enumerate(list(zip(next_pts_exist, prev_pts_exist))):
            # This function returns a flattened one-dimensional array
            a, b = next.ravel()
            c, d = prev.ravel()

            '''
            In order to display the speed of the motion of an object in the video, we have to
            first focus on those points which have actually changed by a considerable distance.
            Since for a moving object, the initial and final position of the object constitutes
            two different points, we are assured those points are part of the moving object.
            However, for all other points for example the points at the background, there will
            hardly be any change in the point's position.So the corner points in the background
            will more or less remain constant.
            '''
            # calculate the euclidean distance between the old and new corner points
            distance = euclidean_distance((a, b), (c, d))
            # if the euclidean distance between two points is greater than the threshold defined
            if distance > DISTANCE_THRESHOLD:
                # draw the line connecting the points on the mask
                cv2.line(mask, (a, b), (c, d), colors[i].tolist(), 2)  # (frame, start_point, end_point, color, thickness)
                # draw the circle on the new corner points
                cv2.circle(frame, (a, b), 5, colors[i].tolist(), -1)  # (frame, coordinate, radius, color, thickness)
                speed = str((distance / PIXEL_PER_CM) * FPS) + " cm/s"
                cv2.putText(mask_speed, speed, (a, b), cv2.FONT_HERSHEY_TRIPLEX, 0.5, colors[i].tolist())
                print(speed)
        # combine the mask and the frame to see the circle and the visualizations
        frame_final = cv2.add(frame, mask)
        frame_final = cv2.add(frame_final, mask_speed)

        # make the current frame as the previous frame
        old_gray = frame_gray.copy()
        # set the current points as the previous points
        # give the points array the appropriate structure if structure is broken
        prev_pts = next_pts_exist.reshape(-1, 1, 2)
        # display the frame
        cv2.imshow("Optical Flow", frame_final)
        # when key 'q' is pressed, break out of the loop
        if cv2.waitKey(1) & 0xFF is ord('q'):
            break
    else:
        break

# destroy all the windows
cv2.destroyAllWindows()
# release any resources
cap.release()


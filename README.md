I have built a speed camera that can detect and measure the speed of a moving object in a video or real time.The idea behind speed camera is Optical Flow.First we need to understand how a point is percieved in an image and in a video.

In an image, we consider only the coordinate of a point ie a point's position with respect to x and y axis.So we get an equation like below

***I(x, y) = P***

(x, y) - coordinate of a point
P - pixel intensity

However in a video, we consider not just the point's coordinate but also the time ie at what interval or at which frame does the point exist.The equaton we get is below

***I(x, y, t) = P***

(x, y) - coordinate of a point or spatial position
P - pixel intensity
t - temporal or when in a video

Based on this concept, we use a technique called Optical Flow.

**Optical Flow**

It is a computer vision technique to track the apparent motion of an object in a video (continuos frames).So if we have three consecutive frames and we want to track a point or an object through the frames, we use optical flow to accomplish the task.So the point will be tracked as the frames come by.

Following are the assumptions Optical Flow makes

1 Pixel intensity doesn't rapidly change between consecutive frames.

2 Group of pixels move together

![Alt text](https://github.com/Souvikray/Speed-Camera/blob/master/screenshot2.png?raw=true "Optional Title")

As we can see in the above diagram, in the first frame the point had a position (x1, y1) and in the next frame the point had a position (x2, y2).So we need to find the displacement of the point to track it.

The above equation for Optical flow is based on the fact that pixel itensity doesn't change between consecutive frames (first assumption).So we apply the equation discussed above for videos in the two consecutive frames and equate it.This gives us the Optical Flow equation.On solving it further using calculus, we get the final equation below.

*Ix*u + Iy*v + It = 0*

Ix - by much the frame has changed with respect to x axis

Iy - by much the frame has changed with respect to y axis

It - by much the frame has changed with respect to time

Ix, Iy and It can be found it but we need to find u and v so that we can calculate the displacement of the point.It can be computed by using the Lucal-Kanade method.It assumes that the displacement of the image contents between two nearby frames is small and approximately constant within a neighborhood of the point p under consideration.But there is a problem.It doesn't work well for the second assumption.So if there is a huge displacement along x and y axis, the tracking of the point becomes inaccurate.

To fix this we use a technique called image pyramid.

![Alt text](https://github.com/Souvikray/Speed-Camera/blob/master/screenshot3.png?raw=true "Optional Title")

So to account for large value of u and v, image pyramid technique is used where we shrink the image at each level so that it becomes smaller and smaller.So the apparent displacement u and v shrinks too and at certain level we can easily compute the values using the Lucas-Kanade method.

But there is another problem.When we say track a point across the frames, which exact pixel to track out of all the pixels.If we try to search the particular pixel out of all the pixels, it will be very slow and inefficient.So we need some good features to track the point or the pixel.

We use a technique called Shi-Tomasi Corner detection.Let us understand what do we mean by corners.

![Alt text](https://github.com/Souvikray/Speed-Camera/blob/master/screenshot4.gif?raw=true "Optional Title")

![Alt text](https://github.com/Souvikray/Speed-Camera/blob/master/screenshot5.jpg?raw=true "Optional Title")

A corner can be defined as the intersection of two edges.So we identify certain corners in an image or frame and then we draw the flow patterns from these corners.Now instead of looking at all the pixels, we just look at certain corners in the frame and since the object in motion too will have certain corners, we can just focus on these corners and save time by discarding rest of the pixel details.

Now let us see the above algorithms and techniques in action and determine the optical flow of a moving object.

Below is a picture on which we will apply the Shi-Tomasi Corner Detection algorithm to determine the corners in the image.

![Alt text](https://github.com/Souvikray/Speed-Camera/blob/master/ironman3.jpg?raw=true "Optional Title")

After applying the Shi-Tomasi Corner Detection algorithm, we get the corners below (all corners are not included)

![Alt text](https://github.com/Souvikray/Speed-Camera/blob/master/screenshot1.png?raw=true "Optional Title")

Now let us apply the Optical Flow technique on a sample video and see the results.So in the video, apart from tracking the points of an object in motion, it also calculates the speed of the movement of the object.

![Alt text](https://github.com/Souvikray/Speed-Camera/blob/master/SpeedCameraVideo.gif?raw=true "Optional Title")

Let us try out the Optical Flow technique in a real time environment.So as before I will be moving a pen and it should detect and track the movement of the pen.

![Alt text](https://github.com/Souvikray/Speed-Camera/blob/master/SpeedCameraRealTime.gif?raw=true "Optional Title")






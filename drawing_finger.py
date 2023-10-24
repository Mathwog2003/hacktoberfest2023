import numpy as np
import cv2
from collections import deque
import re

#default called trackbar function 
def setValues(x):
   print("")
KEYBOARD = [["1","2","3","4","5","6","7","8","9","0"],["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
["a", "s", "d", "f", "g", "h", "j", "k", "l"," "], ["z", "x", "c", "v", "b", "n", "m", "\n", "\b" ,".."]]
v = None
c= None
reader = None
# Creating the trackbars needed for adjusting the marker colour
cv2.namedWindow("Color detectors")
cv2.createTrackbar("Upper Hue", "Color detectors", 100, 180,setValues)
cv2.createTrackbar("Upper Saturation", "Color detectors", 255, 255,setValues)
cv2.createTrackbar("Upper Value", "Color detectors", 255, 255,setValues)
cv2.createTrackbar("Lower Hue", "Color detectors", 40, 180,setValues)
cv2.createTrackbar("Lower Saturation", "Color detectors", 100, 255,setValues)
cv2.createTrackbar("Lower Value", "Color detectors", 100, 255,setValues)


# Giving different arrays to handle colour points of different colour
bpoints = [deque(maxlen=1024)]

# These indexes will be used to mark the points in particular arrays of specific colour
blue_index = 0

#The kernel to be used for dilation purpose 
kernel = np.ones((5,5),np.uint8)

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

# Here is code for Canvas setup
paintWindow = np.zeros((471,636,3)) + 255
paintWindow = cv2.rectangle(paintWindow, (40,1), (150,65), (0,0,0), 2)
paintWindow = cv2.rectangle(paintWindow, (150,1), (265,65), colors[0], -1)
paintWindow = cv2.rectangle(paintWindow, (265,1), (380,65), colors[1], -1)
paintWindow = cv2.rectangle(paintWindow, (380,1), (495,65), colors[2], -1)
paintWindow = cv2.rectangle(paintWindow, (495,1), (600,65), colors[3], -1)

cv2.putText(paintWindow, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)
cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)


# Loading the default webcam of PC.
cap = cv2.VideoCapture(0)

# Keep looping
while True:
    # Reading the frame from the camera
    ret, frame = cap.read()
    #Flipping the frame to see same side of yours
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    u_hue = cv2.getTrackbarPos("Upper Hue", "Color detectors")
    u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
    u_value = cv2.getTrackbarPos("Upper Value", "Color detectors")
    l_hue = cv2.getTrackbarPos("Lower Hue", "Color detectors")
    l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
    l_value = cv2.getTrackbarPos("Lower Value", "Color detectors")
    Upper_hsv = np.array([u_hue,u_saturation,u_value])
    Lower_hsv = np.array([l_hue,l_saturation,l_value])
    

    # Adding the colour buttons to the live frame for colour access
    frame = cv2.rectangle(frame, (40,1), (140,65), (122,122,122), -1)
    frame = cv2.rectangle(frame, (160,1), (255,65), colors[0], -1)
    frame = cv2.rectangle(frame, (275,1), (370,65), colors[1], -1)
    frame = cv2.rectangle(frame, (390,1), (485,65), colors[2], -1)
    frame = cv2.rectangle(frame, (505,1), (600,65), colors[3], -1)
    cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)


    # Identifying the pointer by making its mask
    Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
    Mask = cv2.erode(Mask, kernel, iterations=1)
    Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
    Mask = cv2.dilate(Mask, kernel, iterations=1)

    # Find contours for the pointer after idetifying it
    cnts,_ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.imshow("frame", cnts)
    center = None

    # Ifthe contours are formed
    if len(cnts) > 0:
    	# sorting the contours to find biggest 
        cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        # Get the radius of the enclosing circle around the found contour
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        # Draw the circle around the contour
        
        # Calculating the center of the detected contour
        M = cv2.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']), colorIndex)

        # Now checking if the user wants to click on any button above the screen 
        if center[1] <= 65:
            if 40 <= center[0] <= 140: # Clear Button
                bpoints = [deque(maxlen=2048)]
                
                paintWindow[:,:,:] = 255
            elif 160 <= center[0] <= 255:
                    colorIndex = 0 # Blue
            elif 275 <= center[0] <= 370:
                    colorIndex = 1 # Green
            elif 390 <= center[0] <= 485:
                    colorIndex = 2 # Red
            elif 505 <= center[0] <= 600:
                    colorIndex = 3 # Yellow
        else :
            bpoints[0].appendleft(center)
            
    # Append the next deques when nothing is detected to avois messing up
    else:
        bpoints.append(deque(maxlen=2048))

    # Draw lines of all the colors on the canvas and frame 
    points = [bpoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k - 1][:2], points[i][j][k][:2], colors[points[i][j][k][-1]], 2)
                cv2.line(paintWindow, points[i][j][k - 1][:2], points[i][j][k][:2], colors[i], 2)
    """           
    cv2.rectangle(frame, (98,148), (502,402), (0,0,0), 2)
    cv2.rectangle(frame, (100,150), (500, 200), (120,120,120), -1) 
    cv2.rectangle(frame, (100,200), (500, 400), (55,55,55), -1)
    cv2.line(frame, (98, 199), (502,199), (0,0,0), 2)
    for x in range(10):
        for y in range(4):
            cv2.rectangle(frame, (105 + (x*40),210 + (y*50)), (135 + (x*40), 240 + (y*50)),(0,0,0), 1)
            cv2.rectangle(frame, (105 + (x*40),210 + (y*50)), (135 + (x*40), 240 + (y*50)),(200,200,200), -1)
            cv2.putText(frame, KEYBOARD[y][x], (112 + (x*40),230 + (y*50)), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
    
    
    if center is not(None):
        if 100<center[0]<500 and 200<center[1]<400:
            xtext = (center[0] - 105)/40
            ytext = (center[1] - 210)/50
            if int(xtext)+0.75 > xtext and int(ytext) + 0.6 > ytext:
                c = KEYBOARD[int(ytext)][int(xtext)]
            else:
                v = None
                c = None
            if c == "\b" and c != v:
                reader = reader[:-1]
                f = open("ocv writer.txt", 'w')
                f.write(reader)
                f.close()
            f = open("ocv writer.txt", 'a')
            if c != v and c != "\b":  
                f.write(c)
            elif c == "\b":
                v = c
               
            f.close()
            if v != c and c != "\b":
                f = open("ocv writer.txt", 'r')
                reader = f.read()
                f.close()
                v = c
        else:
            v = None
    else:
        v = None 
    cv2.putText(frame, reader, (110, 180), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,0), 2)   
    """

    cv2.line(frame, (150,250), (350, 250), (255,255,255), 2)
    cv2.line(frame, (250,150), (250, 350), (255,255,255), 2)
    eq = input("Please enter a equation")

    ident = re.compile(r'(.*)[=](.*)')

    yeq = ident.sub(r'\1', eq)
    xeq = ident.sub(r'\2', eq)

    for xval in range(-100,100):
        x = xval
        final = eval(xeq)
        x = xval + 1
        final1 = eval(xeq)
        cv2.line(frame, (xval*10+250, -final+250), ((xval+1)*10+251, -final1 +250 ), (255,255,255),1)

    if center is not(None):
        cv2.circle(frame, (center[0], center[1]), 3, (0, 255, 255), -1)
    # Show all the windows
    cv2.imshow("Tracking", frame)
    cv2.imshow("Paint", paintWindow)
    cv2.imshow("mask",Mask)

	# If the 'q' key is pressed then stop the application 
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and all resources
cap.release()
cv2.destroyAllWindows()

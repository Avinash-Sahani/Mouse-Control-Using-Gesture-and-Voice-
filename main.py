
import cv2
import numpy as np
from pynput.mouse import Button, Controller
from  tkinter import  *
from PIL import ImageTk, Image
from tkinter.ttk import *
import alexa
#part 1 set segmentation and save data in file
#for mouse

alexa_assistant=alexa.Alexa()
root = Tk()

sx = root.winfo_screenwidth()

sy = root.winfo_screenheight()
(camx,camy)=(320,240)
photo = ImageTk.PhotoImage(Image.open(r"alexamic.jpg"))
def nothing(x):
    pass
 
cap = cv2.VideoCapture(0)  #cv2.VideoCapture(2,cv2.CAP_DSHOW)
cap.set(3,1280)
cap.set(4,720)

cv2.namedWindow("Trackbars")
 
cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)
 
 
while True:
    _, frame = cap.read()
    frame = cv2.flip( frame, 1 ) 


    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
 
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
 
    # set the lower and upper range according to the value selected by the trackbar.
    lower_range = np.array([l_h, l_s, l_v])
    upper_range = np.array([u_h, u_s, u_v])
    
    # filter and get the binary mask, where white represents your target color.
    mask = cv2.inRange(hsv, lower_range, upper_range)
 
    # optionally you can also show the real part of the target color
    res = cv2.bitwise_and(frame, frame, mask=mask)
    
    mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    
    # stack all frames and show it
    stacked = np.hstack((mask_3,frame,res))
    cv2.imshow('Trackbars',cv2.resize(stacked,None,fx=0.4,fy=0.4))
 
    key = cv2.waitKey(1)
    if key == 27:
        break
        
    if key == ord('s'):
        thearray = [[l_h,l_s,l_v],[u_h, u_s, u_v]]
        print(thearray)
        
        # Also save this array as penval.npy
        np.save('/penval',thearray)    #for juypter notebbok
        break
    
cap.release()
cv2.destroyAllWindows()


#part 2
# Now you may have noticed that there is some noise in the above program, this can easily be removed by morphological operations.
# This variable determines if we want to load color range from memory or use the ones defined in notebook.

useload = True
# If true then load color range from memory
if useload:
    print("segmentation")
    penval = np.load('/penval.npy')

cap = cv2.VideoCapture(2,cv2.CAP_DSHOW)
cap.set(3,1280)
cap.set(4,720)

# kernel for morphological operations
kernel = np.ones((5,5),np.uint8)

while(1):
    
    # Take each frame and flip it
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip( frame, 1 )

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # If you're reading from memory then load the upper and lower ranges from there
    if useload:
            lower_range = penval[0]
            upper_range = penval[1]
            
    # Otherwise define your own custom values for upper and lower range.
    else:             
       lower_range  = np.array([26,80,147])
       upper_range = np.array([81,255,255])
    
    mask = cv2.inRange(hsv, lower_range, upper_range)
    
    # perform the morphological operations to get rid of the noise
    mask = cv2.erode(mask,kernel,iterations = 1)
    mask = cv2.dilate(mask,kernel,iterations = 2)

   
    res = cv2.bitwise_and(frame,frame, mask= mask)

    mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    
    # stack all frames and show it
    stacked = np.hstack((mask_3,frame,res))
    cv2.imshow('Trackbars',cv2.resize(stacked,None,fx=0.4,fy=0.4))
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
cap.release()


#part 3
# Now that we have got a decent mask we can use it detect our pen using contour detection, in fact we will draw a bonding box around it.
# This variable determines if we want to load color range from memory or use the ones defined now by you.
useload = True
# If true then load color range from memory
if useload:
    print("Track the pen")
    penval = np.load('/penval.npy')

cap = cv2.VideoCapture(0) #cv2.VideoCapture(2,cv2.CAP_DSHOW)
cap.set(3,1280)
cap.set(4,720)

# kernel for morphological operations
kernel = np.ones((5,5),np.uint8)

# set the window to autosize so we can view this full screen.
cv2.namedWindow('image', cv2.WINDOW_NORMAL)

# this threshold is used to filter noise, the contour area must be bigger than this to qualify as an actual contour.
noiseth = 500
Bool = True;
while(Bool):
    
    # Take each frame and flip it
    _, frame = cap.read()
    frame = cv2.flip( frame, 1 )

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # If you're reading from memory then load the upper and lower ranges from there
    if useload:
            lower_range = penval[0]
            upper_range = penval[1]
            
    # Otherwise define your own custom values for upper and lower range.
    else:             
       lower_range  = np.array([26,80,147])
       upper_range = np.array([81,255,255])
    
    mask = cv2.inRange(hsv, lower_range, upper_range)
    
    # perform the morphological operations to get rid of the noise
    mask = cv2.erode(mask,kernel,iterations = 1)
    mask = cv2.dilate(mask,kernel,iterations = 2)
    
    # detect contour.
    contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    # Make sure there was a contour present and also its size was bigger than some threshold.
    if contours and cv2.contourArea(max(contours, key = cv2.contourArea)) > noiseth:
        
        # grab the biggest contour
        c = max(contours, key = cv2.contourArea)
        
        # Draw a bounding box around it.
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)        

    cv2.imshow('image',frame)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27 or ord('n'):
        Bool= False;
        break
cv2.destroyAllWindows()
cap.release()




#part 4  Drawing
# Now that everything is set and we are easily able to track our target object, its time to use this object to draw on the frame, now we can easily do this by combining the above program with our mouse drawing on Gui program, so what we'll do is instead of drawing with the mouse by taking its x,y coordinates we will draw with the object by taking the corner x,y coordinates of our object. You can also track through the object's mid point.
print("Drawing Part ")
useload = True
if useload:
    penval = np.load('/penval.npy')
cap = cv2.VideoCapture(0) #cv2.VideoCapture(2,cv2.CAP_DSHOW)
cap.set(3,1280)
cap.set(4,720)
kernel = np.ones((5,5),np.uint8)
# This is the canvas on which we will draw upon
canvas=None
# initilize x1,y1 points
x1,y1=0,0
# threshold for noise
noiseth = 500
Bool = True;
while(Bool):
    # Take each frame and flip it
    _, frame = cap.read()
    frame = cv2.flip( frame, 1 )
    
    # initilize the canvas as a black image
    if canvas is None:
        canvas = np.zeros_like(frame)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # If you're reading from memory then load the upper and lower ranges from there
    if useload:
            lower_range = penval[0]
            upper_range = penval[1]
            
    # Otherwise define your own custom values for upper and lower range.
    else:             
       lower_range  = np.array([26,80,147])
       upper_range = np.array([81,255,255])
    
    mask = cv2.inRange(hsv, lower_range, upper_range)
    
    # perform the morphological operations to get rid of the noise
    mask = cv2.erode(mask,kernel,iterations = 1)
    mask = cv2.dilate(mask,kernel,iterations = 2)
    
    # detect contour.
    contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    # Make sure there was a contour present and also its size was bigger than some threshold.
    if contours and cv2.contourArea(max(contours, key = cv2.contourArea)) > noiseth:
                
        c = max(contours, key = cv2.contourArea)    
        x2,y2,w,h = cv2.boundingRect(c)
        
        # if there were no previous points then save the detected x2,y2 as x1,y1. (logic similar to x1 = None)
        if x1 == 0 and y1 == 0:
            x1,y1= x2,y2
            
        else:
            # draw the line on the canvas
            canvas = cv2.line(canvas, (x1,y1),(x2,y2), [255,0,0], 4)
        
        # after the line is drawn the new points become the previous points.
        x1,y1= x2,y2

    else:
        # if there were no contours detected then make x1,y1 = 0
        x1,y1 =0,0
    
    # Merge the canvas and the frame.
    frame = cv2.add(frame,canvas)
    
    # Optionally stack both and show them, otherwise you just need to show the frame.
    stacked = np.hstack((canvas,frame))
    cv2.imshow('Trackbars',cv2.resize(stacked,None,fx=0.6,fy=0.6))

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
        
    # When c is pressed clear the canvas
    if k == ord('c') or key == ord('n'):
        Bool = False;
        canvas = None

cv2.destroyAllWindows()
cap.release()



#Part 5
# A) Drawing
# B) Mouse gesture
# c) Integrate both feature together

# In the above script we clear up the screen when the user presses `c` but lets automate this too, so one easy way we can do this is by detecting when the target object is too close to the camera and then if its too close we clear up the screen. (size of contour increases as it comes closer to the camera ).
# One other thing we will do is that we will also warn the user that we are about to clear the screen in a few seconds so he/she can take the object out of the frame.

import time
from pynput.mouse import Button, Controller
mouse = Controller()

print("Drawing , eraser and mouse part")
Bool = False;

                     #Now for mouse code

CLICK = CLICK_MESSAGE = MOVEMENT_START = None
#we will need these variables and objects, mouse object is for mouse movements
# and to get the screen resolution we need an wx app then
# we can use the wx.GetDisplaySize() to get the screen resolution.
#lastly we are setting some variables camx, camy to set the captured image resolution. we will be using it later in image resize function
lowerBound=np.array([33,80,40])
upperBound=np.array([102,255,255])

cam= cv2.VideoCapture(0)

kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))
pinchFlag=0

                   #code for painting
useload = True
if useload:
    penval = np.load('/penval.npy')
cap =  cv2.VideoCapture(0)# cv2.VideoCapture(2,cv2.CAP_DSHOW)
cap.set(3,1280)
cap.set(4,720)

kernel = np.ones((5,5),np.uint8)
# making window size adjustable
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
# This is the canvas on which we will draw upon
canvas=None
# initilize x1,y1 points
x1,y1=0,0
# threshold for noise
noiseth = 500
# threshold for eraser, the size of the contour must be bigger than for us to clear the canvas
eraserthresh = 40000
# A varaibel which tells when to clear canvas
clear = False
pinchFlag=0
k=None
#Function To Ignore a key
def ignorekey():
    pass

while(1):
                  #for painting code

    # Take each frame and flip it
    _, frame = cap.read()
    frame = cv2.flip(frame, 1 )

    # initilize the canvas as a black image
    if canvas is None:
        canvas = np.zeros_like(frame)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # If you're reading from memory then load the upper and lower ranges from there
    if useload:
            lower_range = penval[0]
            upper_range = penval[1]
            
    # Otherwise define your own custom values for upper and lower range.
    else:             
       lower_range  = np.array([26,80,147])
       upper_range = np.array([81,255,255])
    
    mask = cv2.inRange(hsv, lower_range, upper_range)
    
    # perform the morphological operations to get rid of the noise
    mask = cv2.erode(mask,kernel,iterations = 1)
    mask = cv2.dilate(mask,kernel,iterations = 2)
    
    # detect contour.
    contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

                                 #for mouse code
    # color detection code
    ret, img = cam.read()
    img = cv2.resize(img, (340, 220))

                           # convert BGR to HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

                           # create the Mask
    mask2 = cv2.inRange(imgHSV, lowerBound, upperBound)

                           # morphology
    maskOpen = cv2.morphologyEx(mask2, cv2.MORPH_OPEN, kernelOpen)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)

    maskFinal = maskClose
    conts, h = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

                        #if object Bool is False then it is pen.
        #If we make clear screen then it turn into mouse again if we make clear screen then it turn into pen
    if Bool == False:
           # Make sure there was a contour present and also its size was bigger than some threshold.
        if contours and cv2.contourArea(max(contours, key = cv2.contourArea)) > noiseth:
            c = max(contours, key = cv2.contourArea)    
            x2,y2,w,h = cv2.boundingRect(c)

           # get the area of the contour
            area = cv2.contourArea(c)      
            # if there were no previous points then save the detected x2,y2 as x1,y1. (logic similar to x1 = None)
            if x1 == 0 and y1 == 0:
                x1,y1= x2,y2        
            else:
               # draw the line on the canvas
                canvas = cv2.line(canvas, (x1,y1),(x2,y2), [255,0,0], 5)

                # after the line is drawn the new points become the previous points.
            x1,y1= x2,y2
               # Now if the area is greater than the eraser threshold then set the clear variable to True
            if area > eraserthresh:
                cv2.putText(canvas,'Turn into pen ',(100,200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 5, cv2.LINE_AA)
                Bool = True;   #turn into mouse
                clear = True
        else:
               # if there were no contours detected then make x1,y1 = 0
            x1,y1 =0,0
               # Now this piece of code is just for smooth drawing. (Optional)
        _, mask = cv2.threshold(cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY), 20, 255, cv2.THRESH_BINARY)
        foreground = cv2.bitwise_and(canvas, canvas, mask=mask)
        background = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(mask))
        frame = cv2.add(foreground, background)
        cv2.imshow('image', frame)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
                   # Clear the canvas after 1 second, if the clear variable is true
        if clear == True:
            time.sleep(1)
            canvas = None
                   # and then set clear to false
            clear = False
            # close all windows
            cv2.destroyAllWindows()

                            #Bool is false then it is mouse
    elif Bool == True:
        # Now logic code for object if two object then move else one for select or click
        # logic for the open gesture, move mouse without click
        print(len(conts))
        if contours and cv2.contourArea(max(contours, key=cv2.contourArea)) > noiseth:
            c = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(c)

        if (len(conts) == 2):
            if (pinchFlag == 1):
                pinchFlag = 0
                mouse.release(Button.left)
            x1, y1, w1, h1 = cv2.boundingRect(conts[0])
            x2, y2, w2, h2 = cv2.boundingRect(conts[1])
            cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 2)
            cv2.rectangle(img, (x2, y2), (x2 + w2, y2 + h2), (255, 0, 0), 2)
            cx1 = x1 + w1 / 2
            cy1 = y1 + h1 / 2
            cx2 = x2 + w2 / 2
            cy2 = y2 + h2 / 2
            cx = (cx1 + cx2) / 2
            cy = (cy1 + cy2) / 2
            cv2.line(img, (int(cx1), int(cy1)), (int(cx2), int(cy2)), (255, 0, 0), 2)
            cv2.circle(img, (int(cx), int(cy)), 2, (0, 0, 255), 2)
            mouseLoc = (sx - (cx * sx / camx), cy * sy / camy)
            mouse.position = mouseLoc
            print(mouseLoc)
            while mouse.position != mouseLoc:
                pass
        # logic for close gesture
        elif (len(conts) == 1):
            x, y, w, h = cv2.boundingRect(conts[0])
            if (pinchFlag == 0):
                pinchFlag = 1
                mouse.press(Button.left)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cx = x + w / 2
            cy = y + h / 2
            cv2.circle(img, (int(cx), int(cy)), int((w + h) / 4), (0, 0, 255), 2)
            mouseLoc = (sx - (cx * sx / camx), cy * sy / camy)
            mouse.position = mouseLoc
            while mouse.position != mouseLoc:
                pass
        elif(len(conts)==3):
            # twice on macOS
            # Scroll two steps down
            mouse.scroll(0, 2)
        elif (len(conts)==4 or k==ord('a')):
            cv2.destroyAllWindows()
            root.overrideredirect(1)
            Button(root, text='Click Me !', image=photo, command=lambda: alexa_assistant.start_assistant()).pack(
            side=TOP)
            root.bind('<Alt-Key-F4>', ignorekey())
            root.mainloop()

        if area > eraserthresh:
            cv2.putText(canvas,'Turn into panting',(100,200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 5, cv2.LINE_AA)
            clear = True
                   # Turn into pen sleep for one second
        if clear == True:
            time.sleep(1)
            Bool = False;     #turn into pen
            canvas = None
                   # and then set clear to false
            clear = False
            # close all windows
            cv2.destroyAllWindows()

        cv2.drawContours(img, conts, -1, (255, 0, 0), 3)
        for i in range(len(conts)):
            x, y, w, h = cv2.boundingRect(conts[i])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.imshow("cam", img)
        cv2.waitKey(5)

cv2.destroyAllWindows()
cap.release()






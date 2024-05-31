import cv2
import numpy as np
cam=cv2.VideoCapture(0)
cam.set(3,1080)
cam.set(4,720)
cam.set(10,10)
myColors=[[105,62,59,139,191,255]]
myColorv=[[255,0,0]]
circles=[]
def findColor(img):
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    for i in range(len(myColors)):
        lower=np.array(myColors[i][:3])
        upper=np.array(myColors[i][3:])
        mask=cv2.inRange(imgHSV,lower,upper)
        x,y=getContours(mask)
        circles.append([(x,y),myColorv[i]])

def getContours(img):
    contours,hist=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    if len(contours)==0:
        return
    cnt=[]
    bigArea=0
    x,y,w=0,0,0
    for i in contours:
        area=cv2.contourArea(i)
        peri=cv2.arcLength(i,True)
        edges=cv2.approxPolyDP(i,0.02*peri,True)
        if area>bigArea:
          cnt=edges
          bigArea=area
    x,y,w,h=cv2.boundingRect(cnt)
    return x+w//2,y

while 1:
    hst,img=cam.read()
    imgc=img.copy()
    cv2.putText(imgc,"Quit-q",(img.shape[1]-60,img.shape[0]-20),cv2.FONT_HERSHEY_COMPLEX,0.51,(0,0,0))
    findColor(img)
    for i in circles:
        cv2.circle(imgc,i[0],10,i[1],cv2.FILLED)
    cv2.imshow("cnt",imgc)
    if cv2.waitKey(1)==ord("q"):
        break
cv2.destroyAllWindows()
    
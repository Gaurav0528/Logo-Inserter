import cv2 as cv
import sys
def image(frame):
    contour , hierarchies = cv.findContours(frame,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
    leni= len(contour)
    return leni

def display1(img,logo,number,s):
    canny=cv.Canny(img,125,175)
    
    number=int(number)

    #breadth
    x=img.shape[1]
    #height
    y=img.shape[0]
    if(x<y):
      z=x
    else:
      z=y

    if(z<=1500):
        x1=25+z//10
        x1=int(x1)
    else:
        x1=25+z//6.25
        x1=int(x1)

#margin
    y1=2+(z//250)
    min=sys.maxsize
    iter=1
    logo=cv.resize(logo,(int(x1),int(x1)),interpolation=cv.INTER_LINEAR)
    if(number==-1):
      final=canny[y1:int(x1)+y1,y1:int(x1)+y1]
      leni=image(final)
      if(leni<min):
        min=leni
        iter=1

      final=canny[y1:int(x1)+y1,int(x//2)-int(x1//2):int(x//2)+x1-int(x1//2)]
      leni=image(final)
      if(leni<min):
        min=leni
        iter=7
    
      final=canny[y1:int(x1)+y1,-int(x1)-y1:-y1]
      leni=image(final)
      if(leni<min):
        min=leni
        iter=2

      final=canny[-int(x1)-y1:-y1,y1:int(x1)+y1]
      leni=image(final)
      if(leni<min):
        min=leni
        iter=3

      final=canny[-int(x1)-y1:-y1,-int(x1)-y1:-y1]
      leni=image(final)
      if(leni<min):
        min=leni
        iter=4

      final=canny[int(y//2)-int(x1//2):int(y//2)+int(x1//2),y1:int(x1)+y1]
      leni=image(final)
      if(leni<min):
        min=leni
        iter=5

      final=canny[int(y//2)-int(x1//2):int(y//2)+int(x1//2),-int(x1)-y1:-y1]
      leni=image(final)
      if(leni<min):
        min=leni
        iter=6

      final=canny[-int(x1)-y1:-y1,int(x//2)-int(x1//2):int(x//2)+int(x1//2)]
      leni=image(final)
      if(leni<min):
        min=leni
        iter=8
    else:
      iter=int(number)

    if(iter==1):
      img[y1:int(x1)+y1,y1:int(x1)+y1]=logo
    elif(iter==2):
      img[y1:int(x1)+y1,-int(x1)-y1:-y1]=logo
    elif(iter==3):
      img[-int(x1)-y1:-y1,y1:int(x1)+y1]=logo
    elif(iter==4):
      img[-int(x1)-y1:-y1,-int(x1)-y1:-y1]=logo
    elif(iter==5):
      img[int(y/2)-round(x1/2):int(y/2)+x1-round(x1/2),y1:int(x1)+y1]=logo
    elif(iter==6):
      img[int(y/2)-round(x1/2):int(y/2)+x1-round(x1/2),-int(x1)-y1:-y1]=logo
    elif(iter==7):
      img[y1:int(x1)+y1,int(x/2)-round(x1/2):int(x/2)+x1-round(x1/2)]=logo
    elif(iter==8):
      img[-int(x1)-y1:-y1,int(x/2)-round(x1/2):int(x/2)+x1-round(x1/2)]=logo

    return img



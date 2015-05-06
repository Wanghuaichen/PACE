#!C:\Python27\python -u
import numpy as np
import cv2
import cv2.cv as cv

class Blob(object):
    """Find blobs of a particular color (Blue=0,Green=1,Red=2) (openCV => BGR)
       returns list of bounding rectangles which should be the lagoons"""
 
    def __init__(self, color, minsize=24, maxsize=160):
	self.color = color
	self.minDim = minsize
	self.maxDim = maxsize
	self.theta = 1
	self.phi = 1
	self.maxIntensity = 255.0

    def erodeDilate(self,img,iter=1) :
        """Erode(N) --> Dilate(N+1) }"""
        ker = np.ones((5,5),np.uint8)
        return cv2.dilate(
                 cv2.erode(img,ker,iterations=iter),
                    ker,iterations=iter+1)

    def singleErodeDilate(self,img,iter=1) :
        """Erode(N) --> Dilate(N+1) }"""
        ker = np.ones((5,5),np.uint8)
        return cv2.dilate(
                 cv2.erode(img,ker,iterations=iter),
                    ker,iterations=iter)

    def set_minsize(minsize) :
	self.minDim = minsize

    def set_maxsize(maxsize) :
	self.maxDim = maxsize

    def blobs(self, img, pause=1000) :
        """Best so far is 2 rounds of erode->dilate->dilate
           with a a monochrome image of  2*green-(red+blue)/2"""
# IP cameras seem to do best with 2X(Erode->Dilate->Dilate)
#	gray = self.erodeDilate(
#               self.erodeDilate(
#                    cv2.subtract(2*img[:,:,self.color],
#                            cv2.add(
#                                img[:,:,(self.color+1)%3]/2,
#                                img[:,:,(self.color+2)%3]/2))))
# USB camera likes single erode->dilate cycle
	gray = self.singleErodeDilate(
                    cv2.subtract(2*img[:,:,self.color],
                            cv2.add(
                                img[:,:,(self.color+1)%3]/2,
                                img[:,:,(self.color+2)%3]/2)))
# here are some things used in the past for different light conditions
#       cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#	gray = (maxIntensity/phi)*(gray/(maxIntensity/theta))**0.5
#	gray = cv2.blur(gray, (16,16))
	gray2 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        cv2.imshow("camera", gray2)
        if cv.WaitKey(pause) == 27:
                exit()
	contours, _ = cv2.findContours(gray2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	print str(len(contours)) + " contours ( ",
	toosmall = 0
	toolarge = 0
	bbs = []
	for c in contours:
		rect = cv2.boundingRect(c)
		if rect[2] < self.minDim or rect[3] < self.minDim:
			toosmall += 1
#			contours.remove(c)
			continue
		elif rect[2] > self.maxDim or rect[3] > self.maxDim or rect[2] < self.minDim or rect[3] < self.minDim:
			toolarge += 1
#			contours.remove(c)
			continue
		else :
			bbs.append(cv2.boundingRect(c))

	print ") " + str(toosmall) +  " too small " + str(toolarge) + " too large"
# Show the selected bounding boxes in white
#	pen = (255,255,255) # White
#	for r in bbs:
#		cv2.rectangle(img,(r[0],r[1]),(r[0]+r[2],r[1]+r[3]),pen,2)
	return bbs



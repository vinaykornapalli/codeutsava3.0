#---- IMAGE PREPROCESSING ----#
import cv2 as cv
from PIL import Image 
import numpy as np
from matplotlib import pyplot as plt


class PreProcess():

    def __init__(self,source,fade,image,debug): 
        self.debug = debug
        self.image = image
        if fade :
            self.fadedProcess()
        else :
            self.normalProcess()
     
    #increasing resolution
    def resolutionBoost(self) :
        Image.open(self.image).save(self.image,dpi = (600,600))
        img = cv.imread(self.image)
        if self.debug:
            print('IMAGE AFTER INCREASING RESOLUTION')
            plt.imshow(img,'gray')
            plt.show()
    
    #gamma correction
    def gammaCorrection(self) : 
        img= Image.open(self.image)
        a = np.double(img)
        b = a + 1500
        img = np.uint8(b)
        if self.debug:
            print('IMAGE AFTER GAMMA CORRECTION ')
            plt.imshow(img,'gray')
            plt.show()
        
        Image.fromarray(img).save(self.image)
        
    #background text color inversion
    def colorInversion(self) : 
        Image.open(self.image)
        img = cv.imread(self.image)
        cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        gray= cv.bitwise_not(img)
        if self.debug : 
            print('IMAGE AFTER BACKGROUND INVERSION')
            plt.imshow(gray,'gray')
            plt.show()
        Image.fromarray(gray).save(self.image)
        
    #binarization
    def binarization(self) :
        img = cv.imread(self.image,0)
        thresh = cv.threshold(img, 0, 255,
        	cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
        if self.debug : 
            print('IMAGE AFTER BINARIZATION')
            plt.imshow(thresh,'gray')
            plt.show()
        return thresh
    
    #angle correction
    def deskew(self,thresh):
        #angle determination
        img = cv.imread(self.image,0)
        thresh = cv.imread(self.image,0)
        coords = np.column_stack(np.where(thresh >0))
        angle = cv.minAreaRect(coords)[-1]
         
        if angle < -45:
        	angle = -(90 + angle)
        else:
        	angle = -angle
     
        #deskewing
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv.warpAffine(img, M, (w, h),
        	flags=cv.INTER_CUBIC, borderMode=cv.BORDER_REPLICATE)
        if self.debug :
            print('IMAGE AFTER DESKWING')
            plt.imshow(rotated,'gray') 
            plt.show()
        Image.fromarray(rotated).save(self.image)
        
        
    def fadedProcess(self):
        self.resolutionBoost()
        self.gammaCorrection()
        self.colorInversion()
        thresh = self.binarization()
        self.deskew(thresh)

    def normalProcess(self):
        self.resolutionBoost()
        self.colorInversion()
        thresh = self.binarization()
        self.deskew(thresh)

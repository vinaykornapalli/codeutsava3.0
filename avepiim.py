from PIL import Image
import cv2 as cv
import matplotlib.pyplot as plt
import PIL.ImageOps  

class MarkPII():
    def __init__(self,image,info,word_boxes,debug):
        self.debug = debug
        self.info = info
        self.image = image
        self.word_boxes = word_boxes
        self.blockInfo()
        self.invert()
        
        #determining coordinates
    def blockInfo(self):
        Image.open(self.image)
        rotated = cv.imread(self.image)
        coordinates = []
        for word in self.info :
            for box in self.word_boxes :
                if box.content == word :
                    coordinates.append(box.position)
        #blocking words             
        for c in coordinates:
            
            rotated = cv.rectangle(rotated,
                                   (int(c[0][0]),int(c[0][1])),
                                   (int(c[1][0]),int(c[1][1])),
                                   (0,0,0), -1)
        
        if self.debug:
            print('IMAGE AFTER DE-INTIFYING PII')
            plt.imshow(rotated,'gray')
            plt.show()
        Image.fromarray(rotated).save(self.image)
        
    def invert(self):
        #inverting 
        inverted_image = PIL.ImageOps.invert(Image.open(self.image))
        if self.debug:
            print('--- FINAL IMAGE ---')
            plt.imshow(inverted_image,'gray')
            plt.show()
        inverted_image.save(self.image)
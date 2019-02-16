#module importing
import os
from PIL import Image
import datetime
from aveimagepre import PreProcess
from avetextd import  DetectText
from avepiid import DetectPII
from avepiim import MarkPII
import os
path = os.path.dirname(__file__)
uploads = path + 'uploads/'
modified = path + 'modified/'

class IdentifyPI():
    
    def __init__(self,source,debug=False):
        self.debug = debug
        self.path =  os.path.dirname(os.path.realpath('__file__'))
        self.modified = self.path + '/modified/'
        self.source_name = os.path.basename(source)
        self.name, self.extension = self.source_name.split('.')
        self.im_name = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")   
        Image.open(source).save(self.modified + self.im_name + '.'+self.extension)
        self.image = self.modified+self.im_name+'.'+ self.extension
        
        PreProcess(source,False,self.image,self.debug)
        det = DetectText(self.image,self.debug)
        self.text = det.retText()
        self.word_boxes = det.retBox()
        inf = DetectPII(self.text,self.debug)
        self.info = inf.retInfo()
        MarkPII(self.image,self.info,self.word_boxes,self.debug)
        self.retPath()
        
  
    def retText(self):
        return self.text
    def retInfo(self):
        return self.info
    def retPath(self):
        return self.image

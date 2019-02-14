#module importing
from PIL import Image
from aveimagepre import PreProcess
from avetextd import  DetectText
from avepiid import DetectPII
from avepiim import MarkPII



class IdentifyPI():
    
    def __init__(self,source):
        self.name, self.extension = source.split('.')
        Image.open(source).save('temp1.'+ self.extension)
        self.image = 'temp1.'+ self.extension
        
        PreProcess(source,False,self.image)
        det = DetectText(self.image)
        self.text = det.retText()
        self.word_boxes = det.retBox()
        inf = DetectPII(self.text)
        self.info = inf.retInfo()
        MarkPII(self.image,self.info,self.word_boxes)
        
        Image.open(source).save('temp2.'+ self.extension)
        self.image = 'temp2.'+ self.extension
  
    def retText(self):
        return self.text
    def retInfo(self):
        return self.info



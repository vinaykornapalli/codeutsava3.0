#---- TEXT RECOGNITION ----#
import pyocr
import numpy as np
import pyocr.builders
from PIL import Image 


class DetectText():
    def __init__(self,image):
        
        self.image = image
        self.text = []
        self.word_boxes = []
        #checking available tools 
        self.tools = pyocr.get_available_tools()
        if len(self.tools) == 0:
            print("No OCR tool found")
        self.tool = self.tools[0]
        print("Will use tool '%s'" % (self.tool.get_name()))
        
        #checking available languages
        self.langs = self.tool.get_available_languages()
        print("Available languages: %s" % ", ".join(self.langs))
        self.lang = self.langs[0]
        print("Will use lang '%s'" % (self.lang))
        
        #word boxes detection
        self.word_boxes = self.tool.image_to_string(
        Image.open(self.image),
        lang="eng",
        builder=pyocr.builders.WordBoxBuilder())
        
        #text recognition
        for word in self.word_boxes : 
            self.text = np.append(self.text,word.content)
            

    def retText(self):
        return self.text
    def retBox(self):
        return self.word_boxes
        

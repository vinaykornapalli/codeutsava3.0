#---- PERSONALLY IDENTIFIABLE INFORMATION DETECTION ----#
import re
import numpy as np
import en_core_web_sm
from nltk.corpus import stopwords
from nltk.tag.stanford import StanfordNERTagger

class DetectPII():
    
    def __init__(self,text,debug):
        
        self.debug = debug
        self.text = text
        self.preProcess()
        self.spacy_pi = self.spacyDetection()
        self.al_pi = self.alphanumDetection()
        self.stan_pi = self.stanfordDetection()
        self.em_pi = self.emailDetection()
        self.info = np.array([self.spacy_pi,self.al_pi,self.stan_pi,self.em_pi])
        self.info = np.hstack(self.info)
        self.info = [re.sub('[\']', '', inf) for inf in self.info]
        
    #stopword removal
    def preProcess(self):
        self.text = [word for word in self.text if not 
                word in set(stopwords.words('english'))]
        
    #spacy detection
    def spacyDetection(self):
        nlp = en_core_web_sm.load()
        doc = nlp(str(self.text))
        ents = [(e.text, e.label_) for e in doc.ents]
        spacy_pi = [ent[0] for ent in ents ]
        return spacy_pi
    
    #alphanumeric detection
    def alphanumDetection(self):
        al_pi = [con for con in self.text if con.isalnum() and con.isalpha()==False]
        return al_pi
    
    #stanford detection
    def stanfordDetection(self):
        #tagging
        path = '/home/nikhila/Desktop/avepii/stanford-ner'
        jar = path + '/stanford-ner.jar'
        model = path + '/classifiers/english.muc.7class.distsim.crf.ser.gz'
        st = StanfordNERTagger(model,jar)
        classified_text = st.tag(self.text)
        
        #grouping personal information
        if self.debug : 
            print('\n--- PII DETECTION ---\n')
            
        stan_pi = [tags[0] for tags in classified_text if tags[1] == 'PERSON' 
                or tags[1] == 'DATE' or tags[1] == 'ORGANIZATION' 
                or tags[1] == 'LOCATION' or tags[1] == 'PERCENT'
                or tags[1] == 'MONEY' or tags[1] == 'TIME']
        return stan_pi
    
    #email detection
    def emailDetection(self):
        em_pi = [mail for mail in self.text if '@' in mail]
        return em_pi
    
    def retInfo(self):
        return self.info



#-------------------------------------#       


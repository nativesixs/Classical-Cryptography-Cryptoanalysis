from PyQt5 import uic
from PyQt5.QtWidgets import QWidget,QMessageBox
import unicodedata
from utils import Validate
from utils import Files
import numpy as np
from string import ascii_uppercase
import matplotlib.pyplot as plt
from collections import Counter
import sys
sys.path.append("..")
my='gui/analysisgui.ui'

class Analysis(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(my,self)
        self.analyzeBtn.clicked.connect(self.analyze)
        self.evaluateBtn.clicked.connect(self.conclusion)
        self.importDeBtn.clicked.connect(self.importDe)
        self.validate = Validate() 
    
    def importDe(self):
        content=Files().decryptImport()
        self.cipherText.setText(content)

    def analyze(self):
        IOCvalue=self.IOC()
        self.IOClabel.setText(str(IOCvalue))

        '''
        KASISKI
        '''
        ciph=self.cipherText.text()
        ciph=''.join([*filter(str.isalpha, ciph)]).upper()
        #IC key length
        self.mainIC()
        self.accuracyBox.valueChanged.connect(self.mainIC)
        '''
        source:http://www.robindavid.fr/blog/2012/06/15/kasiski-babbage-cryptanalysis-in-python/
        '''
        l=ciph
        res = {}
        freq =[]
        count = 0
        i = 0
        ngramInput=[]
        lst=[]
        while i < len(l): # Loop through all the list
            elt= l[i:i+3] # Take at least 3-character length for tuples
            long = len(elt)
            if long == 3: #should be 3 if not means we are at the end of the list
                for j in range(i+1,len(l)): #Find further in the list for the same pattern
                    if l[i:i+long] == l[j:j+long]: #If match the 3-char check for more
                        while l[i:i+long] == l[j:j+long]:
                            long = long + 1
                        long = long -1
                        elt = l[i:i+long] # Now we have a tuple 
                        diff = j - i # Compute the distance
                        freq.extend(Validate.getDivisors(diff)) #Add the divisors to the list
                        divisors=Validate.getDivisors(diff)
                        #print ("%s\ti:%s\tj:%s\tdiff:%s\t\tDivisors:%s" % 
                        a=[elt,i,j, diff,divisors] #Print information about the tuple (can be deleted)
                        ngramInput.append(("Ngram: "+elt+"\n pos: "+str(i)+",\n next pos: "+str(j)+"\n pos difference: "+str(diff)+"\n divisors:"+str(Validate.getDivisors(diff))+"\n \n"))
                        lst.append(a)
                        count = count +1
                        j = j + long + 1
                i = i + long -3 +1
            else:
                i = i + 1
        self.ngrams.setText(''.join(ngramInput))
        '''
        end of quoted code
        '''
        ngraphs=[]
        for i in range(len(lst)):
            x=[lst[i][0],lst[i][3],lst[i][4]]
            ngraphs.append(x)
        comnum=[]
        for i in range(len(ngraphs)):
            for j in range(len(ngraphs[i][2][:])):
                comnum.append(ngraphs[i][2][j])
        counterlet=Counter(comnum).most_common(20)
        popnums=[]
        for i in range(len(counterlet)):
            if counterlet[i][0] <=25:
                popnums.append(counterlet[i])
        text=[]
        for i in range(len(popnums)):
            text.append("Possible key length: "+str(popnums[i][0])+"\n")
            text.append("Number of occurrences: "+str(popnums[i][1])+"\n \n")
        self.kasiski.setText(''.join(text))
        
        '''
        FREQ AN
        '''
        def freqAn(self):
            alphabet=ascii_uppercase
            cipherCounter=Counter(ciph).most_common()
            alphabetCounter=Counter(alphabet).most_common()
            frequencyAlphabet=[]
            for i in range(26):
                frequencyAlphabet.append(0)
            for i in range(26):
                for j in range(len(cipherCounter)):     
                    if cipherCounter[j][0] in alphabetCounter[i][0]:
                        frequencyAlphabet[i]=cipherCounter[j][1]

            defaultAlphabet=[8.12,1.49,2.71,4.32,12.02,2.30,2.03,5.92,7.31,0.10,0.69,3.98,2.61,6.95,7.68,1.82,0.11,6.02,6.28,9.10,2.88,1.11,2.09,0.17,2.11,0.07]
            alphabet=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
            
            x=alphabet
            y=frequencyAlphabet
            z=defaultAlphabet
            
            z=[8.12,1.49,2.71,4.32,12.02,2.30,2.03,5.92,7.31,0.10,0.69,3.98,2.61,6.95,7.68,1.82,0.11,6.02,6.28,9.10,2.88,1.11,2.09,0.17,2.11,0.07]

            czechfrequency=[6.21,1.55,1.60,3.60,7.69,0.27,0.27,1.27,4.35,2.11,3.73,3.84,3.22,6.53,8.66,3.41,0.001,3.69,4.51,5.72,3.14,4.66,0.008,0.07,1.90,2.19]
            fig,(ax,defalpha,cze)=plt.subplots(nrows=3,sharey=False,figsize=(8,8))
            plt.subplots_adjust(hspace=0.5)  
            p,=defalpha.plot(alphabet,z,'go--')
            p,=ax.plot(alphabet,frequencyAlphabet,'ro--')
            p,=cze.plot(alphabet,czechfrequency,'bo--')
            defalpha.set(xlabel="Chars",ylabel="Frequency",title="English char frequency")
            ax.set(xlabel="Chars",ylabel="Frequency",title="Ciphertext frequency")
            cze.set(xlabel="Chars",ylabel="Frequency",title="Czech char frequency")
            plt.show()
        self.showFreq.clicked.connect(freqAn)
        
        
        
    def mainIC(self):
        ciph=self.cipherText.text()
        ciph=''.join([*filter(str.isalpha,ciph)]).upper()
        maxKey=self.accuracyBox.value()
        maxIC=[]
        keyList=[]
        for i in range(1,maxKey+1):
            maxIC.append(self.getIC(i,ciph)[0])
            keyList.append(self.getIC(i,ciph)[1])
        zz=sorted(zip(maxIC, keyList), reverse=True)[:]
        text=[]
        for i in range(maxKey):
            text.append("Possible key length: "+str(zz[i][1])+"\n")
            text.append("IC: "+str(zz[i][0])+"\n \n")
        self.IC.setText(''.join(text))
        
    def getIC(self,l,string):
        strings=[]
        average=0
        for k in range(l):
            ciph=(string[k::l])
            alphabet=ascii_uppercase
            cipherCounter=Counter(ciph).most_common()
            alphabetCounter=Counter(alphabet).most_common()
            frequencyAlphabet=[]
            for i in range(26):
                frequencyAlphabet.append(0)
            for i in range(26):
                for j in range(len(cipherCounter)):     
                    if cipherCounter[j][0] in alphabetCounter[i][0]:
                        frequencyAlphabet[i]=cipherCounter[j][1]
            numOfLetters=0
            for i in ciph:
                if(i in alphabet):
                    numOfLetters+=1
            freq=0
            N=numOfLetters
            for i in range(len(frequencyAlphabet)):
                freq+=(frequencyAlphabet[i]*(frequencyAlphabet[i]-1))
            IC=(freq/((N*((N-1)))))
            average=average+IC
        averageIC=average/l
        return (averageIC,l)
    
    def IOC(self):
        ciph=self.cipherText.text()
        ciph=''.join([*filter(str.isalpha, ciph)]).upper()
        #IC
        alphabet=ascii_uppercase
        c = Counter(ciph)
        cipherCounter=c.most_common()
        alphabetCounter=Counter(alphabet).most_common()
        frequencyAlphabet=[]
        for i in range(26):
            frequencyAlphabet.append(0)

        for i in range(26):
            for j in range(len(cipherCounter)):     
                if cipherCounter[j][0] in alphabetCounter[i][0]:
                    frequencyAlphabet[i]=cipherCounter[j][1]
        numOfLetters=0
        for i in ciph:
            if(i in alphabet):
                numOfLetters+=1
        freq=0
        N=numOfLetters
        for i in range(len(frequencyAlphabet)):
            freq+=(frequencyAlphabet[i]*(frequencyAlphabet[i]-1))
        IC=(freq/((N*((N-1)))))
        
        return IC
    
    
    
    def conclusion(self):
        ciph=self.cipherText.text()
        ciph=''.join([*filter(str.isalpha, ciph)]).upper()
        conText=[]
        conText.append("IC evaluation:\n")
        
        IC=self.IOC()
        if IC<0.05:
            conText.append("Possible cipher type: Polyalphabetic \n")
            conText.append("Probability: High \n")
        elif IC<0.0385:
            conText.append("Possible cipher type: Polyalphabetic \n")
            conText.append("Probability: Very high \n")
        elif IC>= 0.06 and self.languagePick.currentText()=='Look for Czech words':
            conText.append("Possible cipher type: Monoalphabetic/Transposition \n")
            conText.append("Probability: High \n")
        elif IC>=0.065:
            conText.append("Possible cipher type: Monoalphabetic/Transposition \n")
            conText.append("Probability: High \n")
        elif IC>=0.075:
            conText.append("Possible cipher type: Monoalphabetic/Transposition \n")
            conText.append("Probability: Very high \n")
        else:
            conText.append("Could not evaluate \n")
        # test transposition
        if len(ciph)>=250:
            alphabet=ascii_uppercase
            cipherCounter=Counter(ciph).most_common()
            alphabetCounter=Counter(alphabet).most_common()
            frequencyAlphabet=[]
            for i in range(26):
                frequencyAlphabet.append(0)
            for i in range(26):
                for j in range(len(cipherCounter)):     
                    if cipherCounter[j][0] in alphabetCounter[i][0]:
                        frequencyAlphabet[i]=cipherCounter[j][1]
            freqalphabetletters=[]
            for i in range(13):
                freqalphabetletters.append(cipherCounter[i][0])
            if self.languagePick.currentText()=='Look for English words':
                default=["E","T","A","O","I","N","S","H","R","D","L","C","U"]
            if self.languagePick.currentText()=='Look for Czech words':
                default=["O","E","N","A","T","V","S","I","L","K","R","P","M"]
            points=0
            conText.append("\nFrequency evaluation:\n")
            
            for i in range(len(default)):
                if freqalphabetletters[i] in default:
                    points+=1
            if points>=10:
                conText.append("Possible cipher type: Transposition \n")
                conText.append("Probability: Very high \n")
            if points>=7:
                conText.append("Possible cipher type: Transposition \n")
                conText.append("Probability: High \n")
            if points<=6:
                conText.append("Possible cipher type: Not Transposition \n")
                conText.append("Probability: Medium \n")
            if points<=3:
                conText.append("Possible cipher type: Not Transposition \n")
                conText.append("Probability: Very high \n")
        else:
            conText.append("Ciphertext not long enough \n")
        
        
        # ADFGVX, PLAYFAIR, HILL
        conText.append("\nOther possible ciphers:\n")
        if(len(ciph)%2)==0:
            conText.append("Possible cipher: Playfair \n")
        if(len(ciph)%3)==0:
            conText.append("Possible cipher: Hill \n")
            
        ADFGVX=["B","C","E","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","W","Y","Z"]
        ADFGX=["B","C","E","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","Y","Z"]
        text=ciph
        text=text.replace("A","")
        text=text.replace("D","")
        text=text.replace("F","")
        text=text.replace("G","")
        text=text.replace("V","")
        text=text.replace("X","")
        if len(text)==0:
            conText.append("Possible cipher: ADFGVX \n")

        text=ciph
        text=text.replace("A","")
        text=text.replace("D","")
        text=text.replace("F","")
        text=text.replace("G","")
        text=text.replace("X","")
        if len(text)==0:
            conText.append("Possible cipher: ADFGX \n")
        ###################################
        if self.exportToFile.isChecked():
            self.export(''.join(conText))
        self.conclusionText.setText(''.join(conText))
        
    def export(self,content):
        file = open('analyzedCipher.txt','w')
        file.write(str(content))
        file.close()
        
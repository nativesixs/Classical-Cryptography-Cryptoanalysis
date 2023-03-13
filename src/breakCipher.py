from PyQt5 import uic
from PyQt5.QtWidgets import QWidget,QMessageBox, QVBoxLayout, QPushButton
import unicodedata
from usefull_functions import Validate
from usefull_functions import Files
import numpy as np
import math
import pylab
from pylab import *
from datetime import datetime
from string import ascii_uppercase
import matplotlib.pyplot as plt
from pycipher import Playfair
import random
import re

from collections import Counter

import sys
sys.path.append("..")
my='gui/breakCipherGUI.ui'
import matplotlib
matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib import pyplot
from matplotlib.widgets import Button



class Breaker(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(my, self)
        self.reset()   
  
    def reset(self):
        self.chooseBtn.clicked.connect(self.cipherChoice)
        self.importDeBtn.clicked.connect(self.importDe)
        self.choiceFrame.show()
        self.languagePick.show()
        #Hide all other frames
        self.cipherText.clear()
        self.plainTextLikely.clear()
        self.plainTextLine.clear()
        self.status.setText("Ready")
        self.timer.clear()
        self.basicFrame.hide()
        self.affineFrame.hide()
        self.vigFirstFrame.hide()
        self.plotControlFrame.hide()
        self.radioBrute.hide()
        self.radioFrq.hide()
        self.radioDict.hide()
        self.radioHill.hide()

        
    def importDe(self):
        content=Files().decryptImport()
        self.cipherText.setText(content)
        
    def export(self,content):
        file = open('brokenCipher.txt','w')
        file.write(str(content))
        file.close()
        
    def strip_accents(self,text):
        try:
            text = unicode(text, 'utf-8')
        except NameError: 
                pass
        text = unicodedata.normalize('NFD', text)\
                .encode('ascii', 'ignore')\
                .decode("utf-8")
        return str(text)
    
    def makec(self):
        char = self.cipherText.text()
        char=char.upper()
        char=self.strip_accents(char)
        char = char.replace(" ", "XMEZERAX")
        char=''.join([*filter(str.isalnum, char)])
        char = char.replace("XMEZERAX", " ")
        return char

    def findLikely(self,text):
        self.accuracyBox.show()
        self.ngramsLabel.show()
        possible=[]
        if self.languagePick.currentText()=='Look for English words':
            lines=open("src/eng1000words.txt","r").read().splitlines()
        if self.languagePick.currentText()=='Look for Czech words':
            lines=open("src/czech1000words.txt","r").read().splitlines()
        for j in range(len(text)):
            for i in range(len(lines)):
                if lines[i].upper() in text[j] and len(lines[i])>=self.accuracyBox.value():
                    possible.append(text[j])
                    if self.affineradio.isChecked() or self.routeradio.isChecked() or self.railfenceradio.isChecked():
                        possible.append(str(text[j+1]))
                    elif self.playfairradio.isChecked():
                        possible.append(str(text[1::2]))
                    else:
                        possible.append("Key: "+str(j))
                    break
        self.plainTextLikely.setText('\n'.join(possible))
        if self.exportToFile.isChecked():
            self.export('\n'.join(possible))


    def cipherChoice(self):
        if self.affineradio.isChecked():
            self.mainAffine()
        elif self.adfgvxradio.isChecked():
            pass
        elif self.playfairradio.isChecked():
            self.mainPlayfair()
        elif self.rotradio.isChecked():
            self.mainRot()
        elif self.railfenceradio.isChecked():
            self.mainRailfence()
        elif self.routeradio.isChecked():
            self.mainRoute()
        elif self.vigenereradio.isChecked():
            self.mainVigenere()
        elif self.scytaleradio.isChecked():
            self.mainScytale()
        self.choiceFrame.hide()
 
    '''
    AFFINE
    '''
    def affineFreq(self,ciph):
        lst=[]
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
        lst.append(frequencyAlphabet)
        frequencyAlphabet=lst
        return frequencyAlphabet
    
    
    def mainAffine(self):
        self.basicFrame.show()
        self.affineFrame.show()
        self.radioBrute.show()
        self.radioFrq.show()
        self.radioBrute.setChecked(True)
        
        def breaking():
            if self.radioBrute.isChecked():
                start_time = datetime.now()
                self.status.setText("Ready")
                encrypted=self.makec()
                global previous
                previous=[]
                coprimes=[1,3,5,7,9,11,15,17,19,21,23,25]
                for i in range(len(coprimes)):
                    for j in range(1,26):
                        self.status.setText("Working..")
                        previous.append(self.decryptAffine(encrypted,coprimes[i],j))
                        previous.append("Key a: "+str(coprimes[i])+", Key b: "+str(j))
                        self.plainTextLine.setText('\n'.join(previous))
                self.status.setText("Done")
                self.timer.setText('{}'.format(datetime.now()-start_time))
                self.findLikely(previous)
            if self.radioFrq.isChecked():
                self.vigFirstFrame.show()
                self.guessedKey.hide()
                self.labelHodnotaB_12.hide()
                self.ngramsLabel.hide()
                self.accuracyBox.hide()
                
                def plotting():
                    ciph=Validate().analysisCleantext(self.cipherText.text())
                    self.plotControlFrame.show()
                    self.labelHodnotaB_10.hide()
                    self.shiftletter.hide()
                    self.labelHodnotaB_8.setText("Key A:")
                    self.labelHodnotaB_9.setText("Key B:")
                    self.okBtn.hide()
                    self.labelHodnotaB_11.hide()
                    self.keyLetters.hide()
                    self.plotBox.setRange(1,25)
                    frequencies=self.affineFreq(ciph)
                    key=1
                    self.plots(key,frequencies,ciph)
                self.continueBtn.clicked.connect(plotting) 
        
        def findagain():
            global previous
            self.findLikely(previous)
            
        self.accuracyBox.valueChanged.connect(findagain)
        self.decryptBtn.clicked.connect(breaking)
    
    def decryptAffine(self,text,key,b):
        
        def modInverse(a,m) :
            a=a%m
            for x in range(1,m) :
                if((a*x)%m==1):
                    return x
            return 1
        a=key
        m=26
        chars= ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        dectext=""
        decres=[]
        modin = modInverse(a,m)
        char=text
        for i in range(len(char)):
            if char[i]==" " or char[i].isnumeric():
                decres.append(char[i])
            else:
                dechar=chars.index(char[i])
                vz=(modin*(dechar-b)%m)
                decres.append(chars[vz])
            dectext=''.join(decres)
        if self.radioBrute.isChecked():
            return dectext
        else:
            self.plainTextLine.setText(dectext)
    
    '''
    ADFGVX
    '''

    
    '''
    ROT13
    '''
    def mainRot(self):
        self.basicFrame.show()
        self.affineFrame.show()
        self.ngramsLabel.hide()
        self.accuracyBox.hide()
        self.status.setText("Ready")
        def breaking():
            start_time = datetime.now()
            self.status.setText("Working..")
            ciph=Validate().analysisCleantext(self.cipherText.text())
            decrypted=[]
            result=[]
            for j in range(26):
                chars= ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
                rotval=j
                newalpha=np.roll(chars,rotval)
                index=[]
                for i in range(len(ciph)):
                    index.append(chars.index(ciph[i]))
                decrypted=[]
                for i in range(len(ciph)):
                    decrypted.append(newalpha[index[i]])
                x=''.join(decrypted)
                result.append(x)
                result.append("Key: "+str(j))
            self.status.setText("Done")
            self.timer.setText('{}'.format(datetime.now()-start_time))
            self.plainTextLine.setText('\n'.join(result))
        self.decryptBtn.clicked.connect(breaking)

    
    '''
    RAILFENCE
    '''
    def mainRailfence(self):
        self.status.setText("Ready")
        self.basicFrame.show()
        self.affineFrame.show()
        
        def breaking():
            start_time = datetime.now()
            encrypted=self.makec()
            global previous
            previous=[]
            for i in range(2,len(encrypted)):
                self.status.setText("Working..")
                previous.append(self.decryptRailfence(encrypted,i))
                previous.append("Key: "+str(i))
            self.plainTextLine.setText('\n'.join(previous))
            self.findLikely(previous)
            self.status.setText("Done")
            self.timer.setText('{}'.format(datetime.now()-start_time))

        def findagain():
            global previous
            self.findLikely(previous)
            
        self.accuracyBox.valueChanged.connect(findagain)
        self.decryptBtn.clicked.connect(breaking)
    
    def decryptRailfence(self,text,key):
        parsedText=[char for char in text]
        matrix=np.empty((key,len(text)),dtype="U")
        result=[] 
        for i in range(key):
            column=0
            down=True
            for row in range(len(text)):
                if down==False:
                    if column-1>=0:
                        if column==i:
                            matrix[column][row]=parsedText[0]
                            parsedText.pop(0)
                        elif not [*filter(str.isalnum, matrix[column][row])]:
                            matrix[column][row]="*"
                        column=column-1
                    else:
                        down=True 
                if down==True:   
                    if column<=key-1:
                        if column==i:
                            matrix[column][row]=parsedText[0]
                            parsedText.pop(0)
                        elif not [*filter(str.isalnum, matrix[column][row])]:
                            matrix[column][row]="*"
                        column=column+1
                if column==key:
                    column=column-2
                    down=False
        for row in range(len(text)):
            for column in range(key):
                if [*filter(str.isalnum, matrix[column][row])]:
                    result.append(matrix[column][row])
        decrypted="".join(result)
        return decrypted
    
    '''
    ROUTE
    '''
    def factors(self,lenCiph):
        factors=[]
        for i in range(1, lenCiph + 1):
           if lenCiph % i == 0:
               factors.append(i)
        return factors
    
    def decryptRoute(self):
        start_time=datetime.now()
        self.status.setText("Working..")
        ciph=self.makec()
        factor=self.factors(len(ciph))
        posrow=[]
        poscol=[]
        for i in range(int(len(factor)/2)):
            posrow.append(factor[i])
            
        for i in range(int(len(factor)/2)):
             factor.sort(reverse=True)
             poscol.append(factor[i])
         
        for i in range(int(len(factor)/2)):
            factor.sort(reverse=False)
            poscol.append(factor[i])

        for i in range(int(len(factor)/2)):
             factor.sort(reverse=True)
             posrow.append(factor[i])
           
        posResult=[]
        posKey=[]
        posMethod=[]
        output=[]
        
        for i in range(len(posrow)):
            matrix=np.empty((posrow[i],poscol[i]),dtype="U")
            rows=int(math.ceil(len(ciph)/posrow[i]))  
            columns=int(len(ciph)/posrow[i])
            matrixSize=posrow[i]*rows
            matrix.reshape(-1)[:len(ciph)] = list(ciph)
            
            result=[]
            for j in range(columns):
                result.append(ciph[j::columns])
            decryptedText=''.join(result)
            output.append(decryptedText)
            output.append("Key: "+str(posrow[i]))
            output.append("Route: Column \n")
            
            top=left=0
            bottom=posrow[i]-1
            right=rows-1
            parsedText=[char for char in ciph]
            
            '''
            source: https://www.techiedelight.com/print-matrix-spiral-order/
            '''
            while True:
                if left>right:
                    break
                #top
                for l in range(left,right+1):
                    matrix[top][l]=parsedText[0]
                    parsedText.pop(0)
                top+=1
                if top > bottom:
                    break     
                #right
                for l in range(top,bottom+1):
                    matrix[l][right]=parsedText[0]
                    parsedText.pop(0)
                right-=1     
                if left > right:
                    break  
                #bottom
                for l in range(right,left-1,-1):
                    matrix[bottom][l]=parsedText[0]
                    parsedText.pop(0)
                bottom-=1   
                if top > bottom:
                    break
                #left
                for l in range(bottom,top-1,-1):
                    matrix[l][left]=parsedText[0]
                    parsedText.pop(0)
                left+=1       
            '''
            end quoted code
            '''
            matrix=np.flip(matrix)
            matrix=matrix.transpose() 
            decryptedText=""
            for k in range(rows):
                line="".join(string for string in matrix[k] if len(string) > 0)
                decryptedText=decryptedText+line
            output.append(decryptedText)
            output.append("Key: "+str(posrow[i]))
            output.append("Route: Spiral \n")   
            self.plainTextLine.setText('\n'.join(output))
            self.findLikely(output)
            self.timer.setText('{}'.format(datetime.now()-start_time))
            self.status.setText("Done")
        
    def mainRoute(self):
        self.basicFrame.show()
        self.affineFrame.show()
        self.status.setText("Ready")
        self.accuracyBox.valueChanged.connect(self.decryptRoute)
        self.decryptBtn.clicked.connect(self.decryptRoute)
    
    '''
    VIGENERE
    '''
    
    def vigenereFindKey(self,key,text):
        rows=int(math.ceil(len(text)/key))
        matrix=np.empty((rows,key),dtype="U")   
        matrix.reshape(-1)[:len(text)] = list(text)
        lst=[]
        for i in range(key):
            arr=[]
            for j in range(rows):
                arr.append(matrix[j][i])
            ciph=''.join(arr)   
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
            lst.append(frequencyAlphabet)
        frequencyAlphabet=lst
        return frequencyAlphabet
        
    def plots(self,key,frequencyAlphabet,ciph):
        alphabet=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        defaultAlphabet=[8.12,1.49,2.71,4.32,12.02,2.30,2.03,5.92,7.31,0.10,0.69,3.98,2.61,6.95,7.68,1.82,0.11,6.02,6.28,9.10,2.88,1.11,2.09,0.17,2.11,0.07]
        czechfrequency=[6.21,1.55,1.60,3.60,7.69,0.27,0.27,1.27,4.35,2.11,3.73,3.84,3.22,6.53,8.66,3.41,0.001,3.69,4.51,5.72,3.14,4.66,0.008,0.07,1.90,2.19]
        if self.affineradio.isChecked():
            global keyA
            global keyB

        def shiftPlot1(event):
            if self.vigenereradio.isChecked():
                p.set_ydata(frequencyAlphabet[self.plotBox.value()-1])
                self.shiftletter.setText(alphabet[abs(self.shiftBox.value())])
                plt.draw()
                dispIndex=self.plotBox.value()
                self.currentplotnumber.setText(str(dispIndex))
            if self.affineradio.isChecked():
                global keyA
                global keyB
                keyA=self.plotBox.value()
                keyB=self.shiftBox.value()
                self.decryptAffine(ciph,keyA,keyB)           
        self.plotBox.valueChanged.connect(shiftPlot1)
        
        def shiftPlot2(event):
            if self.vigenereradio.isChecked():
                p.set_ydata(frequencyAlphabet[self.plotBox.value()-1])
                self.shiftletter.setText(alphabet[abs(self.shiftBox.value())])
                plt.draw()
                dispIndex=self.plotBox.value()
                self.currentplotnumber.setText(str(dispIndex))
            if self.affineradio.isChecked():
                global keyA
                global keyB
                keyA=self.plotBox.value()
                keyB=self.shiftBox.value()
                self.decryptAffine(ciph,keyA,keyB)
        self.plotBox.valueChanged.connect(shiftPlot2)
        

        x=alphabet
        z=defaultAlphabet
      
        fig,(ax,defalpha,cze)=plt.subplots(nrows=3,sharey=False,figsize=(8,8))
        plt.subplots_adjust(hspace=0.7)  
        p,=defalpha.plot(x,z,'go--')
        p,=cze.plot(alphabet,czechfrequency,'bo--')
        p,=ax.plot(x,frequencyAlphabet[self.plotBox.value()-1],'ro--')
        defalpha.set(xlabel="Chars",ylabel="Frequency",title="English char frequency")
        cze.set(xlabel="Chars",ylabel="Frequency",title="Czech char frequency")
        ax.set(xlabel="Chars",ylabel="Frequency",title="Ciphertext frequency")
            
        def shift1(event):
            y=np.roll(frequencyAlphabet[self.plotBox.value()-1],self.shiftBox.value())
            self.shiftletter.setText(alphabet[abs(self.shiftBox.value())])
            p.set_ydata(y)
            plt.draw()
            if self.affineradio.isChecked():
                global keyA
                global keyB
                keyA=self.plotBox.value()
                keyB=self.shiftBox.value()
                self.decryptAffine(ciph,keyA,keyB)
        self.shiftBox.valueChanged.connect(shift1)
          

        def shift2(event):
            y=np.roll(frequencyAlphabet[self.plotBox.value()-1],-self.shiftBox.value())
            self.shiftletter.setText(alphabet[self.shiftBox.value()])
            p.set_ydata(y)
            plt.draw()
            if self.affineradio.isChecked():
                global keyA
                global keyB
                keyA=self.plotBox.value()
                keyB=self.shiftBox.value()
                self.decryptAffine(ciph,keyA,keyB)
        self.shiftBox.valueChanged.connect(shift2)
        
        def okFce(event):
            if self.vigenereradio.isChecked():
                keyL=self.keyLetters.text()+self.shiftletter.text()
                self.keyLetters.setText(keyL)
                oldval=self.plotBox.value()
                self.plotBox.setValue(oldval+1)
            if self.affineradio.isChecked():
                keyL=self.shiftBox.value()
                self.keyLetters.setText(str(keyL))
        self.okBtn.clicked.connect(okFce)
        
        def callvgn(event):
            if self.vigenereradio.isChecked():
                self.vigenere(ciph)
            if self.affineradio.isChecked():
                if self.plotBox.value()==1:
                    keyA=self.keyLetters.text()
                    keyA=int(keyA)
                if self.plotBox.value()==2:
                    keyB=self.keyLetters.text()
                    keyB=int(keyB)
                if keyA and keyB:
                    self.decryptAffine(ciph,keyA,keyB)
        self.keyLetters.textChanged.connect(callvgn)
        
        def hideC(event):
            plt.close()
            self.plotControlFrame.hide()
            
        self.guessedKey.valueChanged.connect(hideC)
        plt.ion()
        plt.show()
        
        
    def keyLength(self,ciph):
        '''
        source:http://www.robindavid.fr/blog/2012/06/15/kasiski-babbage-cryptanalysis-in-python/
        '''
        l=ciph
        res = {}
        freq =[]
        count = 0
        i = 0


        def getDivisors(n):
            l = []
            for i in range(2,n):
                if n % i == 0:
                    l.append(i)
            return l
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
                        freq.extend(getDivisors(diff)) #Add the divisors to the list
                        divisors=getDivisors(diff)
                        #print ("%s\ti:%s\tj:%s\tdiff:%s\t\tDivisors:%s" % (elt,i,j, diff,getDivisors(diff))) #Print information about the tuple (can be deleted)
                        a=[elt,i,j, diff,divisors] #Print information about the tuple (can be deleted)
                        lst.append(a)
                        count = count +1
                        j = j + long + 1
                i = i + long -3 +1
            else:
                i = i + 1
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
            text.append("Key length: "+str(popnums[i][0])+"\n")
            text.append("rep.index: "+str(popnums[i][1])+"\n \n")
        self.plainTextLikely.setText(''.join(text))
        
    def vigenere(self,ciph):
        text=Validate().analysisCleantext(ciph)
        keylen=int(self.guessedKey.value())
        key=self.keyLetters.text()
        
        if len(key)<keylen:
            while len(key)<keylen:
                key=key+"X"
            
        result=[]
        keyInt=[ord(i) for i in key]
        textInt=[ord(i) for i in text]

        for i in range(len(text)):
            shift=((textInt[i]-keyInt[i%len(key)])%26)
            if text[i].isalpha():
                result.append(chr(shift+65))
            else:
                result.append(text[i])
        decryptedText=''.join(result)
        return self.plainTextLine.setText(decryptedText)


    def mainVigenere(self):
        self.basicFrame.show()

        def breaking():
            ciph=self.cipherText.text()
            ciph=''.join([*filter(str.isalpha, ciph)]).upper()
            self.vigFirstFrame.show()
            self.keyLength(ciph)
        
        def plotting():
            ciph=self.cipherText.text()
            ciph=''.join([*filter(str.isalpha, ciph)]).upper()
            self.plotControlFrame.show()
            key=int(self.guessedKey.value())
            frequencies=self.vigenereFindKey(key,ciph)
            self.plots(key,frequencies,ciph)
            
        self.continueBtn.clicked.connect(plotting) 
        self.decryptBtn.clicked.connect(breaking)
    
    
    '''
    SCYTALE
    '''
    
    def decryptScytale(self,text,key):
        row=int(math.ceil(len(text)/key))
        col=key  
        matrix=np.empty((col,row),dtype="U")
        matrix.reshape(-1)[:len(text)] = list(text)
        result=[]
        for i in range(row):
            for j in range(col):
                result.append(matrix[j][i])
        if len(text)<(col*key):
            for i in range((col*key)-len(text)):
                if result[-1]=="X":
                    result.remove(result[-1])
        decrypted=''.join(result)
        return decrypted
    
    def mainScytale(self):
        self.basicFrame.show()
        self.affineFrame.show()
        self.accuracyBox.setValue(int(3))
        self.ngramsLabel.setText("Amount of tested keys:")
        def breaking():
            encrypted=self.makec()
            previous=[]
            for i in range(1,26):
                start_time = datetime.now()
                self.status.setText("Working..")
                previous.append(self.decryptScytale(encrypted,i))
                previous.append("Key: "+str(i))
                self.plainTextLine.setText('\n'.join(previous))
            self.status.setText("Done")
            self.timer.setText('{}'.format(datetime.now()-start_time))
        self.decryptBtn.clicked.connect(breaking)
        if self.accuracyBox.value() <=2:
            Validate().errmsg("Min. amount of tested keys = 3")
            self.accuracyBox.setValue(int(3))
            self.accuracyBox.valueChanged.connect(self.mainIC)
        else:
            self.accuracyBox.valueChanged.connect(self.mainIC)
    
    '''
    IC
    '''

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

    
    def mainIC(self):
        self.affineFrame.show()
        self.ngramsLabel.setText("Amount of tested keys:")
        ciph=Validate().analysisCleantext(self.cipherText.text())
        maxKey=self.accuracyBox.value()
        maxIC=[]
        keyList=[]
        for i in range(1,maxKey):
            maxIC.append(self.getIC(i,ciph)[0])
            keyList.append(self.getIC(i,ciph)[1])
        zz=sorted(zip(maxIC, keyList), reverse=True)[:3]
        z="Top 3 keys lengths based on IC \n"+"Key length: "+str(zz[0][1])+"\nIC: "+str(zz[0][0])+"\n"+"Key length: "+str(zz[1][1])+"\nIC: "+str(zz[1][0])+"\n"+"Key length: "+str(zz[2][1])+"\nIC: "+str(zz[2][0])+"\n"
        self.plainTextLikely.setText(z)
    
    '''
    PLAYFAIR
    '''
    def mainPlayfair(self):
        self.basicFrame.show()
        self.affineFrame.show()
        self.radioDict.show()
        self.radioHill.hide()
        self.status.setText("Ready")
        self.radioDict.setChecked(True)
        self.decryptBtn.clicked.connect(self.Playfair)
        self.accuracyBox.valueChanged.connect(self.likelyPlayfair)
    def Playfair(self):
        self.status.setText("Working..")
        start_time = datetime.now()
        if self.radioDict.isChecked():
            self.status.setText("Ready")
            ciph=Validate().analysisCleantext(self.cipherText.text())
            if self.languagePick.currentText()=='Look for English words':
                keyword=open("src/eng1000words.txt","r").read().splitlines()
            if self.languagePick.currentText()=='Look for Czech words':
                keyword=open("src/czech1000words.txt","r").read().splitlines()
            alphabet = list('ABCDEFGHIKLMNOPQRSTUVWXYZ')
            global playfairRes
            global playfairKey
            playfairRes=[]
            playfairKey=[]
            res=[]
            for k in range(len(keyword)):
                self.status.setText("Working..")
                keyphrase=[]
                for i in range(len(keyword[k])):
                    if keyword[k][i]=='j' or keyword[k][i]=='J':
                        keyword[k]=keyword[k].replace('j','I')
                    if keyword[k][i].upper() not in keyphrase:
                        keyphrase.append(keyword[k][i].upper())
                for i in range(len(alphabet)):
                    if alphabet[i] not in keyphrase:
                        keyphrase.append(alphabet[i])
                key=''.join(keyphrase)
                dec=Playfair(key=key).decipher(ciph)
                self.status.setText("Done")
                playfairRes.append(dec)
                playfairKey.append('Key: '+key)
                res.append(dec)
                res.append('Key: '+key)
            self.status.setText("Done")
            self.timer.setText('{}'.format(datetime.now()-start_time))
            self.plainTextLine.setText('\n\n'.join(res))

            
    def likelyPlayfair(self):
        global playfairRes
        global playfairKey
        keys=playfairKey
        text=playfairRes
        possible=[]
        if self.languagePick.currentText()=='Look for English words':
            lines=open("src/eng1000words.txt","r").read().splitlines()
        if self.languagePick.currentText()=='Look for Czech words':
            lines=open("src/czech1000words.txt","r").read().splitlines()
        for j in range(len(text)):
            for i in range(len(lines)):
                if lines[i].upper() in text[j] and len(lines[i])>=self.accuracyBox.value():
                    possible.append(text[j])
                    possible.append(keys[j]+'\n')
                    break
        self.plainTextLikely.setText('\n\n'.join(possible))
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
import unicodedata
from utils import Validate
from utils import Files
# import pylab
# from pylab import *
from string import ascii_uppercase

from collections import Counter

import sys
sys.path.append("..")
my='gui/breakCipherGUI.ui'
import matplotlib
matplotlib.use("Qt5Agg")



from .breakers.affine_cipher import AffineCipher
from .breakers.rot_cipher import RotCipher
from .breakers.railfence_cipher import RailfenceCipher
from .breakers.route_cipher import RouteCipher
from .breakers.vigenere_cipher import VigenereCipher
from .breakers.scytale_cipher import ScytaleCipher
from .breakers.playfair_cipher import PlayfairCipher

class Breaker(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(my, self)
        self.reset()
        self.affine_cipher = AffineCipher()
        self.rot_cipher = RotCipher()
        self.railfence_cipher = RailfenceCipher()
        self.route_cipher = RouteCipher()
        self.vigenere_cipher = VigenereCipher()
        self.scytale_cipher = ScytaleCipher()
        self.playfair_cipher = PlayfairCipher()
        self.validate = Validate()
  
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
            self.affine_cipher.mainAffine(self)
        elif self.adfgvxradio.isChecked():
            pass
        elif self.playfairradio.isChecked():
            self.playfair_cipher.mainPlayfair(self)
        elif self.rotradio.isChecked():
            self.rot_cipher.mainRot(self)
        elif self.railfenceradio.isChecked():
            self.railfence_cipher.mainRailfence(self)
        elif self.routeradio.isChecked():
            self.route_cipher.mainRoute(self)
        elif self.vigenereradio.isChecked():
            self.vigenere_cipher.mainVigenere(self)
        elif self.scytaleradio.isChecked():
            self.scytale_cipher.mainScytale(self)
        self.choiceFrame.hide()

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
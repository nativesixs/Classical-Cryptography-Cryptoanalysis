from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from utils import Validate
from utils import Files

from itertools import cycle
import sys
sys.path.append("..")
my='gui/vigeneregui.ui'

class Vigenere(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(my, self)
        
        self.encryptBtn.clicked.connect(self.encrypt)
        self.decryptBtn.clicked.connect(self.decrypt)
        self.plainText.text()
        self.cipherText.text()
        self.keyLine.text()
        self.keepSpaces.setChecked(False)
        self.importEnBtn.clicked.connect(self.importEn)
        self.importDeBtn.clicked.connect(self.importDe)
    
    def importEn(self):
        content=Files().encryptImport()
        self.plainText.setText(content)
        
    def importDe(self):
        content=Files().decryptImport()
        self.cipherText.setText(content)
        
    def keyValidator(self):
        b=str(self.keyLine.text())
        if b.isalpha()==True:
            b=b.upper()
            return b
        else:
            Validate().errmsg('Invalid key, "ABC" as default')
            self.keyLine.clear()
            self.keyLine.setText('ABC')
            b="ABC"
            return b

        
    def generateKey(self,text,key):
        if len(key)>len(text):
            self.errmsg('Key length > text length, input shorter key')
            self.keyLine.clear()
            return
        key=list(key)
        keystream=[]
        if len(text)==len(key): 
          return(key)
        else:
            for item in cycle(key):
                keystream.append(item)
                if len(keystream)==len(text):
                    break
            return keystream
        



    def encrypt(self):
        if self.keepSpaces.isChecked():
            text=Validate().inputVer(self.plainText.text())
        else:
            text=Validate().analysisCleantext(self.plainText.text())
        
        key=self.keyValidator()
        key=''.join([*filter(str.isalpha, key)])
        key=''.join(self.generateKey(text, key))
        
        result=[]
        keyInt=[ord(i) for i in key]
        textInt=[ord(i) for i in text]
        
        for i in range(len(text)):
            shift=((textInt[i]+keyInt[i%len(key)])%26)
            if text[i].isalpha():
                result.append(chr(shift+65))
            else:
                result.append(text[i])
        encryptedText=''.join(result)
        if self.exportToFile.isChecked():
            self.export(encryptedText,1)
        if len(encryptedText)>4:
            fives=' '.join(encryptedText[i:i+5] for i in range(0, len(encryptedText), 5))
            return (self.cipherTextLine.setText(fives),
                    self.cipherText.clear(),
                    self.cipherText.setText(''.join(result)))
        else:
            return (self.cipherTextLine.setText(''.join(result)),
                    self.cipherText.clear(),
                    self.cipherText.setText(''.join(result)))
        
    def decrypt(self):
        if self.keepSpaces.isChecked():
            text=Validate().inputVer(self.cipherText.text())
        else:
            text=Validate().analysisCleantext(self.cipherText.text())
            
        key=self.keyValidator()
        key=''.join([*filter(str.isalpha, key)])
        key=''.join(self.generateKey(text, key))
        
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
        if self.exportToFile.isChecked():
            self.export(decryptedText,2)
        return self.plainTextLine.setText(decryptedText)
    
    def export(self,content,sw):
        if sw==1:
            file = open('encrypted.txt','w')
        if sw==2:
            file = open('decrypted.txt','w')
        file.write(str(content))
        file.close()
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget,QMessageBox
import unicodedata
from usefull_functions import Validate
from usefull_functions import Files
import math
import numpy as np
import sys
sys.path.append("..")
my='gui/scytalegui.ui'

class Scytale(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(my, self)
        
        self.encryptBtn.clicked.connect(self.crypt)
        self.decryptBtn.clicked.connect(self.decryp)
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
        try:
            b=int(self.keyLine.text())
            return b
        except ValueError:
            Validate().errmsg('Invalid key, inserting 3 as default')
            self.keyLine.clear()
            self.keyLine.setText('3')
            b=3
            return b

    def crypt(self):
        #text=Validate().inputVer(self.plainText.text())
        if self.keepSpaces.isChecked():
            text=Validate().inputVer(self.plainText.text())
        else:
            text=Validate().analysisCleantext(self.plainText.text())
        key=self.keyValidator()
        row=int(math.ceil(len(text)/key))
        col=key        

        result=[]
        for i in range(col):
            if len(text[i::col])<row:
                result.append(text[i::col]+"X")
            else:
                result.append(text[i::col])
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
        
    def decryp(self):
        #text=Validate().inputVer(self.cipherText.text())
        if self.keepSpaces.isChecked():
            text=Validate().inputVer(self.cipherText.text())
        else:
            text=Validate().analysisCleantext(self.cipherText.text())
        key=self.keyValidator()
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
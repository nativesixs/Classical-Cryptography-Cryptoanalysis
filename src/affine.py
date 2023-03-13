from PyQt5 import uic
from PyQt5.QtWidgets import QWidget,QMessageBox
import unicodedata

from usefull_functions import Validate
from usefull_functions import Files

import sys
sys.path.append("..")
my='gui/affinegui.ui'
class Affine(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(my, self)      
        self.encryptBtn.clicked.connect(self.encrypt)
        self.decryptBtn.clicked.connect(self.decrypt)
        self.importEnBtn.clicked.connect(self.importEn)
        self.importDeBtn.clicked.connect(self.importDe)
        self.comboBox.currentText()
        self.keyLine.text()
        self.keepSpaces.setChecked(False)

    def keyValidator(self):
        try:
            b=int(self.keyLine.text())
            return b
        except ValueError:
            Validate().errmsg('Invalid B key, inserting 5 as default')
            self.keyLine.clear()
            self.keyLine.setText('5')
            b=5
            return b   
    def importEn(self):
        content=Files().encryptImport()
        self.plainText.setText(content)
        
    def importDe(self):
        content=Files().decryptImport()
        self.cipherText.setText(content)
    
    def encrypt(self):
        a=int(self.comboBox.currentText())
        b=self.keyValidator()
        m=26
        chars= ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        res=[]
        #char =Validate().inputVer(self.plainText.text())
        if self.keepSpaces.isChecked():
            char=Validate().inputVer(self.plainText.text())
        else:
            char=Validate().analysisCleantext(self.plainText.text())
            
            
        for i in range(len(char)):
            if char[i]==" " or char[i].isnumeric():
                res.append(char[i])
            else:
                d=chars.index(char[i])
                print(d,"d")
                vzorec=((a*d+b)%m)
                res.append(chars[vzorec]) 
            encryptedText=''.join(res)
            
            if self.exportToFile.isChecked():
                self.export(encryptedText,1)
                
        if len(encryptedText)>4: #osetreni rozdeleni na petice
            fives=' '.join(encryptedText[i:i+5] for i in range(0, len(encryptedText), 5))
            return (self.cipherTextLine.setText(fives),
                    self.cipherText.clear(), ##vrati automaticky hodnotu do pole 2
                    self.cipherText.setText(''.join(res)))
        else:
            return (self.cipherTextLine.setText(''.join(res)),
                    self.cipherText.clear(),
                    self.cipherText.setText(''.join(res)))
        
        
            
    def decrypt(self):
        def modInverse(a, m) :
            a = a % m
            for x in range(1, m) :
                if((a*x)%m==1):
                    return x
            return 1
        
        a=int(self.comboBox.currentText())
        b=self.keyValidator()
        m=26
        chars= ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        
        decres=[]
        modin = modInverse(a,m)
        #char =Validate().inputVer(self.cipherText.text())
        if self.keepSpaces.isChecked():
            char=Validate().inputVer(self.cipherText.text())
        else:
            char=Validate().analysisCleantext(self.cipherText.text())
        for i in range(len(char)):
            if char[i]==" " or char[i].isnumeric():
                decres.append(char[i])
            else:
                dechar=chars.index(char[i])
                vz=(modin*(dechar-b)%m)
                decres.append(chars[vz])
            dectext=''.join(decres)
            if self.exportToFile.isChecked():
                self.export(dectext,2)
                
        return self.plainTextLine.setText(dectext)
    
    def export(self,content,sw):
        if sw==1:
            file = open('encrypted.txt','w')
        if sw==2:
            file = open('decrypted.txt','w')
        file.write(str(content))
        file.close()
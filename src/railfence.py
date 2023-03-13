from PyQt5 import uic
from PyQt5.QtWidgets import QWidget,QMessageBox
import unicodedata
from usefull_functions import Validate
from usefull_functions import Files

import numpy as np
import sys
sys.path.append("..")
my='gui/railfencegui.ui'

class Rail(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(my, self)
        
        self.encryptBtn.clicked.connect(self.encrypt)
        self.decryptBtn.clicked.connect(self.decrypt)
        self.plainText.text()
        self.cipherText.text()
        self.keyLine.text()
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
            Validate().errmsg('Invalid key, inserting 2 as default')
            self.keyLine.clear()
            self.keyLine.setText('2')
            b=2
            return b
  
    def encrypt(self):
        text=Validate().inputVer(self.plainText.text())
        key=self.keyValidator()
        if key<2 or key>=len(text):
            Validate().errmsg("Invlaid key length, inserting 2 as default")
            self.keyLine.clear()
            self.keyLine.setText('2')
            key=2
        parsedText=[char for char in text]
        matrix=np.empty((key,len(text)),dtype="U")
        column=0
        down=True
        for row in range(len(text)):
            
            if down==False:
                if column-1>=0:
                    matrix[column][row]=parsedText[0]
                    parsedText.pop(0)
                    column=column-1
                else:
                    down=True 

            if down==True:   
                if column<=key-1:
                    matrix[column][row]=parsedText[0]
                    parsedText.pop(0)
                    column=column+1

            if column==key:
                column=column-2
                down=False
                

        encryptedText=""
        for i in range(key):
            line="".join(string for string in matrix[i] if len(string) > 0)
            encryptedText=encryptedText+line
        if self.exportToFile.isChecked():
            self.export(encryptedText,1)
        if len(encryptedText)>4:
            fives=' '.join(encryptedText[i:i+5] for i in range(0, len(encryptedText), 5))
            return (self.cipherTextLine.setText(fives),
                    self.cipherText.clear(),
                    self.cipherText.setText(''.join(encryptedText)))
        else:
            return (self.cipherTextLine.setText(''.join(encryptedText)),
                    self.cipherText.clear(),
                    self.cipherText.setText(''.join(encryptedText)))

        
    
    def decrypt(self):
        text=Validate().inputVer(self.cipherText.text())
        key=self.keyValidator()

        if key<2 or key>=len(text):
            Validate().errmsg("Invlaid key length, inserting 2 as default")
            self.keyLine.clear()
            self.keyLine.setText('2')
            key=2
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
        if self.exportToFile.isChecked():
            self.export(decrypted,2)
        return self.plainTextLine.setText(decrypted)
    
    def export(self,content,sw):
        if sw==1:
            file = open('encrypted.txt','w')
        if sw==2:
            file = open('decrypted.txt','w')
        file.write(str(content))
        file.close()
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget,QMessageBox
import unicodedata
import usefull_functions as helpers
import math
import numpy as np
from usefull_functions import Validate
from usefull_functions import Files
import sys
sys.path.append("..")
my='gui/routegui.ui'

class Route(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(my, self)
        
        self.encryptBtn.clicked.connect(self.encrypt)
        self.decryptBtn.clicked.connect(self.decrypt)
        self.plainText.text()
        self.cipherText.text()
        self.keyLine.text()
        self.radioButtonColumn.setChecked(True)
        self.keepSpaces.setChecked(False)
        self.importEnBtn.clicked.connect(self.importEn)
        self.importDeBtn.clicked.connect(self.importDe)
   
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
    
    def importEn(self):
        content=Files().encryptImport()
        self.plainText.setText(content)
        
    def importDe(self):
        content=Files().decryptImport()
        self.cipherText.setText(content)
    
    def encrypt(self):
        #text=Validate().inputVer(self.plainText.text())
        if self.keepSpaces.isChecked():
            text=Validate().inputVer(self.plainText.text())
        else:
            text=Validate().analysisCleantext(self.plainText.text())
        key=self.keyValidator() #key = num. of collumns
        if key<2 or key>=len(text):
            self.errmsg("Invlaid key length, inserting 3 as default")
            self.keyLine.clear()
            self.keyLine.setText('3')
            key=3
        rows=int(math.ceil(len(text)/key))
        matrixSize=key*rows
        if len(text)<matrixSize:
            while len(text)!=matrixSize:
                text=text+"X"
        parsedText=[char for char in text]
        matrix=np.empty((rows,key),dtype="U")   
        matrix.reshape(-1)[:len(text)] = list(text)

        result=[]
        '''
        column
        '''
        if self.radioButtonColumn.isChecked():
            for column in range(key):
                for row in range(rows):
                    result.append(matrix[row][column])
            encryptedText="".join(result)
        
        '''
        spiral counter-clockwise
        '''
        if self.radioButtonSpiral.isChecked():
            matrix=np.flip(matrix)
            matrix=matrix.transpose()
            
            top = left = 0
            bottom=key-1
            right=rows-1
            
            
            '''
            source: https://www.techiedelight.com/print-matrix-spiral-order/
            '''
            while True:
                if left>right:
                    break
         
                #top
                for i in range(left,right+1):
                    result.append(matrix[top][i])
                top+=1
    
                if top > bottom:
                    break
         
                #right
                for i in range(top,bottom+1):
                    result.append(matrix[i][right])
                right-=1
         
                if left > right:
                    break
         
                #bottom
                for i in range(right,left-1,-1):
                    result.append(matrix[bottom][i])
                bottom-=1
         
                if top > bottom:
                    break
         
                #left
                for i in range(bottom,top-1,-1):
                    result.append(matrix[i][left])
                left+=1
            '''
            end of quoted code
            '''
                
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
        #text=Validate().inputVer(self.cipherText.text())
        if self.keepSpaces.isChecked():
            text=Validate().inputVer(self.cipherText.text())
        else:
            text=Validate().analysisCleantext(self.cipherText.text())
        key=self.keyValidator()
        if key<2 or key>=len(text):
            self.errmsg("Invlaid key length, inserting 3 as default")
            self.keyLine.clear()
            self.keyLine.setText('3')
            key=3
        rows=int(math.ceil(len(text)/key))
        matrixSize=key*rows
        if len(text)<matrixSize:
            while len(text)!=matrixSize:
                text=text+"X"
        parsedText=[char for char in text]
        '''
        column
        '''
        
        if self.radioButtonColumn.isChecked():
            matrix=np.empty((rows,key),dtype="U") 
            matrix.reshape(-1)[:len(text)] = list(text)
            columns=int(len(text)/key)
            result=[]
            for i in range(columns):
                result.append(text[i::columns])
            decryptedText=''.join(result)
            return self.plainTextLine.setText(decryptedText)

        '''
        spiral counter-clockwise
        '''
        if self.radioButtonSpiral.isChecked():
            matrix=np.empty((key,rows),dtype="U") 
            matrix.reshape(-1)[:len(text)] = list(text)
            
            top=left=0
            bottom=key-1
            right=rows-1
    
            '''
            source: https://www.techiedelight.com/print-matrix-spiral-order/
            '''
            while True:
                if left>right:
                    break
         
                #top
                for i in range(left,right+1):
                    matrix[top][i]=parsedText[0]
                    parsedText.pop(0)
                top+=1
    
                if top > bottom:
                    break
         
                #right
                for i in range(top,bottom+1):
                    matrix[i][right]=parsedText[0]
                    parsedText.pop(0)
                right-=1
         
                if left > right:
                    break
         
                #bottom
                for i in range(right,left-1,-1):
                    matrix[bottom][i]=parsedText[0]
                    parsedText.pop(0)
                bottom-=1
         
                if top > bottom:
                    break
         
                #left
                for i in range(bottom,top-1,-1):
                    matrix[i][left]=parsedText[0]
                    parsedText.pop(0)
                left+=1
                
    
            matrix=np.flip(matrix)
            matrix=matrix.transpose()
            
            decryptedText=""
            for i in range(rows):
                line="".join(string for string in matrix[i] if len(string) > 0)
                decryptedText=decryptedText+line
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
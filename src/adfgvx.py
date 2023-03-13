from PyQt5 import uic
from PyQt5.QtWidgets import QWidget,QMessageBox
import unicodedata
import random
import itertools
from usefull_functions import Validate
from usefull_functions import Files

import sys
sys.path.append("..")
my='gui/adfgvxgui.ui'

class Adf(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(my, self)
        
        self.encryptBtn.clicked.connect(self.encrypt)
        self.buttonShowMatrix.clicked.connect(self.matrixdisplay)
        self.decryptBtn.clicked.connect(self.decrypt)
        self.keyLine.text()
        self.radioButtonEN.setChecked(True)
        self.buttonPool.clicked.connect(self.alpinput)
        self.buttonGenerateRandom.clicked.connect(self.randomchars)
        self.keepSpaces.setChecked(False)
        self.importEnBtn.clicked.connect(self.importEn)
        self.importDeBtn.clicked.connect(self.importDe)
    
    def importEn(self):
        content=Files().encryptImport()
        self.plainText.setText(content)
        
    def importDe(self):
        content=Files().decryptImport()
        self.cipherText.setText(content)
    
    def errmsg(self,message): #vyhazuje error cuz fancy
        msg = QMessageBox()
        msg.setWindowTitle("Input Error")
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.exec_()
     
    def strip_accents(self,text):
        try:
            text = unicode(text, 'utf-8')
        except NameError: # unicode is a default on python 3 
                pass
        text = unicodedata.normalize('NFD', text)\
                .encode('ascii', 'ignore')\
                .decode("utf-8")
        return str(text)

    def matice(self,chars):  #vytvori matici s klicem
        matrix = [[None] * 5 for i in range(5)]
        full_string =chars #keyword + alphabet     
        for i in range(25):
            matrix[i // 5][i % 5] = full_string[i]   
        for row in matrix:
             print(row)       
        return matrix

    ########################################
    def makec(self): ##osetreni klice
        key = self.keyLine.text()
        key=key.upper()
        key=self.strip_accents(key)
        res = [] 
        for i in key:
            if i not in res: 
                res.append(i)
        key=''.join([*filter(str.isalpha, res)])
        return key
    
    def alpinput(self):
        self.textEditPoolLeft.clear()
        if self.radioButtonAll.isChecked():
            pool= ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",'0','1','2','3','4','5','6','7','8','9']
        elif self.radioButtonEN.isChecked():pool= ["A","B","C","D","E","F","G","H","I","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        elif self.radioButtonCZ.isChecked():pool= ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","R","S","T","U","V","W","X","Y","Z"]
            
        #else: pool= ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        pooltaken=self.textEditInputMatrix.toPlainText()#################################
        
        if self.radioButtonAll.isChecked():
            pooltaken=self.makechars2(pooltaken)
        else: pooltaken=self.makechars(pooltaken)
        poolwritten=[]
        for i in range(len(pooltaken)):
            poolwritten.append(pooltaken[i])
            pool.remove(pooltaken[i])
        
        if len(pool)>0: self.textEditPoolLeft.setText(str(pool))
        return poolwritten
    
    def randomchars(self):
        if self.radioButtonAll.isChecked():
            chars= ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",'0','1','2','3','4','5','6','7','8','9']
        elif self.radioButtonEN.isChecked():chars= ["A","B","C","D","E","F","G","H","I","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        elif self.radioButtonCZ.isChecked():chars= ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","R","S","T","U","V","W","X","Y","Z"]
        random.shuffle(chars) ## generuje random abecedu
        c=''
        c=c.join(chars)
        return self.textEditInputMatrix.setText(c)
    
    def makechars(self,chars):
        chars=chars.upper()
        
        if self.radioButtonEN.isChecked():
                chars=chars.replace('J','I')#I
        if self.radioButtonCZ.isChecked():
            chars=chars.replace('Q','O')#O
        
        chars=self.strip_accents(chars)
        res = [] 
        for i in chars:
            if i not in res: 
                res.append(i)      
        chars=''.join([*filter(str.isalpha, res)])
        return chars
    
        
    def make(self,char):
        char = char.replace(" ", "XMEZERAX")
        char=''.join([*filter(str.isalpha, char)])
       # char = char.replace("XMEZERAX", " ")
        char=self.strip_accents(char)
        char=char.upper()
        if self.radioButtonEN.isChecked():
            char=char.replace('J','I')
        if self.radioButtonCZ.isChecked():
            char=char.replace('Q','O')
        return char
    

    
    def loc(self,char,matrix):
           hel=[]
           for v in range(len(char)):       
               loc=[]          
               for i ,j in enumerate(matrix):
                   for k,l in enumerate(j):
                       if char[v]==l:
                           loc.append(i)
                           loc.append(k)
                           hel.append(loc)
           return hel
    
    def matrixdisplay(self): ##vypise matici na vystup
        if self.radioButtonAll.isChecked():
             if len(self.alpinput())<35:
                self.errmsg('Matrix is missing characters')
                return
             matrix=self.maticedruha(self.alpinput())
        else:
            if len(self.alpinput())<25:
                self.errmsg('Matrix is missing characters')
                return
            matrix=self.matice(self.alpinput())
        return self.matrixField.setText(str(matrix))
    
    def encrypt(self):
        if self.radioButtonAll.isChecked():
            if len(self.alpinput())<35:
                self.errmsg('Matrix is missing characters')
                return
            return self.encryptv()
        else:
            if len(self.alpinput())<25:
                self.errmsg('Matrix is missing characters')
                return
        chars=self.alpinput()
 
        key=self.makec()
        #text=self.plainText.text()
        if self.keepSpaces.isChecked():
            text=Validate().inputVer(self.plainText.text())
        else:
            text=Validate().analysisCleantext(self.plainText.text())
        text=self.make(text)
        if len(key)==0:self.errmsg('Non valid key');return
        if len(text)==0:self.errmsg('Input text is too short');return
        
        if (len(key)*2)>len(text):
            self.errmsg('Key is too long')
            return
        
        matrix=self.matice(chars)
        res=self.loc(text,matrix)
        #print(res,'lokace')
        flat=itertools.chain.from_iterable(res)
        te=list(flat)
      
        for n, i in enumerate(te):
            if i == 0:te[n] = 'A'
            if i == 1:te[n] = 'D'
            if i == 2:te[n] = 'F'
            if i == 3:te[n] = 'G'
            if i == 4:te[n] = 'X'      
  
        sortedkey=[i[0] for i in sorted(enumerate(key), key=lambda x:x[1])]
        encrypted=[]
        for i in sortedkey:
            for j in range(i,len(te),len(key)):
                encrypted.append(te[j])
        encryptedstr=''.join(encrypted)
        if self.exportToFile.isChecked():
            self.export(encryptedstr,1)
        fives=' '.join(encryptedstr[i:i+(len(key))] for i in range(0, len(encryptedstr), (len(key))))
        return (self.cipherTextLine.setText(fives),
                self.cipherText.clear(),
                self.cipherText.setText(encryptedstr))
    
    def decrypt(self):
        if self.radioButtonAll.isChecked():
            if len(self.alpinput())<35:
                self.errmsg('Matrix is missing characters')
                return
            return self.decryptv()
        else:
            if len(self.alpinput())<25:
                self.errmsg('Matrix is missing characters')
                return
        chars=self.alpinput()
        key=self.makec()
        matrix=self.matice(chars)
        #encryptedstr=self.cipherText.text()
        if self.keepSpaces.isChecked():
            encryptedstr=Validate().inputVer(self.cipherText.text())
        else:
            text=Validate().analysisCleantext(self.cipherText.text())
            encryptedstr=text
            
        text=list(encryptedstr)
        encrypted=text
        if len(key)==0:self.errmsg('Non valid key');return
        if len(text)==0:self.errmsg('Input text is too short');return
        sortedkey=[i[0] for i in sorted(enumerate(key), key=lambda x:x[1])]
        
        ind=[]
        for i in sortedkey:
            for j in range(i,len(text),len(key)):
                ind.append(j)
        
        for i in range(len(ind)):
            encryptedstr=encryptedstr[:ind[i]]+encrypted[i]+encryptedstr[ind[i]+1:]
        encryptedstr=list(encryptedstr)

        for i in range(len(encryptedstr)):
            if encryptedstr[i]=='A':encryptedstr[i]=0
            if encryptedstr[i]=='D':encryptedstr[i]=1
            if encryptedstr[i]=='F':encryptedstr[i]=2
            if encryptedstr[i]=='G':encryptedstr[i]=3
            if encryptedstr[i]=='X':encryptedstr[i]=4

        ad=0
        dectext=[]
        for i in range(int(len(encryptedstr)/2)):
            dectext.append(matrix[encryptedstr[ad]][encryptedstr[ad+1]])
            ad=ad+2
        result=''.join(dectext)
        result=result.replace('XMEZERAX', ' ')
        
        if self.exportToFile.isChecked():
            self.export(result,2)
        return self.plainTextLine.setText(''.join(result))
        
       
    def maticedruha(self,chars):  #vytvori matici s klicem
        matrix = [[None] * 6 for i in range(6)]
        full_string =chars #keyword + alphabet     
        for i in range(36):
            matrix[i // 6][i % 6] = full_string[i]   
        for row in matrix:
             print(row)       
        return matrix

    def makechars2(self,chars):
        chars=chars.upper()
        chars=self.strip_accents(chars)
        res = [] 
        for i in chars:
            if i not in res: 
                res.append(i)      
        chars=''.join([*filter(str.isalnum, res)])
        return chars
    
        
    def make2(self,char):
        char = char.replace(" ", "XMEZERAX")
        char=''.join([*filter(str.isalnum, char)])
        char=self.strip_accents(char)
        char=char.upper()
        return char
    
    def encryptv(self):
        chars=self.alpinput()
        key=self.makec()
        text=self.plainText.text()
        text=self.make2(text)
        if len(key)==0:self.errmsg('Non valid key');return
        if len(text)==0:self.errmsg('Input text is too short');return
        matrixdruha=self.maticedruha(chars)
        res=self.loc(text,matrixdruha)
        
        flat=itertools.chain.from_iterable(res)
        te=list(flat)    
        
        for n, i in enumerate(te):
            if i == 0:te[n] = 'A'
            if i == 1:te[n] = 'D'
            if i == 2:te[n] = 'F'
            if i == 3:te[n] = 'G'
            if i == 4:te[n] = 'V'
            if i == 5:te[n] = 'X'
        sortedkey=[i[0] for i in sorted(enumerate(key), key=lambda x:x[1])]     
        encrypted=[]
        for i in sortedkey:
            for j in range(i,len(te),len(key)):
                encrypted.append(te[j])

        encryptedstr=''.join(encrypted)
        fives=' '.join(encryptedstr[i:i+len(key)] for i in range(0, len(encryptedstr), len(key)))
        return (self.cipherTextLine.setText(fives),
                self.cipherText.clear(),
                self.cipherText.setText(encryptedstr))
    ########################################## DEC
    def decryptv(self):
        chars=self.alpinput()
        key=self.makec()
        matrixdruha=self.maticedruha(chars)
        encryptedstr=self.cipherText.text()
        
        text=list(encryptedstr)
        encrypted=text
        if len(key)==0: self.errmsg('Non valid key');return
        if len(text)==0:self.errmsg('Input text is too short');return
        sortedkey=[i[0] for i in sorted(enumerate(key), key=lambda x:x[1])]
        
        ind=[]
        for i in sortedkey:
            for j in range(i,len(text),len(key)):
                ind.append(j)
        
        for i in range(len(ind)):
            encryptedstr=encryptedstr[:ind[i]]+encrypted[i]+encryptedstr[ind[i]+1:]
        encryptedstr=list(encryptedstr)

        for i in range(len(encryptedstr)):
            if encryptedstr[i]=='A':encryptedstr[i]=0
            if encryptedstr[i]=='D':encryptedstr[i]=1
            if encryptedstr[i]=='F':encryptedstr[i]=2
            if encryptedstr[i]=='G':encryptedstr[i]=3
            if encryptedstr[i]=='V':encryptedstr[i]=4
            if encryptedstr[i]=='X':encryptedstr[i]=5
        
        ad=0
        dectext=[]
        for i in range(int(len(encryptedstr)/2)):
            dectext.append(matrixdruha[encryptedstr[ad]][encryptedstr[ad+1]])
            ad=ad+2
        result=''.join(dectext)
        result=result.replace('XMEZERAX', ' ')
        return self.plainTextLine.setText(''.join(result))

    def export(self,content,sw):
        if sw==1:
            file = open('encrypted.txt','w')
        if sw==2:
            file = open('decrypted.txt','w')
        file.write(str(content))
        file.close()
        

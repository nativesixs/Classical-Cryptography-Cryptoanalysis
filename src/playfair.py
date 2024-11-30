from PyQt5 import uic
from PyQt5.QtWidgets import QWidget,QMessageBox
import unicodedata
import sys
from PyQt5 import uic

from PyQt5.QtWidgets import QMessageBox
import unicodedata
import operator
from utils import Validate
from utils import Files


import sys
sys.path.append("..")
my='gui/playfairgui.ui'

class Playfair(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(my, self)
        
        self.encryptBtn.clicked.connect(self.encrypt)
        self.buttonShowMatrix.clicked.connect(self.matrixdisplay)
        self.decryptBtn.clicked.connect(self.decrypt)
        self.keyLine.text()
        self.radioButtonEN.setChecked(True)
        self.keepSpaces.setChecked(False)
        self.importEnBtn.clicked.connect(self.importEn)
        self.importDeBtn.clicked.connect(self.importDe)
    
    def importEn(self):
        content=Files().encryptImport()
        self.plainText.setText(content)
        
    def importDe(self):
        content=Files().decryptImport()
        self.cipherText.setText(content)
    
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
        key = self.keyLine.text()
        key=key.upper()
        key=self.strip_accents(key)
        res = [] 
        for i in key:
            if i not in res: 
                res.append(i)
        key=''.join([*filter(str.isalpha, res)])   
        return key
    
    '''
    CZ - Q  O (dplnek je X,Q)
    EN - J I (dplnek je Z,X)
    v klici vyhodim duplicity tzn. kočka bude koca
    
    ve dvou dvojicich se muzou opakovat znaky
    string: maassefaajn
    bude: ma,as,se,fa,aj,nz
    kdyz je treba aa,bb,cc bude = az,ab,bc,cz
    na petice se seka i zasifrovany text
    '''
    def errmsg(self,message):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.exec_()
    
    def getnums(self,char,op):
        key=self.makec()
        cislahod=[]
        cislaind=[]
        for i,c in enumerate(char):
            if c.isdigit():
                cislaind.append(i)
                cry = (op(int(c), len(key)) % 10)
                cislahod.append(cry)   
        if len(key)==0 and len(cislahod)!=0:
            self.errmsg('Numbers wont be encrypted because key is empty')
        return cislahod,cislaind
    
    def getspace(self,char):
        cislaind=[]
        for i,c in enumerate(char):
            if c==' ':  
                cislaind.append(i)
        return cislaind 
    
    def make(self,char): 
        char=''.join([*filter(str.isalpha, char)])
        char=self.strip_accents(char)
        char=char.upper()
        if self.radioButtonEN.isChecked():
            char=char.replace('J','I')
        if self.radioButtonCZ.isChecked():
            char=char.replace('Q','O')
        tosix=0
        for i in range(int(len(char)/2)):
            if (char[tosix:tosix+2][0])==(char[tosix:tosix+2][1]):
                if (char[tosix:tosix+2][0])=='Z'and(char[tosix:tosix+2][1])=='Z':
                    char=(char[:tosix+1]+'X'+char[tosix+1:])
                else:
                    char=(char[:tosix+1]+'Z'+char[tosix+1:])
                return self.make(char)
            tosix=tosix+2
        return char
        
    
    def matrixdisplay(self):
        matrix=self.matice()
        return self.matrixField.setText(str(matrix))

    def matice(self):
        chars = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        key=self.makec()

        sd = set(chars) - set(key)
        ld = list(sd)
        abc=list(key)+sorted(ld)
        
        if self.radioButtonEN.isChecked():
            abc.remove("J") 
        if self.radioButtonCZ.isChecked():
            abc.remove("Q")
        
        matrix = [[None] * 5 for i in range(5)]
        full_string =abc
        
        for i in range(25):
            matrix[i // 5][i % 5] = full_string[i]
         
        for row in matrix:
            print(row)
        return matrix
        
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
        print(hel)
        return hel     

    def checkodd(self,char):
            c=""
            if self.radioButtonEN.isChecked():
                dopln='Z'
                dopln2='X'
            if self.radioButtonCZ.isChecked():
                dopln='Z'
                dopln2='X'
            if char[-1]==dopln:
                c=char[:]+dopln2
            else:
                c=char[:]+dopln
            char=c
            return char
        
        
    def encrypt(self):
        if self.keepSpaces.isChecked():
            char=Validate().inputVer(self.plainText.text())
        else:
            char=Validate().analysisCleantext(self.plainText.text())
        spaces=self.getspace(char) 
        cisla=self.getnums(char,operator.add)
        char=self.make(char)
        matrix=self.matice()
        if len(char)%2!=0:
            char=self.checkodd(char)    
        hel=self.loc(char,matrix)
        v1=[]
        t=0
        h=0
        for i in range(int(len(char)/2)):
            pom=hel[t]
            pom2=hel[h+1]
            if pom[1]==pom2[1]:
                if pom[0]==4:
                    v1.append(matrix[pom[0]-4][pom[1]])
                if pom[0]!=4: 
                    v1.append(matrix[pom[0]+1][pom[1]])     
                if pom2[0]==4:
                    v1.append(matrix[pom2[0]-4][pom2[1]])
                if pom2[0]!=4: 
                    v1.append(matrix[pom2[0]+1][pom2[1]])
                                    
            if pom[0]==pom2[0]:
                if pom[0]==pom[0]:
                    if pom[1]==4:
                        v1.append(matrix[pom[0]][pom[1]-4])
                    if pom[1]!=4:
                        v1.append(matrix[pom[0]][pom[1]+1])
                    if pom2[1]==4:
                        v1.append(matrix[pom2[0]][pom2[1]-4])
                    if pom2[1]!=4:
                        v1.append(matrix[pom2[0]][pom2[1]+1])
                    
            else:
                prev=pom[1]
                while pom[1]!=pom2[1]:
                    if pom[1]<pom2[1]:
                        pom[1]=pom[1]+1
                        if pom[1]==pom2[1]:
                            posun=pom[1]
                            dist=posun-prev
                            v1.append(matrix[pom[0]][posun])
                            v1.append(matrix[pom2[0]][pom2[1]-dist])
                    if pom[1]>pom2[1]:
                        pom[1]=pom[1]-1
                        if pom[1]==pom2[1]:
                            posun=pom[1]
                            dist=posun-prev
                            v1.append(matrix[pom[0]][posun])
                            v1.append(matrix[pom2[0]][pom2[1]-dist])
                    
            t=t+2
            h=h+2     
        for i in range(len(spaces)): 
            v1.insert(spaces[i],' ')
        if len(cisla[0])>=1:
            for i in range(len(cisla[0])):
                v1.insert(cisla[1][i],cisla[0][i])
        dec1string=''.join(map(str, v1))
        if self.exportToFile.isChecked():
            self.export(dec1string,1)
        
        if len(dec1string)>4:
            fives=' '.join(dec1string[i:i+5] for i in range(0, len(dec1string), 5))
            return (self.cipherTextLine.setText(fives),
                    self.cipherText.clear(),
                    self.cipherText.setText(''.join(dec1string)))
        else:
            return (self.cipherTextLine.setText(''.join(dec1string)),
                    self.cipherText.clear(),
                    self.cipherText.setText(''.join(dec1string)))
        
    
    def decrypt(self):
        if self.keepSpaces.isChecked():
            char=Validate().inputVer(self.cipherText.text())
        else:
            char=Validate().analysisCleantext(self.cipherText.text())
        spaces=self.getspace(char) 
        cisla=self.getnums(char,operator.sub)
        char=self.make(char)
        matrix=self.matice()
        if len(char)%2!=0:
            char=self.checkodd(char)
        hel=self.loc(char,matrix)
        v1=[]    
        t=0
        h=0  
        for i in range(int(len(char)/2)):
            pom=hel[t]
            pom2=hel[h+1]
            if pom[1]==pom2[1]:
                if pom[0]==4:
                    v1.append(matrix[pom[0]-1][pom[1]])
                if pom[0]!=4: 
                    v1.append(matrix[pom[0]-1][pom[1]])     
                if pom2[0]==4:
                    v1.append(matrix[pom2[0]-1][pom2[1]])
                if pom2[0]!=4: 
                    v1.append(matrix[pom2[0]-1][pom2[1]])
                 
            if pom[0]==pom2[0]:
                if pom[0]==pom[0]:
                    if pom[1]==0:
                        v1.append(matrix[pom[0]][pom[1]+4])
                    if pom[1]!=0:
                        v1.append(matrix[pom[0]][pom[1]-1])
                    if pom2[1]==0:
                        v1.append(matrix[pom2[0]][pom2[1]+4])
                    if pom2[1]!=0:
                        v1.append(matrix[pom2[0]][pom2[1]-1])
                    
            else:
                prev=pom[1]
                while pom[1]!=pom2[1]:
                    if pom[1]<pom2[1]:
                        pom[1]=pom[1]+1
                        if pom[1]==pom2[1]:
                            posun=pom[1]
                            dist=posun-prev
                            v1.append(matrix[pom[0]][posun])
                            v1.append(matrix[pom2[0]][pom2[1]-dist])
                    if pom[1]>pom2[1]:
                        pom[1]=pom[1]-1
                        if pom[1]==pom2[1]:
                            posun=pom[1]
                            dist=posun-prev
                            v1.append(matrix[pom[0]][posun])
                            v1.append(matrix[pom2[0]][pom2[1]-dist])                  
                    
            t=t+2
            h=h+2  
        for i in range(len(spaces)): 
            v1.insert(spaces[i],' ')
        if len(cisla[0])>=1:
            for i in range(len(cisla[0])):
                v1.insert(cisla[1][i],cisla[0][i])
        dec1string=''.join(map(str, v1))
        if self.exportToFile.isChecked():
            self.export(dec1string,2)
        return self.plainTextLine.setText(dec1string)
    
    def export(self,content,sw):
        if sw==1:
            file = open('encrypted.txt','w')
        if sw==2:
            file = open('decrypted.txt','w')
        file.write(str(content))
        file.close()
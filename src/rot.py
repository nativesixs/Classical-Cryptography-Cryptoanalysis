from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from utils import Validate
from utils import Files
import sys
sys.path.append("..")
my='gui/rotgui.ui'
class Rot(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(my, self)
        self.encryptBtn.clicked.connect(self.cryp)
        self.decryptBtn.clicked.connect(self.decryp)
        self.plainText.text()
        self.cipherText.text()
        self.importEnBtn.clicked.connect(self.importEn)
        self.importDeBtn.clicked.connect(self.importDe)
     
    def importEn(self):
        content=Files().encryptImport()
        self.plainText.setText(content)
        
    def importDe(self):
        content=Files().decryptImport()
        self.cipherText.setText(content)
        
    def cryp(self):
        char=Validate().inputVer(self.plainText.text())
        char=''.join([*filter(str.isalpha, char)])
        char=Validate().strip_accents(char)
        chars= ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        passed=[]
        for i in range(len(char)):
            currentIndex=chars.index(char[i])
            if currentIndex>=13:#24
                newIndex=26-currentIndex#37
                newIndex=13-newIndex#13
            else:
                newIndex=currentIndex+13#13
            passed.append(chars[newIndex])
            encryptedText=''.join(passed)
        if self.exportToFile.isChecked():
            self.export(encryptedText,1)
        if len(encryptedText)>4:
            fives=' '.join(encryptedText[i:i+5] for i in range(0, len(encryptedText), 5))
            return (self.cipherTextLine.setText(fives),
                    self.cipherText.clear(),
                    self.cipherText.setText(''.join(passed)))
        else:
            return (self.cipherTextLine.setText(''.join(passed)),
                    self.cipherText.clear(),
                    self.cipherText.setText(''.join(passed)))
        
        
    
    def decryp(self):
        char=Validate().inputVer(self.cipherText.text())
        chars= ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        passed=[]
        for i in range(len(char)):
            currentIndex=chars.index(char[i])
            if currentIndex<=12:#12
                newIndex=13-currentIndex#13
                newIndex=26-newIndex#37
            else:
                newIndex=currentIndex-13#13    
            passed.append(chars[newIndex])
        if self.exportToFile.isChecked():
            self.export(''.join(passed),2)
        return self.plainTextLine.setText(''.join(passed))
    
    def export(self,content,sw):
        if sw==1:
            file = open('encrypted.txt','w')
        if sw==2:
            file = open('decrypted.txt','w')
        file.write(str(content))
        file.close()
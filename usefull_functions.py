from PyQt5 import uic
from PyQt5.QtWidgets import QWidget,QMessageBox,QFileDialog
import unicodedata

class Validate():
    
    
    
    def strip_accents(self,text):
        try:
            text = unicode(text, 'utf-8')
        except NameError: 
                pass
        text = unicodedata.normalize('NFD', text)\
                .encode('ascii', 'ignore')\
                .decode("utf-8")
        return str(text)
    
    
    def inputVer(self,char):
        #char = self.lineEditHodnotaA.text()
        char=char.upper()
        char=self.strip_accents(char)
        char = char.replace(" ", "XMEZERAX")
        char=''.join([*filter(str.isalnum, char)])
        char = char.replace("XMEZERAX", " ")
        return char
    
    def errmsg(self,message): 
        msg = QMessageBox()
        msg.setWindowTitle("Input Error")
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.exec_()
        
    def analysisCleantext(self,text):
        text=''.join([*filter(str.isalpha, text)]).upper()
        text=self.strip_accents(text)
        return text
    #Validate().analysisCleantext(self.plainText.text())
class Files(QWidget): 
    
    def encryptImport(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Text files (*.txt)", options=options)
        with open(file, 'r') as f:
            content = f.read()
        #content=file.read()
        content=''.join([*filter(str.isalpha,content)]).upper()
        f.close()
        return content
    
    def decryptImport(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Text files (*.txt)", options=options)
        with open(file, 'r') as f:
            content = f.read()
        #content=file.read()
        content=''.join([*filter(str.isalpha,content)]).upper()
        f.close()
        return content
    
        
        
        
        
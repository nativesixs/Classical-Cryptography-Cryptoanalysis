import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, uic
import unicodedata
from ui_mainWindow import Ui_MainWindow

from src.affine import Affine
from src.adfgvx import Adf
from src.rot import Rot
from src.railfence import Rail
from src.route import Route
from src.vigenere import Vigenere
from src.scytale import Scytale
from src.playfair import Playfair
from src.breakCipher import Breaker
from src.analysis import Analysis



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('bpdraftgui.ui', self)
        self.stackedWidget.setCurrentWidget(self.centralwidget)
        self.affineBtn.clicked.connect(self.gotoAffine)
        self.adfgvxBtn.clicked.connect(self.gotoAdf)
        self.rot13Btn.clicked.connect(self.gotoRot)
        self.railfenceBtn.clicked.connect(self.gotoRail)
        self.routeBtn.clicked.connect(self.gotoRoute)
        self.vigenereBtn.clicked.connect(self.gotoVigenere)
        self.scytaleBtn.clicked.connect(self.gotoScytale)
        self.playfairBtn.clicked.connect(self.gotoPlayfair)     
        self.breakerBtn.clicked.connect(self.gotoBreaker)      
        self.analysisBtn.clicked.connect(self.gotoAnalysis)
        self.aboutBtn.triggered.connect(self.about)
    def about(self):
        self.stackedWidget.setCurrentWidget(self.aboutPage)

    def gotoAdf(self):
        self.adf=Adf()
        self.stackedWidget.addWidget(self.adf)  
        self.stackedWidget.setCurrentWidget(self.adf)


    def gotoAffine(self):
        self.affine=Affine()
        self.stackedWidget.addWidget(self.affine)   
        self.stackedWidget.setCurrentWidget(self.affine)
        
    def gotoRot(self):
        self.rot=Rot()
        self.stackedWidget.addWidget(self.rot)   
        self.stackedWidget.setCurrentWidget(self.rot)
        
    def gotoRail(self):
        self.rail=Rail()
        self.stackedWidget.addWidget(self.rail)   
        self.stackedWidget.setCurrentWidget(self.rail)
        
    def gotoRoute(self):
        self.route=Route()
        self.stackedWidget.addWidget(self.route)   
        self.stackedWidget.setCurrentWidget(self.route)
        
    def gotoVigenere(self):
        self.vigenere=Vigenere()
        self.stackedWidget.addWidget(self.vigenere)   
        self.stackedWidget.setCurrentWidget(self.vigenere)
        
    def gotoScytale(self):
        self.scytale=Scytale()
        self.stackedWidget.addWidget(self.scytale)   
        self.stackedWidget.setCurrentWidget(self.scytale)

    def gotoPlayfair(self):
        self.playfair=Playfair()
        self.stackedWidget.addWidget(self.playfair)
        self.stackedWidget.setCurrentWidget(self.playfair)
        
    def gotoBreaker(self):
        self.breaker=Breaker()
        self.stackedWidget.addWidget(self.breaker)
        self.stackedWidget.setCurrentWidget(self.breaker)
    
    def gotoAnalysis(self):
        self.analysis=Analysis()
        self.stackedWidget.addWidget(self.analysis)
        self.stackedWidget.setCurrentWidget(self.analysis)
    
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
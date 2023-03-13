# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bpdraftgui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(848, 500)
        MainWindow.setMinimumSize(QtCore.QSize(500, 500))
        MainWindow.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0.573682, y1:0, x2:0.574364, y2:1, stop:0 rgba(100, 100, 100, 255), stop:1 rgba(133, 133, 133, 255));\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(1, 1, 2, 1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.affineBtn = QtWidgets.QPushButton(self.centralwidget)
        self.affineBtn.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.affineBtn.sizePolicy().hasHeightForWidth())
        self.affineBtn.setSizePolicy(sizePolicy)
        self.affineBtn.setMinimumSize(QtCore.QSize(75, 0))
        self.affineBtn.setBaseSize(QtCore.QSize(500, 100))
        self.affineBtn.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.affineBtn.setStyleSheet("QPushButton {\n"
"  qproperty-alignment: \'AlignVCenter | AlignRight\';\n"
"  border: 1px solid gray;\n"
"    background-color: qlineargradient(spread:reflect, x1:0.573682, y1:0, x2:0.574364, y2:1, stop:0 rgba(178, 178, 178, 255), stop:1 rgba(153, 153, 153, 255));\n"
"    \n"
"    border-color: rgb(108, 108, 108);\n"
"}\n"
"QPushButton:pressed{\n"
"background-color: rgb(130, 130, 130);\n"
"/*background-color: qlineargradient(spread:reflect, x1:0.573682, y1:0, x2:0.574364, y2:1, stop:0 rgba(188, 188, 188, 255), stop:1 rgba(130, 130, 130, 255));*/\n"
"}\n"
"\n"
"")
        self.affineBtn.setObjectName("affineBtn")
        self.verticalLayout.addWidget(self.affineBtn)
        self.adfgvxBtn = QtWidgets.QPushButton(self.centralwidget)
        self.adfgvxBtn.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.adfgvxBtn.sizePolicy().hasHeightForWidth())
        self.adfgvxBtn.setSizePolicy(sizePolicy)
        self.adfgvxBtn.setMinimumSize(QtCore.QSize(75, 0))
        self.adfgvxBtn.setBaseSize(QtCore.QSize(500, 100))
        self.adfgvxBtn.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.adfgvxBtn.setStyleSheet("QPushButton {\n"
"  qproperty-alignment: \'AlignVCenter | AlignRight\';\n"
"  border: 1px solid gray;\n"
"    background-color: qlineargradient(spread:reflect, x1:0.573682, y1:0, x2:0.574364, y2:1, stop:0 rgba(178, 178, 178, 255), stop:1 rgba(153, 153, 153, 255));\n"
"    \n"
"    border-color: rgb(108, 108, 108);\n"
"}\n"
"QPushButton:pressed{\n"
"background-color: rgb(130, 130, 130);\n"
"/*background-color: qlineargradient(spread:reflect, x1:0.573682, y1:0, x2:0.574364, y2:1, stop:0 rgba(188, 188, 188, 255), stop:1 rgba(130, 130, 130, 255));*/\n"
"}\n"
"\n"
"")
        self.adfgvxBtn.setObjectName("adfgvxBtn")
        self.verticalLayout.addWidget(self.adfgvxBtn)
        self.playfairBtn = QtWidgets.QPushButton(self.centralwidget)
        self.playfairBtn.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playfairBtn.sizePolicy().hasHeightForWidth())
        self.playfairBtn.setSizePolicy(sizePolicy)
        self.playfairBtn.setMinimumSize(QtCore.QSize(75, 0))
        self.playfairBtn.setBaseSize(QtCore.QSize(500, 100))
        self.playfairBtn.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.playfairBtn.setStyleSheet("QPushButton {\n"
"  qproperty-alignment: \'AlignVCenter | AlignRight\';\n"
"  border: 1px solid gray;\n"
"    background-color: qlineargradient(spread:reflect, x1:0.573682, y1:0, x2:0.574364, y2:1, stop:0 rgba(178, 178, 178, 255), stop:1 rgba(153, 153, 153, 255));\n"
"    \n"
"    border-color: rgb(108, 108, 108);\n"
"}\n"
"QPushButton:pressed{\n"
"background-color: rgb(130, 130, 130);\n"
"/*background-color: qlineargradient(spread:reflect, x1:0.573682, y1:0, x2:0.574364, y2:1, stop:0 rgba(188, 188, 188, 255), stop:1 rgba(130, 130, 130, 255));*/\n"
"}\n"
"\n"
"")
        self.playfairBtn.setObjectName("playfairBtn")
        self.verticalLayout.addWidget(self.playfairBtn)
        self.rot13Btn = QtWidgets.QPushButton(self.centralwidget)
        self.rot13Btn.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rot13Btn.sizePolicy().hasHeightForWidth())
        self.rot13Btn.setSizePolicy(sizePolicy)
        self.rot13Btn.setMinimumSize(QtCore.QSize(75, 0))
        self.rot13Btn.setBaseSize(QtCore.QSize(500, 100))
        self.rot13Btn.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.rot13Btn.setStyleSheet("QPushButton {\n"
"  qproperty-alignment: \'AlignVCenter | AlignRight\';\n"
"  border: 1px solid gray;\n"
"    background-color: qlineargradient(spread:reflect, x1:0.573682, y1:0, x2:0.574364, y2:1, stop:0 rgba(178, 178, 178, 255), stop:1 rgba(153, 153, 153, 255));\n"
"    \n"
"    border-color: rgb(108, 108, 108);\n"
"}\n"
"QPushButton:pressed{\n"
"background-color: rgb(130, 130, 130);\n"
"/*background-color: qlineargradient(spread:reflect, x1:0.573682, y1:0, x2:0.574364, y2:1, stop:0 rgba(188, 188, 188, 255), stop:1 rgba(130, 130, 130, 255));*/\n"
"}\n"
"\n"
"")
        self.rot13Btn.setObjectName("rot13Btn")
        self.verticalLayout.addWidget(self.rot13Btn)
        self.railfenceBtn = QtWidgets.QPushButton(self.centralwidget)
        self.railfenceBtn.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.railfenceBtn.sizePolicy().hasHeightForWidth())
        self.railfenceBtn.setSizePolicy(sizePolicy)
        self.railfenceBtn.setMinimumSize(QtCore.QSize(75, 0))
        self.railfenceBtn.setBaseSize(QtCore.QSize(500, 100))
        self.railfenceBtn.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.railfenceBtn.setStyleSheet("QPushButton {\n"
"  qproperty-alignment: \'AlignVCenter | AlignRight\';\n"
"  border: 1px solid gray;\n"
"    background-color: qlineargradient(spread:reflect, x1:0.573682, y1:0, x2:0.574364, y2:1, stop:0 rgba(178, 178, 178, 255), stop:1 rgba(153, 153, 153, 255));\n"
"    \n"
"    border-color: rgb(108, 108, 108);\n"
"}\n"
"QPushButton:pressed{\n"
"background-color: rgb(130, 130, 130);\n"
"/*background-color: qlineargradient(spread:reflect, x1:0.573682, y1:0, x2:0.574364, y2:1, stop:0 rgba(188, 188, 188, 255), stop:1 rgba(130, 130, 130, 255));*/\n"
"}\n"
"\n"
"")
        self.railfenceBtn.setObjectName("railfenceBtn")
        self.verticalLayout.addWidget(self.railfenceBtn)
        self.routeBtn = QtWidgets.QPushButton(self.centralwidget)
        self.routeBtn.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.routeBtn.sizePolicy().hasHeightForWidth())
        self.routeBtn.setSizePolicy(sizePolicy)
        self.routeBtn.setMinimumSize(QtCore.QSize(75, 0))
        self.routeBtn.setBaseSize(QtCore.QSize(500, 100))
        self.routeBtn.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.routeBtn.setStyleSheet("QPushButton {\n"
"  qproperty-alignment: \'AlignVCenter | AlignRight\';\n"
"  border: 1px solid gray;\n"
"    background-color: qlineargradient(spread:reflect, x1:0.573682, y1:0, x2:0.574364, y2:1, stop:0 rgba(178, 178, 178, 255), stop:1 rgba(153, 153, 153, 255));\n"
"    \n"
"    border-color: rgb(108, 108, 108);\n"
"}\n"
"QPushButton:pressed{\n"
"background-color: rgb(130, 130, 130);\n"
"/*background-color: qlineargradient(spread:reflect, x1:0.573682, y1:0, x2:0.574364, y2:1, stop:0 rgba(188, 188, 188, 255), stop:1 rgba(130, 130, 130, 255));*/\n"
"}\n"
"\n"
"")
        self.routeBtn.setObjectName("routeBtn")
        self.verticalLayout.addWidget(self.routeBtn)
        self.vigenereBtn = QtWidgets.QPushButton(self.centralwidget)
        self.vigenereBtn.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vigenereBtn.sizePolicy().hasHeightForWidth())
        self.vigenereBtn.setSizePolicy(sizePolicy)
        self.vigenereBtn.setMinimumSize(QtCore.QSize(75, 0))
        self.vigenereBtn.setBaseSize(QtCore.QSize(500, 100))
        self.vigenereBtn.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.vigenereBtn.setStyleSheet("QPushButton {\n"
"  qproperty-alignment: \'AlignVCenter | AlignRight\';\n"
"  border: 1px solid gray;\n"
"    background-color: qlineargradient(spread:reflect, x1:0.573682, y1:0, x2:0.574364, y2:1, stop:0 rgba(178, 178, 178, 255), stop:1 rgba(153, 153, 153, 255));\n"
"    \n"
"    border-color: rgb(108, 108, 108);\n"
"}\n"
"QPushButton:pressed{\n"
"background-color: rgb(130, 130, 130);\n"
"/*background-color: qlineargradient(spread:reflect, x1:0.573682, y1:0, x2:0.574364, y2:1, stop:0 rgba(188, 188, 188, 255), stop:1 rgba(130, 130, 130, 255));*/\n"
"}\n"
"\n"
"")
        self.vigenereBtn.setObjectName("vigenereBtn")
        self.verticalLayout.addWidget(self.vigenereBtn)
        self.scytaleBtn = QtWidgets.QPushButton(self.centralwidget)
        self.scytaleBtn.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scytaleBtn.sizePolicy().hasHeightForWidth())
        self.scytaleBtn.setSizePolicy(sizePolicy)
        self.scytaleBtn.setMinimumSize(QtCore.QSize(75, 0))
        self.scytaleBtn.setBaseSize(QtCore.QSize(500, 100))
        self.scytaleBtn.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.scytaleBtn.setStyleSheet("QPushButton {\n"
"  qproperty-alignment: \'AlignVCenter | AlignRight\';\n"
"  border: 1px solid gray;\n"
"    background-color: qlineargradient(spread:reflect, x1:0.573682, y1:0, x2:0.574364, y2:1, stop:0 rgba(178, 178, 178, 255), stop:1 rgba(153, 153, 153, 255));\n"
"    \n"
"    border-color: rgb(108, 108, 108);\n"
"}\n"
"QPushButton:pressed{\n"
"background-color: rgb(130, 130, 130);\n"
"/*background-color: qlineargradient(spread:reflect, x1:0.573682, y1:0, x2:0.574364, y2:1, stop:0 rgba(188, 188, 188, 255), stop:1 rgba(130, 130, 130, 255));*/\n"
"}\n"
"\n"
"")
        self.scytaleBtn.setObjectName("scytaleBtn")
        self.verticalLayout.addWidget(self.scytaleBtn)
        self.analysisBtn = QtWidgets.QPushButton(self.centralwidget)
        self.analysisBtn.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.analysisBtn.sizePolicy().hasHeightForWidth())
        self.analysisBtn.setSizePolicy(sizePolicy)
        self.analysisBtn.setMinimumSize(QtCore.QSize(75, 0))
        self.analysisBtn.setBaseSize(QtCore.QSize(500, 100))
        self.analysisBtn.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.analysisBtn.setStyleSheet("QPushButton {\n"
"  qproperty-alignment: \'AlignVCenter | AlignRight\';\n"
"  border: 1px solid gray;\n"
"    background-color: qlineargradient(spread:reflect, x1:0.573682, y1:0, x2:0.574364, y2:1, stop:0 rgba(178, 178, 178, 255), stop:1 rgba(153, 153, 153, 255));\n"
"    \n"
"    border-color: rgb(108, 108, 108);\n"
"}\n"
"QPushButton:pressed{\n"
"background-color: rgb(130, 130, 130);\n"
"/*background-color: qlineargradient(spread:reflect, x1:0.573682, y1:0, x2:0.574364, y2:1, stop:0 rgba(188, 188, 188, 255), stop:1 rgba(130, 130, 130, 255));*/\n"
"}\n"
"\n"
"")
        self.analysisBtn.setObjectName("analysisBtn")
        self.verticalLayout.addWidget(self.analysisBtn)
        self.breakerBtn = QtWidgets.QPushButton(self.centralwidget)
        self.breakerBtn.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.breakerBtn.sizePolicy().hasHeightForWidth())
        self.breakerBtn.setSizePolicy(sizePolicy)
        self.breakerBtn.setMinimumSize(QtCore.QSize(75, 0))
        self.breakerBtn.setBaseSize(QtCore.QSize(500, 100))
        self.breakerBtn.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.breakerBtn.setStyleSheet("QPushButton {\n"
"  qproperty-alignment: \'AlignVCenter | AlignRight\';\n"
"  border: 1px solid gray;\n"
"    background-color: qlineargradient(spread:reflect, x1:0.573682, y1:0, x2:0.574364, y2:1, stop:0 rgba(178, 178, 178, 255), stop:1 rgba(153, 153, 153, 255));\n"
"    \n"
"    border-color: rgb(108, 108, 108);\n"
"}\n"
"QPushButton:pressed{\n"
"background-color: rgb(130, 130, 130);\n"
"/*background-color: qlineargradient(spread:reflect, x1:0.573682, y1:0, x2:0.574364, y2:1, stop:0 rgba(188, 188, 188, 255), stop:1 rgba(130, 130, 130, 255));*/\n"
"}\n"
"\n"
"")
        self.breakerBtn.setObjectName("breakerBtn")
        self.verticalLayout.addWidget(self.breakerBtn)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.p1 = QtWidgets.QPushButton(self.page_2)
        self.p1.setGeometry(QtCore.QRect(350, 200, 75, 23))
        self.p1.setObjectName("p1")
        self.stackedWidget.addWidget(self.page_2)
        self.horizontalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 848, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Classical Ciphers Cryptanalysis Tool"))
        self.affineBtn.setText(_translate("MainWindow", "Affine"))
        self.adfgvxBtn.setText(_translate("MainWindow", "ADFGVX"))
        self.playfairBtn.setText(_translate("MainWindow", "Playfair"))
        self.rot13Btn.setText(_translate("MainWindow", "ROT13"))
        self.railfenceBtn.setText(_translate("MainWindow", "Railfence"))
        self.routeBtn.setText(_translate("MainWindow", "Route"))
        self.vigenereBtn.setText(_translate("MainWindow", "Vigenere"))
        self.scytaleBtn.setText(_translate("MainWindow", "Scytale"))
        self.analysisBtn.setText(_translate("MainWindow", "Analysis"))
        self.breakerBtn.setText(_translate("MainWindow", "Breaker"))
        self.p1.setText(_translate("MainWindow", "goto p1"))
        self.menuFile.setTitle(_translate("MainWindow", "About"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
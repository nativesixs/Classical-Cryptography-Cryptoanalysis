from collections import Counter
from string import ascii_uppercase
from datetime import datetime
from utils import Validate

class AffineCipher:
    def __init__(self):
        self.previous = []

    def affineFreq(self, ciph):
        lst = []
        alphabet = ascii_uppercase

        cipherCounter = Counter(ciph).most_common()
        alphabetCounter = Counter(alphabet).most_common()

        frequencyAlphabet = [0] * 26
        for i in range(26):
            for j in range(len(cipherCounter)):
                if cipherCounter[j][0] in alphabetCounter[i][0]:
                    frequencyAlphabet[i] = cipherCounter[j][1]
        lst.append(frequencyAlphabet)
        frequencyAlphabet = lst
        return frequencyAlphabet

    def decryptAffine(self, text, key, b):
        def modInverse(a, m):
            a = a % m
            for x in range(1, m):
                if (a * x) % m == 1:
                    return x
            return 1

        a = key
        m = 26
        chars = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        dectext = ""
        decres = []
        modin = modInverse(a, m)
        char = text
        for i in range(len(char)):
            if char[i] == " " or char[i].isnumeric():
                decres.append(char[i])
            else:
                dechar = chars.index(char[i])
                vz = (modin * (dechar - b) % m)
                decres.append(chars[vz])
            dectext = ''.join(decres)
        return dectext

    def mainAffine(self, ui):
        ui.basicFrame.show()
        ui.affineFrame.show()
        ui.radioBrute.show()
        ui.radioFrq.show()
        ui.radioBrute.setChecked(True)

        def breaking():
            if ui.radioBrute.isChecked():
                start_time = datetime.now()
                ui.status.setText("Ready")
                encrypted = ui.makec()
                self.previous = []
                coprimes = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
                for i in range(len(coprimes)):
                    for j in range(1, 26):
                        ui.status.setText("Working..")
                        self.previous.append(self.decryptAffine(encrypted, coprimes[i], j))
                        self.previous.append("Key a: " + str(coprimes[i]) + ", Key b: " + str(j))
                        ui.plainTextLine.setText('\n'.join(self.previous))
                ui.status.setText("Done")
                ui.timer.setText('{}'.format(datetime.now() - start_time))
                ui.findLikely(self.previous)
            if ui.radioFrq.isChecked():
                ui.vigFirstFrame.show()
                ui.guessedKey.hide()
                ui.labelHodnotaB_12.hide()
                ui.ngramsLabel.hide()
                ui.accuracyBox.hide()

                def plotting():
                    ciph = Validate().analysisCleantext(ui.cipherText.text())
                    ui.plotControlFrame.show()
                    ui.labelHodnotaB_10.hide()
                    ui.shiftletter.hide()
                    ui.labelHodnotaB_8.setText("Key A:")
                    ui.labelHodnotaB_9.setText("Key B:")
                    ui.okBtn.hide()
                    ui.labelHodnotaB_11.hide()
                    ui.keyLetters.hide()
                    ui.plotBox.setRange(1, 25)
                    frequencies = self.affineFreq(ciph)
                    key = 1
                    ui.plots(key, frequencies, ciph)
                ui.continueBtn.clicked.connect(plotting)

        def findagain():
            ui.findLikely(self.previous)

        ui.accuracyBox.valueChanged.connect(findagain)
        ui.decryptBtn.clicked.connect(breaking)
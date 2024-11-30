from datetime import datetime
from pycipher import Playfair
from utils import Validate

class PlayfairCipher:
    def mainPlayfair(self, ui):
        ui.basicFrame.show()
        ui.affineFrame.show()
        ui.radioDict.show()
        ui.radioHill.hide()
        ui.status.setText("Ready")
        ui.radioDict.setChecked(True)
        ui.decryptBtn.clicked.connect(lambda: self.Playfair(ui))
        ui.accuracyBox.valueChanged.connect(lambda: self.likelyPlayfair(ui))

    def Playfair(self, ui):
        ui.status.setText("Working..")
        start_time = datetime.now()
        if ui.radioDict.isChecked():
            ui.status.setText("Ready")
            ciph = Validate().analysisCleantext(ui.cipherText.text())
            if ui.languagePick.currentText() == 'Look for English words':
                keyword = open("src/eng1000words.txt", "r").read().splitlines()
            if ui.languagePick.currentText() == 'Look for Czech words':
                keyword = open("src/czech1000words.txt", "r").read().splitlines()
            alphabet = list('ABCDEFGHIKLMNOPQRSTUVWXYZ')
            global playfairRes
            global playfairKey
            playfairRes = []
            playfairKey = []
            res = []
            for k in range(len(keyword)):
                ui.status.setText("Working..")
                keyphrase = []
                for i in range(len(keyword[k])):
                    if keyword[k][i] == 'j' or keyword[k][i] == 'J':
                        keyword[k] = keyword[k].replace('j', 'I')
                    if keyword[k][i].upper() not in keyphrase:
                        keyphrase.append(keyword[k][i].upper())
                for i in range(len(alphabet)):
                    if alphabet[i] not in keyphrase:
                        keyphrase.append(alphabet[i])
                key = ''.join(keyphrase)
                dec = Playfair(key=key).decipher(ciph)
                ui.status.setText("Done")
                playfairRes.append(dec)
                playfairKey.append('Key: ' + key)
                res.append(dec)
                res.append('Key: ' + key)
            ui.status.setText("Done")
            ui.timer.setText('{}'.format(datetime.now() - start_time))
            ui.plainTextLine.setText('\n\n'.join(res))

    def likelyPlayfair(self, ui):
        global playfairRes
        global playfairKey
        keys = playfairKey
        text = playfairRes
        possible = []
        if ui.languagePick.currentText() == 'Look for English words':
            lines = open("src/eng1000words.txt", "r").read().splitlines()
        if ui.languagePick.currentText() == 'Look for Czech words':
            lines = open("src/czech1000words.txt", "r").read().splitlines()
        for j in range(len(text)):
            for i in range(len(lines)):
                if lines[i].upper() in text[j] and len(lines[i]) >= ui.accuracyBox.value():
                    possible.append(text[j])
                    possible.append(keys[j] + '\n')
                    break
        ui.plainTextLikely.setText('\n\n'.join(possible))
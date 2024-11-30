from datetime import datetime
import math
from matplotlib import pyplot as plt
import numpy as np
from collections import Counter
from string import ascii_uppercase
from utils import Validate

class VigenereCipher:
    def vigenereFindKey(self, key, text):
        rows = int(math.ceil(len(text) / key))
        matrix = np.empty((rows, key), dtype="U")
        matrix.reshape(-1)[:len(text)] = list(text)
        lst = []
        for i in range(key):
            arr = []
            for j in range(rows):
                arr.append(matrix[j][i])
            ciph = ''.join(arr)
            alphabet = ascii_uppercase
            cipherCounter = Counter(ciph).most_common()
            alphabetCounter = Counter(alphabet).most_common()
            frequencyAlphabet = []
            for i in range(26):
                frequencyAlphabet.append(0)
            for i in range(26):
                for j in range(len(cipherCounter)):
                    if cipherCounter[j][0] in alphabetCounter[i][0]:
                        frequencyAlphabet[i] = cipherCounter[j][1]
            lst.append(frequencyAlphabet)
        frequencyAlphabet = lst
        return frequencyAlphabet

    def plots(self, key, frequencyAlphabet, ciph, ui):
        alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        defaultAlphabet = [8.12, 1.49, 2.71, 4.32, 12.02, 2.30, 2.03, 5.92, 7.31, 0.10, 0.69, 3.98, 2.61, 6.95, 7.68, 1.82, 0.11, 6.02, 6.28, 9.10, 2.88, 1.11, 2.09, 0.17, 2.11, 0.07]
        czechfrequency = [6.21, 1.55, 1.60, 3.60, 7.69, 0.27, 0.27, 1.27, 4.35, 2.11, 3.73, 3.84, 3.22, 6.53, 8.66, 3.41, 0.001, 3.69, 4.51, 5.72, 3.14, 4.66, 0.008, 0.07, 1.90, 2.19]

        def shiftPlot1(event):
            if ui.vigenereradio.isChecked():
                p.set_ydata(frequencyAlphabet[ui.plotBox.value() - 1])
                ui.shiftletter.setText(alphabet[abs(ui.shiftBox.value())])
                plt.draw()
                dispIndex = ui.plotBox.value()
                ui.currentplotnumber.setText(str(dispIndex))
            if ui.affineradio.isChecked():
                global keyA
                global keyB
                keyA = ui.plotBox.value()
                keyB = ui.shiftBox.value()
                self.decryptAffine(ciph, keyA, keyB)
        ui.plotBox.valueChanged.connect(shiftPlot1)

        def shiftPlot2(event):
            if ui.vigenereradio.isChecked():
                p.set_ydata(frequencyAlphabet[ui.plotBox.value() - 1])
                ui.shiftletter.setText(alphabet[abs(ui.shiftBox.value())])
                plt.draw()
                dispIndex = ui.plotBox.value()
                ui.currentplotnumber.setText(str(dispIndex))
            if ui.affineradio.isChecked():
                global keyA
                global keyB
                keyA = ui.plotBox.value()
                keyB = ui.shiftBox.value()
                self.decryptAffine(ciph, keyA, keyB)
        ui.plotBox.valueChanged.connect(shiftPlot2)

        x = alphabet
        z = defaultAlphabet

        fig, (ax, defalpha, cze) = plt.subplots(nrows=3, sharey=False, figsize=(8, 8))
        plt.subplots_adjust(hspace=0.7)
        p, = defalpha.plot(x, z, 'go--')
        p, = cze.plot(alphabet, czechfrequency, 'bo--')
        p, = ax.plot(x, frequencyAlphabet[ui.plotBox.value() - 1], 'ro--')
        defalpha.set(xlabel="Chars", ylabel="Frequency", title="English char frequency")
        cze.set(xlabel="Chars", ylabel="Frequency", title="Czech char frequency")
        ax.set(xlabel="Chars", ylabel="Frequency", title="Ciphertext frequency")

        def shift1(event):
            y = np.roll(frequencyAlphabet[ui.plotBox.value() - 1], ui.shiftBox.value())
            ui.shiftletter.setText(alphabet[abs(ui.shiftBox.value())])
            p.set_ydata(y)
            plt.draw()
            if ui.affineradio.isChecked():
                global keyA
                global keyB
                keyA = ui.plotBox.value()
                keyB = ui.shiftBox.value()
                self.decryptAffine(ciph, keyA, keyB)
        ui.shiftBox.valueChanged.connect(shift1)

        def shift2(event):
            y = np.roll(frequencyAlphabet[ui.plotBox.value() - 1], -ui.shiftBox.value())
            ui.shiftletter.setText(alphabet[ui.shiftBox.value()])
            p.set_ydata(y)
            plt.draw()
            if ui.affineradio.isChecked():
                global keyA
                global keyB
                keyA = ui.plotBox.value()
                keyB = ui.shiftBox.value()
                self.decryptAffine(ciph, keyA, keyB)
        ui.shiftBox.valueChanged.connect(shift2)

        def okFce(event):
            if ui.vigenereradio.isChecked():
                keyL = ui.keyLetters.text() + ui.shiftletter.text()
                ui.keyLetters.setText(keyL)
                oldval = ui.plotBox.value()
                ui.plotBox.setValue(oldval + 1)
            if ui.affineradio.isChecked():
                keyL = ui.shiftBox.value()
                ui.keyLetters.setText(str(keyL))
        ui.okBtn.clicked.connect(okFce)

        def callvgn(event):
            if ui.vigenereradio.isChecked():
                self.vigenere(ciph, ui)
            if ui.affineradio.isChecked():
                if ui.plotBox.value() == 1:
                    keyA = ui.keyLetters.text()
                    keyA = int(keyA)
                if ui.plotBox.value() == 2:
                    keyB = ui.keyLetters.text()
                    keyB = int(keyB)
                if keyA and keyB:
                    self.decryptAffine(ciph, keyA, keyB)
        ui.keyLetters.textChanged.connect(callvgn)

        def hideC(event):
            plt.close()
            ui.plotControlFrame.hide()

        ui.guessedKey.valueChanged.connect(hideC)
        plt.ion()
        plt.show()

    def keyLength(self, ciph, ui):
        '''
        source:http://www.robindavid.fr/blog/2012/06/15/kasiski-babbage-cryptanalysis-in-python/
        '''
        l = ciph
        res = {}
        freq = []
        count = 0
        i = 0

        def getDivisors(n):
            l = []
            for i in range(2, n):
                if n % i == 0:
                    l.append(i)
            return l
        lst = []
        while i < len(l):  # Loop through all the list
            elt = l[i:i + 3]  # Take at least 3-character length for tuples
            long = len(elt)
            if long == 3:  # should be 3 if not means we are at the end of the list
                for j in range(i + 1, len(l)):  # Find further in the list for the same pattern
                    if l[i:i + long] == l[j:j + long]:  # If match the 3-char check for more
                        while l[i:i + long] == l[j:j + long]:
                            long = long + 1
                        long = long - 1
                        elt = l[i:i + long]  # Now we have a tuple
                        diff = j - i  # Compute the distance
                        freq.extend(getDivisors(diff))  # Add the divisors to the list
                        divisors = getDivisors(diff)
                        # print ("%s\ti:%s\tj:%s\tdiff:%s\t\tDivisors:%s" % (elt,i,j, diff,getDivisors(diff))) #Print information about the tuple (can be deleted)
                        a = [elt, i, j, diff, divisors]  # Print information about the tuple (can be deleted)
                        lst.append(a)
                        count = count + 1
                        j = j + long + 1
                i = i + long - 3 + 1
            else:
                i = i + 1

        ngraphs = []
        for i in range(len(lst)):
            x = [lst[i][0], lst[i][3], lst[i][4]]
            ngraphs.append(x)
        comnum = []
        for i in range(len(ngraphs)):
            for j in range(len(ngraphs[i][2][:])):
                comnum.append(ngraphs[i][2][j])
        counterlet = Counter(comnum).most_common(20)
        popnums = []
        for i in range(len(counterlet)):
            if counterlet[i][0] <= 25:
                popnums.append(counterlet[i])
        text = []
        for i in range(len(popnums)):
            text.append("Key length: " + str(popnums[i][0]) + "\n")
            text.append("rep.index: " + str(popnums[i][1]) + "\n \n")
        ui.plainTextLikely.setText(''.join(text))

    def vigenere(self, ciph, ui):
        text = Validate().analysisCleantext(ciph)
        keylen = int(ui.guessedKey.value())
        key = ui.keyLetters.text()

        if len(key) < keylen:
            while len(key) < keylen:
                key = key + "X"

        result = []
        keyInt = [ord(i) for i in key]
        textInt = [ord(i) for i in text]

        for i in range(len(text)):
            shift = ((textInt[i] - keyInt[i % len(key)]) % 26)
            if text[i].isalpha():
                result.append(chr(shift + 65))
            else:
                result.append(text[i])
        decryptedText = ''.join(result)
        return ui.plainTextLine.setText(decryptedText)

    def mainVigenere(self, ui):
        ui.basicFrame.show()

        def breaking():
            ciph = ui.cipherText.text()
            ciph = ''.join([*filter(str.isalpha, ciph)]).upper()
            ui.vigFirstFrame.show()
            self.keyLength(ciph, ui)

        def plotting():
            ciph = ui.cipherText.text()
            ciph = ''.join([*filter(str.isalpha, ciph)]).upper()
            ui.plotControlFrame.show()
            key = int(ui.guessedKey.value())
            frequencies = self.vigenereFindKey(key, ciph)
            self.plots(key, frequencies, ciph, ui)

        ui.continueBtn.clicked.connect(plotting)
        ui.decryptBtn.clicked.connect(breaking)
from datetime import datetime
import numpy as np
import math
from utils import Validate

class ScytaleCipher:
    def decryptScytale(self, text, key):
        row = int(math.ceil(len(text) / key))
        col = key  
        matrix = np.empty((col, row), dtype="U")
        matrix.reshape(-1)[:len(text)] = list(text)
        result = []
        for i in range(row):
            for j in range(col):
                result.append(matrix[j][i])
        if len(text) < (col * key):
            for i in range((col * key) - len(text)):
                if result[-1] == "X":
                    result.remove(result[-1])
        decrypted = ''.join(result)
        return decrypted

    def mainScytale(self, ui):
        ui.basicFrame.show()
        ui.affineFrame.show()
        ui.accuracyBox.setValue(int(3))
        ui.ngramsLabel.setText("Amount of tested keys:")
        
        def breaking():
            encrypted = ui.makec()
            previous = []
            for i in range(1, 26):
                start_time = datetime.now()
                ui.status.setText("Working..")
                previous.append(self.decryptScytale(encrypted, i))
                previous.append("Key: " + str(i))
            ui.plainTextLine.setText('\n'.join(previous))
            ui.findLikely(previous)
            ui.status.setText("Done")
            ui.timer.setText('{}'.format(datetime.now() - start_time))
        
        ui.decryptBtn.clicked.connect(breaking)
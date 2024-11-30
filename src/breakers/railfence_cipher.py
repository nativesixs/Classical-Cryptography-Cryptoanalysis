from datetime import datetime
import numpy as np
from utils import Validate

class RailfenceCipher:
    def mainRailfence(self, ui):
        ui.status.setText("Ready")
        ui.basicFrame.show()
        ui.affineFrame.show()
        
        def breaking():
            start_time = datetime.now()
            encrypted = ui.makec()
            global previous
            previous = []
            for i in range(2, len(encrypted)):
                ui.status.setText("Working..")
                previous.append(self.decryptRailfence(encrypted, i))
                previous.append("Key: " + str(i))
            ui.plainTextLine.setText('\n'.join(previous))
            ui.findLikely(previous)
            ui.status.setText("Done")
            ui.timer.setText('{}'.format(datetime.now() - start_time))
        
        def findagain():
            global previous
            ui.findLikely(previous)
        
        ui.accuracyBox.valueChanged.connect(findagain)
        ui.decryptBtn.clicked.connect(breaking)
    
    def decryptRailfence(self, text, key):
        parsedText = [char for char in text]
        matrix = np.empty((key, len(text)), dtype="U")
        result = [] 
        for i in range(key):
            column = 0
            down = True
            for row in range(len(text)):
                if down == False:
                    if column - 1 >= 0:
                        if column == i:
                            matrix[column][row] = parsedText[0]
                            parsedText.pop(0)
                        elif not [*filter(str.isalnum, matrix[column][row])]:
                            matrix[column][row] = "*"
                        column = column - 1
                    else:
                        down = True 
                if down == True:   
                    if column <= key - 1:
                        if column == i:
                            matrix[column][row] = parsedText[0]
                            parsedText.pop(0)
                        elif not [*filter(str.isalnum, matrix[column][row])]:
                            matrix[column][row] = "*"
                        column = column + 1
                if column == key:
                    column = column - 2
                    down = False
        for row in range(len(text)):
            for column in range(key):
                if [*filter(str.isalnum, matrix[column][row])]:
                    result.append(matrix[column][row])
        decrypted = "".join(result)
        return decrypted
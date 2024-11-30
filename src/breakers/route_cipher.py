from datetime import datetime
import numpy as np
from utils import Validate

class RouteCipher:
    def factors(self, lenCiph):
        factors = []
        for i in range(1, lenCiph + 1):
            if lenCiph % i == 0:
                factors.append(i)
        return factors
    
    def decryptRoute(self, ui):
        start_time = datetime.now()
        ui.status.setText("Working..")
        ciph = ui.makec()
        factor = self.factors(len(ciph))
        posrow = []
        poscol = []
        for i in range(int(len(factor) / 2)):
            posrow.append(factor[i])
        for i in range(int(len(factor) / 2)):
            factor.sort(reverse=True)
            poscol.append(factor[i])
        for i in range(int(len(factor) / 2)):
            factor.sort(reverse=False)
            poscol.append(factor[i])
        for i in range(int(len(factor) / 2)):
            factor.sort(reverse=True)
            posrow.append(factor[i])
        
        posResult = []
        posKey = []
        posMethod = []
        
        for i in range(len(posrow)):
            rows = posrow[i]
            columns = poscol[i]
            matrix = np.empty((rows, columns), dtype="U")
            parsedText = [char for char in ciph]
            for j in range(rows):
                for k in range(columns):
                    if len(parsedText) > 0:
                        matrix[j][k] = parsedText[0]
                        parsedText.pop(0)
                    else:
                        matrix[j][k] = ""
            matrix = np.flip(matrix)
            matrix = matrix.transpose()
            decryptedText = ""
            for k in range(columns):  # Corrected to iterate over columns
                line = "".join(string for string in matrix[k] if len(string) > 0)
                decryptedText = decryptedText + line
            posResult.append(decryptedText)
            posKey.append("Key: " + str(posrow[i]))
            posMethod.append("Route: Spiral \n")
        
        ui.plainTextLine.setText('\n'.join(posResult))
        ui.findLikely(posResult)
        ui.timer.setText('{}'.format(datetime.now() - start_time))
        ui.status.setText("Done")
    
    def mainRoute(self, ui):
        ui.basicFrame.show()
        ui.affineFrame.show()
        ui.status.setText("Ready")
        ui.accuracyBox.valueChanged.connect(lambda: self.decryptRoute(ui))
        ui.decryptBtn.clicked.connect(lambda: self.decryptRoute(ui))
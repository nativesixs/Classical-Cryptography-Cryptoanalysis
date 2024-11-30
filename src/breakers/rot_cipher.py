from datetime import datetime
import numpy as np
from utils import Validate

class RotCipher:
    def mainRot(self, ui):
        ui.basicFrame.show()
        ui.affineFrame.show()
        ui.ngramsLabel.hide()
        ui.accuracyBox.hide()
        ui.status.setText("Ready")
        
        def breaking():
            start_time = datetime.now()
            ui.status.setText("Working..")
            ciph = Validate().analysisCleantext(ui.cipherText.text())
            decrypted = []
            result = []
            for j in range(26):
                chars = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
                rotval = j
                newalpha = np.roll(chars, rotval)
                index = []
                for i in range(len(ciph)):
                    index.append(chars.index(ciph[i]))
                decrypted = []
                for i in range(len(ciph)):
                    decrypted.append(newalpha[index[i]])
                x = ''.join(decrypted)
                result.append(x)
                result.append("Key: " + str(j))
            ui.status.setText("Done")
            ui.timer.setText('{}'.format(datetime.now() - start_time))
            ui.plainTextLine.setText('\n'.join(result))
        
        ui.decryptBtn.clicked.connect(breaking)
#from Dialogo import Dialogo
#import sys
import threading
import time
#from typing import Container
#from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QThread, pyqtSignal
from CargaArchivos import CargandoArchivos
from os import close, environ


class CargaArchivosAplicacion(QDialog):
    def __init__(self):
        super().__init__()

        self.setModal(True)

        self.ui = CargandoArchivos()
        self.contador = 0
        self.ui.setupUi(self)

        self.processClass = ProcesoCargaArchivo()
        self.processClass.update_progress_bar.connect(self.update_progressBar)
        self.processClass.start()

        self.show()

    def update_progressBar(self, val):
        if val <= 100:
            self.ui.pbr_cargando_archivo.setValue(val)
            self.contador = val
        else:
            self.cerrar_aplicacion()

    def cerrar_aplicacion(self):
        self.processClass.terminate()
        self.close()

class ProcesoCargaArchivo(QThread):

    update_progress_bar = pyqtSignal(int)

    def run(self):
        self.setTerminationEnabled(True)
        self.contador = 0
        while self.contador <= 100:
            time.sleep(0.1)
            self.update_progress_bar.emit(self.contador)
            self.contador += 10
        self.update_progress_bar.emit(self.contador)
            

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


def correr_programa():
    #suppress_qt_warnings() #para evitar los errores
    #app = QApplication(sys.argv)
    dialogo = CargaArchivosAplicacion()
    t = ProcesoCargaArchivo(dialogo)
    t.start()        
    dialogo.exec()
    #sys.exit(app.exec_())
    #t.join()

if __name__ == '__main__':
    correr_programa()    
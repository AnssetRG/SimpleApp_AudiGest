import sys
import threading
import time
from PyQt5.QtWidgets import QApplication, QDialog
from CargaArchivos import CargandoArchivos
from os import environ


class CargaArchivosAplicacion(QDialog):
    def __init__(self):
        super().__init__()

        self.ui = CargandoArchivos()
        self.ui.setupUi(self)

        self.show()


class ProcesoCargaArchivo(threading.Thread):
    contador = 0
    def __init__(self, dialogo):
        threading.Thread.__init__(self)
        self.dialogo = dialogo
        self.contador = 0

    def run(self):
        while self.contador <=100:
            time.sleep(0.25)          
            self.dialogo.ui.pbr_cargando_archivo.setValue(self.contador)
            self.contador += 10

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


def correr_programa():
    suppress_qt_warnings() #para evitar los errores
    #app = QApplication(sys.argv)
    dialogo = CargaArchivosAplicacion()
    t = ProcesoCargaArchivo(dialogo)
    t.start()        
    dialogo.exec()
    #sys.exit(app.exec_())
    #t.join()

if __name__ == '__main__':
    correr_programa()    
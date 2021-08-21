import sys
import threading
import time
from PyQt5.QtWidgets import QApplication, QDialog
from CargaArchivos import CargandoArchivos


class CargaArchivosAplicacion(QDialog):
    def __init__(self):
        super().__init__()

        self.ui = CargandoArchivos()
        self.ui.setupUi(self)

        self.show()


class ProcesoCargaArchivo(threading.Thread):
    
    def __init__(self, dialogo):
        threading.Thread.__init__(self)
        self.dialogo = dialogo
        self.contador = 0

    def run(self):
        while self.contador <=100:
            time.sleep(0.25)
            self.dialogo.ui.pbr_descarg_archivo.setValue(self.contador)
            self.contador += 10


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialogo = CargaArchivosAplicacion()
    t = ProcesoCargaArchivo(dialogo)
    t.start()        
    #dialogo.exec()
    sys.exit(app.exec_()) 

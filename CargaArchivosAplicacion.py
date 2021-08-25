import sys
import threading
import time
from PyQt5.QtWidgets import QApplication, QDialog
from CargaArchivos import CargandoArchivos
from os import environ


class CargaArchivosAplicacion(QDialog):
    def __init__(self): #constructor
        super().__init__() #se invoca el constructor de la clase padre por medio de la función super  

        self.ui = CargandoArchivos() #creación de objeto de la interfaz gráfica en la clase CargandoArchivos()
        self.ui.setupUi(self) #desde allí usamos el método setupUi 

        self.show() #mostrar


#Thread que realizar el trabajo de la barra de progreso en segundo plano
class ProcesoCargaArchivo(threading.Thread): 
    #contador = 0

    def __init__(self, dialogo): #constructor
        threading.Thread.__init__(self) 
        self.dialogo = dialogo #variable de instancia de la clase proceso CargaArchivo
        self.contador = 0

    def run(self): #método por defecto de la super clase thread que se está heredando
        while self.contador <=100: #barrita cargando...
            time.sleep(0.25)
            self.dialogo.ui.pbr_cargando_archivo.setValue(self.contador)
            self.contador += 10
        

def suppress_qt_warnings(): #para evitar mensajes de error
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

def correr_programa():
    suppress_qt_warnings() #para evitar los errores

    app = QApplication(sys.argv)
    dialogo = CargaArchivosAplicacion()
    t = ProcesoCargaArchivo(dialogo)
    t.start()        
    dialogo.exec()
    sys.exit(app.exec_()) 

if __name__ == '__main__':
    suppress_qt_warnings()

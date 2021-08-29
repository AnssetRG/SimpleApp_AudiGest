import sys
import librosa
import os
from os import environ
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor, QPixmap
from PyQt5.QtWidgets import QApplication, QBoxLayout, QDialog, QMainWindow,QLabel, QPushButton, QWidget, QGridLayout, QMessageBox, QFileDialog,QVBoxLayout,QHBoxLayout,QGraphicsPixmapItem, QGraphicsScene
from Dialogo import Dialogo
from CargaArchivos import CargandoArchivos
from CargaArchivosAplicacion import ProcesoCargaArchivo, CargaArchivosAplicacion, correr_programa

parameters = {
    "audio": [],
    "model": [],
    "result": []
}

widgets = {
    "audio_file": []
}

class AudiGest_terminado(QDialog,QMainWindow):
    def __init__(self):        
        super().__init__()
        self.ui = Dialogo()
        self.ui.setupUi(self)
        self.imagenes()
        #self.activar_boton_procesar()        

        widgets["audio_file"].append(self.ui.caja_texto1)

        self.ui.btn_cargar.clicked.connect(self.set_new_file)
        self.ui.btn_procesar.clicked.connect(correr_programa)
        

    def imagenes(self):        
        self.scene = QGraphicsScene(self)
        self.scene2 = QGraphicsScene(self)
        self.scene3 = QGraphicsScene(self)
        pixmap = QPixmap()
        pixmap2 = QPixmap()
        pixmap3 = QPixmap()
        pixmap.load('imagenes\cara1.png')
        pixmap2.load('imagenes\cara2.png')
        pixmap3.load('imagenes\cara3.png')
        item = QGraphicsPixmapItem(pixmap)
        item2 = QGraphicsPixmapItem(pixmap2)
        item3 = QGraphicsPixmapItem(pixmap3)
        self.scene.addItem(item)
        self.scene2.addItem(item2)
        self.scene3.addItem(item3)
        self.ui.gpc_imagen1.setScene(self.scene)
        self.ui.gpc_imagen2.setScene(self.scene2)
        self.ui.gpc_imagen3.setScene(self.scene3)

        self.show()
        
    def closeEvent(self, event):        
        reply = QMessageBox.question(self, 'Confirmar Cerrar Ventana', '¿Está seguro que quiere salir de la aplicación?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 

    def set_new_file(self):
        fname = QFileDialog.getOpenFileName(None,'Abrir Archivo', '','Audio (*.wav *.WAV)')
        temp_split = fname[0].split('/')

        resultado = ""

        if temp_split[len(temp_split) - 1] == "":
            if parameters["audio"][-1] == "":
                resultado = "Nombre del Archivo de Audio"
            else:
                resultado = parameters["audio"][-1]
        else:
            y, sr = librosa.load(fname[0])
            audio_length = librosa.get_duration(y=y, sr=sr)
            if audio_length < 6:
                resultado = temp_split[len(temp_split) - 1]
            else:
                self.alert_window()
                resultado = parameters["audio"][-1] 
        parameters["audio"].append(resultado)
        #print(parameters['audio'])
        #print(widgets['audio_file']) 
        widgets["audio_file"][-1].setText(parameters["audio"][-1])
  

    def alert_window(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText('La duración del audio es mayor a la esperada.')
        msg.setWindowTitle("Error de Carga de Audio")
        msg.exec_()
    
    def activar_boton_procesar(self):
        
        if self.ui.radio_btn1.isChecked() == True or self.ui.radio_btn2.isChecked() == True or self.ui.radio_btn3.isChecked() == True:
            self.ui.btn_procesar.setEnabled(True)
        else: 
            self.ui.btn_procesar.setEnabled(False)
    

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

def main():
    suppress_qt_warnings()    
    app = QApplication(sys.argv)
    ventana = AudiGest_terminado()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
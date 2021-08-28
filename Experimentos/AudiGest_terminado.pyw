import sys
import librosa
import os
from os import environ
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow,QLabel, QPushButton, QWidget, QGridLayout, QMessageBox, QFileDialog,QVBoxLayout,QHBoxLayout,QGraphicsPixmapItem, QGraphicsScene
from Dialogo import Dialogo

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

    def imagenes(self):
        #sección imagenes
        self.scene = QGraphicsScene(self)
        self.scene2 = QGraphicsScene(self)
        self.scene3 = QGraphicsScene(self)
        pixmap = QPixmap()
        pixmap2 = QPixmap()
        pixmap3 = QPixmap()
        pixmap.load('cara1.png')
        pixmap2.load('cara2.png')
        pixmap3.load('cara3.png')
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






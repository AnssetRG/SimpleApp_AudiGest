import sys
import librosa
import os
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow,QLabel, QPushButton, QWidget, QGridLayout, QMessageBox, QFileDialog,QVBoxLayout,QHBoxLayout,QGraphicsPixmapItem, QGraphicsScene
from Dialogo import Dialogo
from os import environ

parameters = {
    "audio": [],
    "model": [],
    "result": []
}

widgets = {
    "audio_file": []
}

class AudiGest_terminado(QDialog):
    def __init__(self):        
        super().__init__()
        self.ui = AudiGest_terminado()
        self.ui.setupUi(self)


        #sección imagenes
        self.scene = QGraphicsScene(self)
        pixmap = QPixmap()
        pixmap.load('cara1.png')
        item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)
        self.ui.gpc_imagen1.setScene(self.scene)

        self.show()

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


if __name__ == '__main__':
    suppress_qt_warnings()
    app = QApplication(sys.argv)
    ventana = AudiGest_terminado()
    ventana.show()
    sys.exit(app.exec_())






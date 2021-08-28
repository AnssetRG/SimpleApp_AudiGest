from CargaArchivos import CargandoArchivos
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow,QLabel, QPushButton, QWidget, QGridLayout, QMessageBox, QFileDialog,QVBoxLayout,QHBoxLayout
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
import sys
import librosa
import os
from CargaArchivosAplicacion import ProcesoCargaArchivo, CargaArchivosAplicacion, correr_programa

parameters = {
    "audio": [],
    "model": [],
    "result": []
}

widgets = {
    "audio_file": []
}

class AudioGrid(QVBoxLayout):
    def __init__(self):
        super().__init__()
        parameters["audio"].append("")

        title = QHBoxLayout()
        section = QHBoxLayout()

        #texto 1
        audio_label = QLabel("1. Seleccione el Audio")
        audio_label.setAlignment(QtCore.Qt.AlignCenter)
        audio_label.setStyleSheet(
            "*{font-size: 32px;"+
            "color: 'black';"+
            "padding: 15px 0}"
        )

        #botón cargar
        audio_btn = QPushButton("Cargar")
        audio_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        audio_btn.setFixedWidth(250)
        audio_btn.setStyleSheet(
            "*{margin-right: 20px; "+
            "border: 4px solid 'black';"+
            "border-radius: 10px;" +
            "font-size: 24px;"+
            "color: 'black';"+
            "padding: 15px 0}" +
            "*:hover{background: 'gray';}"
        )

        #texto 2
        audio_file_label = QLabel("Nombre del Archivo de Audio")
        audio_file_label.setAlignment(QtCore.Qt.AlignLeft)
        audio_file_label.setStyleSheet(
            "*{margin-left: 20px; "+
            "border: 2px solid 'black';"+
            "border-radius: 5px;" +
            "font-size: 24px;"
            "padding: 15px 0;"+
            "background: 'white'}"
        )

        #boton procesar
        procesar_btn = QPushButton("Procesar")
        procesar_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        procesar_btn.setFixedWidth(250)
        procesar_btn.setStyleSheet(
            "*{margin-right: 20px; "+
            "border: 4px solid 'black';"+
            "border-radius: 10px;" +
            "font-size: 24px;"+
            "color: 'black';"+
            "padding: 15px 0}" +
            "*:hover{background: 'gray';}"
        )

        widgets["audio_file"].append(audio_file_label)

        audio_btn.clicked.connect(self.set_new_file)
        procesar_btn.clicked.connect(correr_programa)

        title.addWidget(audio_label)
        section.addWidget(audio_btn)
        section.addWidget(procesar_btn)
        section.addWidget(audio_file_label)

        self.addLayout(title)
        self.addLayout(section)
    
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
        widgets["audio_file"][-1].setText(parameters["audio"][-1])        

    
    def alert_window(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText('La duración del audio es mayor a la esperada.')
        msg.setWindowTitle("Error de Carga de Audio")
        msg.exec_()


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.set_mainWindow()
        self.set_AudioLayout()

        self.centralwidget.setLayout(self.layout)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Confirmar Cerrar Ventana', '¿Está seguro que quiere salir de la aplicación?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
    def set_mainWindow(self):
        self.setWindowTitle("AudiGest v0.0")
        self.setFixedWidth(1000)

        self.centralwidget = QWidget()
        self.layout = QVBoxLayout()
        self.setCentralWidget(self.centralwidget)

    def set_AudioLayout(self):
        self.audioGrid = AudioGrid()
        self.layout.addLayout(self.audioGrid)

    def set_ModelSelection(self):
        self.modelGrid = AudioGrid()
        self.centralwidget.setLayout(self.modelGrid)

def suppress_qt_warnings(): #para evitar mensajes de error
    os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"

def main():
    suppress_qt_warnings()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
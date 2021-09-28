from os import close
import time
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
#from CargaArchivos import CargandoArchivos


class LoadWidget(object):
    def setupUi(self, CargandoArchivos):
        CargandoArchivos.setObjectName("CargandoArchivos")
        CargandoArchivos.resize(401, 193)

        # texto
        self.lbl_cargandoarchivo = QtWidgets.QLabel(CargandoArchivos)
        self.lbl_cargandoarchivo.setGeometry(QtCore.QRect(100, 40, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lbl_cargandoarchivo.setFont(font)
        self.lbl_cargandoarchivo.setObjectName("lbl_cargandoarchivo")

        #barra de carga
        self.pbr_cargando_archivo = QtWidgets.QProgressBar(CargandoArchivos)
        self.pbr_cargando_archivo.setGeometry(QtCore.QRect(50, 110, 311, 31))
        self.pbr_cargando_archivo.setProperty("value", 0)
        self.pbr_cargando_archivo.setObjectName("pbr_cargando_archivo")

        self.retranslateUi(CargandoArchivos)
        QtCore.QMetaObject.connectSlotsByName(CargandoArchivos)

    def retranslateUi(self, CargandoArchivos):
        _translate = QtCore.QCoreApplication.translate
        CargandoArchivos.setWindowTitle(_translate("CargandoArchivos", "Carga Archivos"))
        self.lbl_cargandoarchivo.setText(_translate("CargandoArchivos", "Cargando archivos..."))


class LoadWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setModal(True)

        self.ui = LoadWidget()
        self.contador = 0
        self.ui.setupUi(self)

        self.processClass = ProcesoCarga()
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
        while self.processClass.isRunning():
            self.processClass.terminate()
        self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.processClass.isRunning():
            a0.ignore()

class ProcesoCarga(QThread):
        

    update_progress_bar = pyqtSignal(int)

    def run(self):
        self.setTerminationEnabled(True)
        self.contador = 0
        while self.contador <= 100:
            time.sleep(0.1)
            self.update_progress_bar.emit(self.contador)
            self.contador += 10
        self.update_progress_bar.emit(self.contador)


def start_load():
    dialogo = LoadWindow()
    dialogo.exec()

if __name__ == '__main__':
    start_load()    
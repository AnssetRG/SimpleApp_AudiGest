# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CargaArchivos.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class CargandoArchivos(object):
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

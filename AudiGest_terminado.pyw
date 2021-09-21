import sys
import PyQt5
from PyQt5 import QtCore
import librosa
import os
from os import environ
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog,QGraphicsPixmapItem, QGraphicsScene
from numpy.lib.type_check import imag
from Dialogo import Dialogo
from CargaArchivosAplicacion import correr_programa
from Model import AudiGestNet

parameters = {
    "audio": [],
    "audio_path": [],
    "model": [],
    "result": []
}

widgets = {
    "audio_file": []
}

class AudiGest_terminado(QDialog,QMainWindow):
    def __init__(self, windows_size: QtCore.QSize):        
        #inicializadores
        super().__init__()
        self.ui = Dialogo()
        self.ui.setupUi(self, window_size=windows_size)
        self.net = AudiGestNet()
        self.Audio_val = False
        self.Image_val = False
        self.current_answer = None

        #Array que guardará valores referente a cada imagen, por el momento es un array de string
        self.images_values = ["Image 1", "Image 2" ,"Image 3"]
        #Valor actual que se usará como imagen, cambia conforme se seleccione una nueva imagen
        self.image_current_value = None

        #carga imagenes
        self.imagenes()
        
        #variable global
        self.bandera_procesar = False
        #bibliotecas 
        parameters["audio"].append("")
        widgets["audio_file"].append(self.ui.caja_texto1)

        #función de botones
        #a los botones se le está añadiendo la función con 2 parámetros: el valor que guarda la imagen y el botón que está siendo interactuado
        self.ui.radio_btn1.toggled.connect(lambda: (self.set_image_file(self.images_values[0], self.ui.radio_btn1)))
        self.ui.radio_btn2.toggled.connect(lambda: (self.set_image_file(self.images_values[1], self.ui.radio_btn2)))
        self.ui.radio_btn3.toggled.connect(lambda: (self.set_image_file(self.images_values[2], self.ui.radio_btn3)))
        self.ui.btn_cargar.clicked.connect(self.set_new_file)
        self.ui.btn_procesar.clicked.connect(correr_programa) 
        self.ui.btn_procesar.clicked.connect(self.mensaje_boton)
        self.ui.btn_procesar.clicked.connect(self.inferir_audio)

    def load_picture(self, image_path):
        pixmap = QPixmap()
        pixmap.load(image_path)
        item = QGraphicsPixmapItem(pixmap)
        return item
                       
    def imagenes(self):        
        self.scene = QGraphicsScene(self)
        self.scene2 = QGraphicsScene(self)
        self.scene3 = QGraphicsScene(self)
        self.scene.addItem(self.load_picture(os.path.join("imagenes","cara1.png")))
        self.scene2.addItem(self.load_picture(os.path.join("imagenes","cara2.png")))
        self.scene3.addItem(self.load_picture(os.path.join("imagenes","cara3.png")))
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
        fname = QFileDialog.getOpenFileName(None,'Abrir Archivo', os.path.join("Audios"),'Audio (*.wav *.WAV)')
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
                
                #la bandera se enciende cuando el audio es correcto
                self.Audio_val = True
                self.activar_boton_procesar()
                parameters["audio_path"].append(fname[0])
            else:
                self.alert_window()
                if parameters["audio"][-1] == "":
                    resultado = "Nombre del Archivo de Audio"
                                
                else:
                    resultado = parameters["audio"][-1] 
        parameters["audio"].append(resultado)
        widgets["audio_file"][-1].setText(parameters["audio"][-1])

        #Si quieres validar qué path/dirección de audio se está guardando al intentar cargar un archivo
        #if len(parameters["audio_path"]) > 0:
            #print("Current Audio Path: ", parameters["audio_path"][-1])
        #else:
            #print("Current Audio Path: Dictionary is EMPTY")
    
    #Función de cuando es interactuado el botón de las imágenes, solo si se marca entonces se guarda los valores
    def set_image_file(self, image, button):
        if button.isChecked():
            #print("Selected :", image)
            self.Image_val = True
            self.activar_boton_procesar()
            self.image_current_value = image
    
    def alert_window(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText('La duración del audio es mayor a la esperada.')
        msg.setWindowTitle("Error de Carga de Audio")
        msg.exec_()
        
    #Función para validar que tanto el audio como la imagen han sido seleccionados, en ese caso se habilita el botón de procesar
    def activar_boton_procesar(self):
        if self.Audio_val and self.Image_val:
            self.ui.btn_procesar.setEnabled(True)  

    #El mensaje ahora muestra la información del valor guardado actual (referente a la imagen seleccionada)
    def mensaje_boton(self):
        print("La %s ha sido seleccionada" % self.image_current_value)
    
    #Función de la aplicación que llama la inferencia de la red
    def inferir_audio(self):
        self.current_answer = self.net.prediction(path=parameters["audio_path"][-1])
    
    def show_answer(self):
        print(self.current_answer)

            
def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

def main():
    #suppress_qt_warnings()    
    app = QApplication(sys.argv)
    ventana = AudiGest_terminado(windows_size=app.primaryScreen().size())
    ventana.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
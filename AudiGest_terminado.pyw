import sys
import librosa
import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog,QGraphicsPixmapItem, QGraphicsScene
from Dialogo import Dialogo
from LoadWindow import start_load
#from Model import AudiGestNet
from VideoWindow import show_video

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
    def __init__(self):        
        #inicializadores
        super().__init__()
        self.ui = Dialogo()
        self.ui.setupUi(self)
        #self.net = AudiGestNet()
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
        self.ui.btn_procesar.clicked.connect(start_load) 
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
    
    #Función de cuando es interactuado el botón de las imágenes, solo si se marca entonces se guarda los valores
    def set_image_file(self, image, button):
        if button.isChecked():
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
        #video_path = self.net.inference(audio_path=parameters["audio_path"][-1])
        #print("VIDEO: ", video_path)
        show_video()
    
    def show_answer(self):
        print(self.current_answer)

def main(): 
    app = QApplication(sys.argv)
    ventana = AudiGest_terminado()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
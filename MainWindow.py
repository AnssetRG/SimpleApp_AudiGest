from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *


class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent)
        uic.loadUi("Diseños ui\QMediaPlayer.ui",self)
        self.setup()
        self.makeConnections()
    
    def setup(self):
        self.videoOutput = self.makeVideoWidget()
        self.mediaPlayer = self.makeMediaPlayer()
    
    def makeMediaPlayer(self):
        mediaPlayer = QMediaPlayer(self)
        mediaPlayer.setVideoOutput(self.videoOutput)
        return mediaPlayer
    
    def makeVideoWidget(self):
        videoOutput = QVideoWidget(self)
        vbox = QVBoxLayout()
        vbox.addWidget(videoOutput)          
        self.videoWidget.setLayout(vbox)
        return videoOutput

    def makeConnections(self):
        self.actionSalir.triggered.connect(self.close)
        self.actionAbrir.triggered.connect(self.onActionAbrirTriggered)
        self.playButton.clicked.connect(self.mediaPlayer.play)
        self.pauseButton.clicked.connect(self.mediaPlayer.pause)
        self.stopButton.clicked.connect(self.mediaPlayer.stop)

    def onActionAbrirTriggered(self):
        path = QFileDialog.getOpenFileName(self,"Abrir", "/")
        filepath = path[0]
        if path == "":
            return 
        self.mediaPlayer.setMedia(QMediaContent(QUrl(filepath)))
        self.mediaPlayer.play()



from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QFileDialog
import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, QUrl
import os
 
class VideoWindow(QDialog):
    def __init__(self, video_path: str = None):
        super().__init__()

        self.setModal(True)
 
        self.setWindowTitle(video_path.split("/")[-1])
        self.setGeometry(350, 100, 700, 500)
        self.setWindowIcon(QIcon('player.png'))
 
        p =self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)
 
        self.init_ui(video_path)

        self.show()
 
 
    def init_ui(self, video_path: str = None):
 
        #create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
 
        #create videowidget object
        videowidget = QVideoWidget()
  
        #create button for playing
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)
  
        #create slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)
 
        #create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        #create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0,0,0,0)
 
        #set widgets to the hbox layout
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)
 
        #create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)
 
        self.setLayout(vboxLayout)
 
        self.mediaPlayer.setVideoOutput(videowidget)
 
        #media player signals
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
        self.playBtn.setEnabled(True)
 
    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
 
    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        self.slider.setValue(position)
 
    def duration_changed(self, duration):
        self.slider.setRange(0, duration)
 
    def set_position(self, position):
        self.mediaPlayer.setPosition(position)
    
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        print("Closing")
        self.mediaPlayer.stop()
        return super().closeEvent(a0)

def show_video(video_path: str = os.path.join("Videos","TestVideo.wmv")):
    player = VideoWindow(os.path.join(os.getcwd(),video_path))
    player.exec()


if __name__ == '__main__':
  app = QApplication(sys.argv)
  show_video()
  sys.exit(app.exec_())
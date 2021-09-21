import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow

if __name__ == '__main__':    
    app = QApplication([])
    app.setStyle("fusion")
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
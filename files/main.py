import sys
import freefall
from PyQt6 import uic, QtGui
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow



class Wip(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi('uis/wipscreen.ui', self)
        self.pushButton.clicked.connect(self.close)


class Ui(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi('uis/mainmenu.ui', self)
        self.setWindowIcon(QtGui.QIcon('pics/settingsicon.png'))

        self.freefall.clicked.connect(self.loadfreefall)
        self.uniaccmotion.clicked.connect(self.loadwip)
        self.archlaw.clicked.connect(self.loadwip)
        self.friction.clicked.connect(self.loadwip)
        self.exit.clicked.connect(sys.exit)
        self.show()

    def loadwip(self):
        w.show()

    def loadfreefall(self):
        freefall.start()


app = QApplication(sys.argv)
window = Ui()
window.show()
w = Wip()
app.exec()

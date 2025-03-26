from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import sys
from atbsh import AtbashCipherDialog
from ces import CaesarCipherDialog
from resh import RichelieuDialog
from gron import GronsfeldCipherDialog
from vizh import VigenereCipherDialog
from pleiph import PlayfairCipherDialog
from CKA import FrequencyAnalysisDialog

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.ico"))
        self.setWindowTitle("Сборник шифров")
        self.setGeometry(100, 100, 350, 230)
        
        self.label = QtWidgets.QLabel("Выберите шифр:", self)
        self.label.setGeometry(50, 20, 150, 30)
        
        self.atbashButton = QtWidgets.QPushButton("Атбаш", self)
        self.atbashButton.setGeometry(30, 60, 80, 30)
        self.atbashButton.clicked.connect(self.open_atbash)
        
        self.caesarButton = QtWidgets.QPushButton("Цезарь", self)
        self.caesarButton.setGeometry(130, 60, 80, 30)
        self.caesarButton.clicked.connect(self.open_caesar)

        self.ReshButton = QtWidgets.QPushButton("Ришелье", self)
        self.ReshButton.setGeometry(230, 60, 80, 30)
        self.ReshButton.clicked.connect(self.open_resh)

        self.GronButton = QtWidgets.QPushButton("Гронсфельд", self)
        self.GronButton.setGeometry(30, 100, 80, 30)
        self.GronButton.clicked.connect(self.open_gron)

        self.VishButton = QtWidgets.QPushButton("Виженер", self)
        self.VishButton.setGeometry(130, 100, 80, 30)
        self.VishButton.clicked.connect(self.open_vish)

        self.VishButton = QtWidgets.QPushButton("Плейфер", self)
        self.VishButton.setGeometry(230, 100, 80, 30)
        self.VishButton.clicked.connect(self.open_pleiph)

        self.label2 = QtWidgets.QLabel("Выберите интсрумент:", self)
        self.label2.setGeometry(50, 140, 150, 30)

        self.CKAButton = QtWidgets.QPushButton("ЧКА", self)
        self.CKAButton.setGeometry(30, 180, 80, 30)
        self.CKAButton.clicked.connect(self.open_CKA)
    
    def open_atbash(self):
        self.atbash_dialog = AtbashCipherDialog()
        self.atbash_dialog.exec_()
    
    def open_caesar(self):
        self.caesar_dialog = CaesarCipherDialog()
        self.caesar_dialog.exec_()

    def open_resh(self):
        self.resh_dialog = RichelieuDialog()
        self.resh_dialog.exec_()
    
    def open_gron(self):
        self.gron_dialog = GronsfeldCipherDialog()
        self.gron_dialog.exec_()

    def open_vish(self):
        self.vish_dialog = VigenereCipherDialog()
        self.vish_dialog.exec_()

    def open_pleiph(self):
        self.vish_dialog = PlayfairCipherDialog()
        self.vish_dialog.exec_()

    def open_CKA(self):
        self.CKA_dialog = FrequencyAnalysisDialog()
        self.CKA_dialog.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

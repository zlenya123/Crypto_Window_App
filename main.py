from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
import sys
from atbsh import AtbashCipherDialog
from ces import CaesarCipherDialog
from resh import RichelieuDialog
from gron import GronsfeldCipherDialog
from vizh import VigenereCipherDialog
from pleiph import PlayfairCipherDialog
from CKA import FrequencyAnalysisDialog
from gam import GammaCipherDialog
from des import DesCipherDialog

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.ico"))
        self.setWindowTitle("Сборник шифров")
        self.resize(400, 200)

        main_layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel("Выберите шифр:", self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.label)

        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        main_layout.addWidget(separator)

        cipher_buttons_layout = QtWidgets.QHBoxLayout()

        self.atbashButton = QtWidgets.QPushButton("Атбаш", self)
        self.atbashButton.clicked.connect(self.open_atbash)
        cipher_buttons_layout.addWidget(self.atbashButton)

        self.caesarButton = QtWidgets.QPushButton("Цезарь", self)
        self.caesarButton.clicked.connect(self.open_caesar)
        cipher_buttons_layout.addWidget(self.caesarButton)

        self.ReshButton = QtWidgets.QPushButton("Ришелье", self)
        self.ReshButton.clicked.connect(self.open_resh)
        cipher_buttons_layout.addWidget(self.ReshButton)

        main_layout.addLayout(cipher_buttons_layout)

        cipher_buttons_layout2 = QtWidgets.QHBoxLayout()

        self.GronButton = QtWidgets.QPushButton("Гронсфельд", self)
        self.GronButton.clicked.connect(self.open_gron)
        cipher_buttons_layout2.addWidget(self.GronButton)

        self.VishButton = QtWidgets.QPushButton("Виженер", self)
        self.VishButton.clicked.connect(self.open_vish)
        cipher_buttons_layout2.addWidget(self.VishButton)

        self.PleiphButton = QtWidgets.QPushButton("Плейфер", self)
        self.PleiphButton.clicked.connect(self.open_pleiph)
        cipher_buttons_layout2.addWidget(self.PleiphButton)

        main_layout.addLayout(cipher_buttons_layout2)

        cipher_buttons_layout3 = QtWidgets.QHBoxLayout()

        self.DESButton = QtWidgets.QPushButton("DES", self)
        self.DESButton.clicked.connect(self.open_des)
        cipher_buttons_layout3.addWidget(self.DESButton)

        main_layout.addLayout(cipher_buttons_layout3)

        self.label2 = QtWidgets.QLabel("Выберите инструмент:", self)
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.label2)
        separator2 = QtWidgets.QFrame()
        separator2.setFrameShape(QtWidgets.QFrame.HLine)
        separator2.setFrameShadow(QtWidgets.QFrame.Sunken)
        main_layout.addWidget(separator2)
        tools_buttons_layout = QtWidgets.QHBoxLayout()
        self.CKAButton = QtWidgets.QPushButton("Частотный анализ", self)
        self.CKAButton.clicked.connect(self.open_CKA)
        tools_buttons_layout.addWidget(self.CKAButton)

        self.GamButton = QtWidgets.QPushButton("Гаммирование", self)
        self.GamButton.clicked.connect(self.open_gam)
        tools_buttons_layout.addWidget(self.GamButton)
        main_layout.addLayout(tools_buttons_layout)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

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
        self.pleiph_dialog = PlayfairCipherDialog()
        self.pleiph_dialog.exec_()

    def open_CKA(self):
        self.CKA_dialog = FrequencyAnalysisDialog()
        self.CKA_dialog.exec_()

    def open_gam(self):
        self.gam_dialog = GammaCipherDialog()
        self.gam_dialog.exec_()

    def open_des(self):
        self.des_dialog = DesCipherDialog()
        self.des_dialog.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
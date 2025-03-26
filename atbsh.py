from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from alp import ALPHABETS

class AtbashCipherDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.ico"))
        self.setWindowTitle("Шифр Атбаш")
        self.setGeometry(100, 100, 500, 300)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.label = QtWidgets.QLabel("Исходный текст:", self)
        self.label.setGeometry(20, 0, 100, 20)
        
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(20, 20, 460, 80)
        
        self.resultLabel = QtWidgets.QLabel("Результат:", self)
        self.resultLabel.setGeometry(20, 100, 100, 20)
        
        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setGeometry(20, 120, 460, 80)
        
        self.encryptButton = QtWidgets.QPushButton("Шифровать", self)
        self.encryptButton.setGeometry(50, 220, 100, 30)
        self.encryptButton.clicked.connect(self.encrypt_text)
        
        self.decryptButton = QtWidgets.QPushButton("Расшифровать", self)
        self.decryptButton.setGeometry(200, 220, 100, 30)
        self.decryptButton.clicked.connect(self.decrypt_text)
        
        self.clearButton = QtWidgets.QPushButton("Очистить", self)
        self.clearButton.setGeometry(350, 220, 100, 30)
        self.clearButton.clicked.connect(self.clear_text)
    
    def atbash_cipher(self, text):
        result = ""
        for char in text:
            for alphabet in ALPHABETS.values():
                if char in alphabet:
                    result += alphabet[-alphabet.index(char) - 1]
                    break
            else:
                result += char
        return result

    def encrypt_text(self):
        self.textBrowser.setPlainText(self.atbash_cipher(self.textEdit.toPlainText()))
    
    def decrypt_text(self):
        self.encrypt_text()
    
    def clear_text(self):
        self.textEdit.clear()
        self.textBrowser.clear()
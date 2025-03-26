from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from alp import ALPHABETS

class CaesarCipherDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.ico"))
        self.setWindowTitle("Шифр Цезаря")
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
        
        self.shiftLabel = QtWidgets.QLabel("Сдвиг:", self)
        self.shiftLabel.setGeometry(20, 220, 50, 30)
        
        self.spinBox = QtWidgets.QSpinBox(self)
        self.spinBox.setGeometry(80, 220, 50, 30)
        
        self.encryptButton = QtWidgets.QPushButton("Шифровать", self)
        self.encryptButton.setGeometry(150, 220, 100, 30)
        self.encryptButton.clicked.connect(self.encrypt_text)
        
        self.decryptButton = QtWidgets.QPushButton("Расшифровать", self)
        self.decryptButton.setGeometry(260, 220, 100, 30)
        self.decryptButton.clicked.connect(self.decrypt_text)
        
        self.clearButton = QtWidgets.QPushButton("Очистить", self)
        self.clearButton.setGeometry(370, 220, 100, 30)
        self.clearButton.clicked.connect(self.clear_text)
    
    def caesar_cipher(self, text, shift):
        result = []
        for char in text:
            for alphabet in ALPHABETS.values():
                if char in alphabet:
                    result.append(alphabet[(alphabet.index(char) + shift) % len(alphabet)])
                    break
            else:
                result.append(char)
        return "".join(result)

    
    def encrypt_text(self):
        self.textBrowser.setPlainText(self.caesar_cipher(self.textEdit.toPlainText(), self.spinBox.value()))
    
    def decrypt_text(self):
        self.textBrowser.setPlainText(self.caesar_cipher(self.textEdit.toPlainText(), -self.spinBox.value()))
    
    def clear_text(self):
        self.textEdit.clear()
        self.textBrowser.clear()

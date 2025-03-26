from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIcon
from alp import ALPHABETS

class VigenereCipherDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.ico"))
        self.setWindowTitle("Шифр Виженера")
        self.setGeometry(100, 100, 500, 330)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.label = QtWidgets.QLabel("Исходный текст:", self)
        self.label.setGeometry(20, 0, 100, 20)
        
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(20, 20, 460, 80)
        
        self.keyLabel = QtWidgets.QLabel("Ключ (текст):", self)
        self.keyLabel.setGeometry(20, 200, 250, 20)
        
        self.keyEdit = QtWidgets.QLineEdit(self)
        self.keyEdit.setGeometry(20, 220, 460, 30)
        self.keyEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-zA-Zа-яА-Я0-9]+")))
        
        self.resultLabel = QtWidgets.QLabel("Результат:", self)
        self.resultLabel.setGeometry(20, 100, 100, 20)
        
        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setGeometry(20, 120, 460, 80)
        
        self.encryptButton = QtWidgets.QPushButton("Шифровать", self)
        self.encryptButton.setGeometry(100, 270, 100, 30)
        self.encryptButton.clicked.connect(self.encrypt_text)
        
        self.decryptButton = QtWidgets.QPushButton("Расшифровать", self)
        self.decryptButton.setGeometry(210, 270, 100, 30)
        self.decryptButton.clicked.connect(self.decrypt_text)
        
        self.clearButton = QtWidgets.QPushButton("Очистить", self)
        self.clearButton.setGeometry(320, 270, 100, 30)
        self.clearButton.clicked.connect(self.clear_text)

    def show_error(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setWindowIcon(QIcon("icon.ico"))
        msg.setWindowTitle("Ошибка")
        msg.setText(message)
        msg.exec_()

    def valid_key(self, key):
        t_key = []
        for char in key:   
            for alphabet in ALPHABETS.values():
                if char in alphabet:
                    t_key.append(alphabet.index(char))
        return t_key

    def vigenere_cipher(self, text, key_d, decrypt=False):
        result = []
        key = self.valid_key(key_d)
        key_length = len(key)
        i = 0
        for char in text:
            for alphabet in ALPHABETS.values():
                if char in alphabet:
                    shift = key[i % key_length]
                    if decrypt:
                        shift = -shift
                    new_char = alphabet[(alphabet.index(char) + shift) % len(alphabet)]
                    result.append(new_char)
                    i += 1
                    break
            else:
                result.append(char)
        
        return "".join(result)

    def encrypt_text(self):
        text = self.textEdit.toPlainText()
        key = self.keyEdit.text()
        if not key:
            self.show_error("Ошибка: введите ключ")
            return
        encrypted_text = self.vigenere_cipher(text, key)
        self.textBrowser.setPlainText(encrypted_text)

    def decrypt_text(self):
        text = self.textEdit.toPlainText()
        key = self.keyEdit.text()
        if not key:
            self.show_error("Ошибка: введите ключ")
            return
        decrypted_text = self.vigenere_cipher(text, key, decrypt=True)
        self.textBrowser.setPlainText(decrypted_text)

    def clear_text(self):
        self.textEdit.clear()
        self.keyEdit.clear()
        self.textBrowser.clear()
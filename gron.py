from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIcon
from alp import ALPHABETS

class GronsfeldCipherDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.ico"))
        self.setWindowTitle("Шифр Гронсфельда")
        self.resize(500, 300)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        main_layout = QtWidgets.QVBoxLayout()

        title_label = QtWidgets.QLabel("Шифр Гронсфельда", self)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(title_label)

        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        main_layout.addWidget(separator)

        self.label = QtWidgets.QLabel("Исходный текст:", self)
        main_layout.addWidget(self.label)

        self.textEdit = QtWidgets.QTextEdit(self)
        main_layout.addWidget(self.textEdit)

        self.keyLabel = QtWidgets.QLabel("Ключ (цифры):", self)
        main_layout.addWidget(self.keyLabel)

        self.keyEdit = QtWidgets.QLineEdit(self)
        self.keyEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+")))
        main_layout.addWidget(self.keyEdit)

        self.resultLabel = QtWidgets.QLabel("Результат:", self)
        main_layout.addWidget(self.resultLabel)

        self.textBrowser = QtWidgets.QTextBrowser(self)
        main_layout.addWidget(self.textBrowser)

        button_layout = QtWidgets.QHBoxLayout()

        button_layout.addStretch(1)

        self.encryptButton = QtWidgets.QPushButton("Шифровать", self)
        self.encryptButton.clicked.connect(self.encrypt_text)
        button_layout.addWidget(self.encryptButton)
        button_layout.addSpacing(20)

        self.decryptButton = QtWidgets.QPushButton("Расшифровать", self)
        self.decryptButton.clicked.connect(self.decrypt_text)
        button_layout.addWidget(self.decryptButton)
        button_layout.addSpacing(20)

        self.clearButton = QtWidgets.QPushButton("Очистить", self)
        self.clearButton.clicked.connect(self.clear_text)
        button_layout.addWidget(self.clearButton)

        button_layout.addStretch(1)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def show_error(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setWindowIcon(QIcon("icon.ico"))
        msg.setWindowTitle("Ошибка")
        msg.setText(message)
        msg.exec_()

    def gronsfeld_cipher(self, text, key, decrypt=False):
        result = []
        key = [int(digit) for digit in key]
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
        encrypted_text = self.gronsfeld_cipher(text, key)
        self.textBrowser.setPlainText(encrypted_text)

    def decrypt_text(self):
        text = self.textEdit.toPlainText()
        key = self.keyEdit.text()
        if not key:
            self.show_error("Ошибка: введите ключ")
            return
        decrypted_text = self.gronsfeld_cipher(text, key, decrypt=True)
        self.textBrowser.setPlainText(decrypted_text)

    def clear_text(self):
        self.textEdit.clear()
        self.keyEdit.clear()
        self.textBrowser.clear()


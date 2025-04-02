from PyQt5 import QtWidgets, QtCore, QtGui
from alp import ALPHABETS

class AtbashCipherDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.setWindowTitle("Шифр Атбаш")
        self.resize(500, 300)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        main_layout = QtWidgets.QVBoxLayout()

        title_label = QtWidgets.QLabel("Шифр Атбаш", self)
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

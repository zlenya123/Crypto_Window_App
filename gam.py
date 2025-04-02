from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIcon
import base64
import numpy as np

class LinearCongruentialGenerator:
    def __init__(self, seed=1, a=1664525, c=1013904223, m=2**32):
        self.seed = seed
        self.a = a
        self.c = c
        self.m = m

    def next(self):
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed

    def generate(self, length):
        return [self.next() % 256 for _ in range(length)]

class LCGSettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки Линейного Конгруэнтного Генератора")
        self.resize(400, 200)

        main_layout = QtWidgets.QVBoxLayout()

        self.seedLabel = QtWidgets.QLabel("Начальное значение (зерно):", self)
        main_layout.addWidget(self.seedLabel)

        self.seedEdit = QtWidgets.QLineEdit(self)
        self.seedEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+")))
        main_layout.addWidget(self.seedEdit)

        self.aLabel = QtWidgets.QLabel("Множитель (a):", self)
        main_layout.addWidget(self.aLabel)

        self.aEdit = QtWidgets.QLineEdit(self)
        self.aEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+")))
        main_layout.addWidget(self.aEdit)

        self.cLabel = QtWidgets.QLabel("Слагаемое (c):", self)
        main_layout.addWidget(self.cLabel)

        self.cEdit = QtWidgets.QLineEdit(self)
        self.cEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+")))
        main_layout.addWidget(self.cEdit)

        self.mLabel = QtWidgets.QLabel("Модуль (m):", self)
        main_layout.addWidget(self.mLabel)

        self.mEdit = QtWidgets.QLineEdit(self)
        self.mEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+")))
        main_layout.addWidget(self.mEdit)

        button_layout = QtWidgets.QHBoxLayout()

        button_layout.addStretch(1)

        self.okButton = QtWidgets.QPushButton("OK", self)
        self.okButton.clicked.connect(self.accept)
        button_layout.addWidget(self.okButton)

        self.cancelButton = QtWidgets.QPushButton("Отмена", self)
        self.cancelButton.clicked.connect(self.reject)
        button_layout.addWidget(self.cancelButton)

        button_layout.addStretch(1)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def get_settings(self):
        seed = int(self.seedEdit.text())
        a = int(self.aEdit.text())
        c = int(self.cEdit.text())
        m = int(self.mEdit.text())
        return seed, a, c, m

class GammaCipherDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.ico"))
        self.setWindowTitle("Гаммирование")
        self.resize(500, 300)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.lcg_seed = 1
        self.lcg_a = 1664525
        self.lcg_c = 1013904223
        self.lcg_m = 2**32

        main_layout = QtWidgets.QVBoxLayout()

        title_label = QtWidgets.QLabel("Гаммирование", self)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(title_label)

        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        main_layout.addWidget(separator)

        self.configureLCGButton = QtWidgets.QPushButton("Настроить генератор", self)
        self.configureLCGButton.clicked.connect(self.configure_lcg)
        main_layout.addWidget(self.configureLCGButton)

        self.textLabel = QtWidgets.QLabel("Текст:", self)
        main_layout.addWidget(self.textLabel)

        self.textEdit = QtWidgets.QTextEdit(self)
        main_layout.addWidget(self.textEdit)

        self.fileLabel = QtWidgets.QLabel("Файл:", self)
        main_layout.addWidget(self.fileLabel)

        self.fileLineEdit = QtWidgets.QLineEdit(self)
        self.fileLineEdit.setReadOnly(True)
        main_layout.addWidget(self.fileLineEdit)

        self.browseButton = QtWidgets.QPushButton("Обзор...", self)
        self.browseButton.clicked.connect(self.browse_file)
        main_layout.addWidget(self.browseButton)

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

    def browse_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл")
        if file_path:
            self.fileLineEdit.setText(file_path)

    def configure_lcg(self):
        dialog = LCGSettingsDialog(self)
        dialog.seedEdit.setText(str(self.lcg_seed))
        dialog.aEdit.setText(str(self.lcg_a))
        dialog.cEdit.setText(str(self.lcg_c))
        dialog.mEdit.setText(str(self.lcg_m))

        if dialog.exec_():
            self.lcg_seed, self.lcg_a, self.lcg_c, self.lcg_m = dialog.get_settings()

    def generate_gamma(self, length, seed):
        lcg = LinearCongruentialGenerator(seed=seed, a=self.lcg_a, c=self.lcg_c, m=self.lcg_m)
        return np.array(lcg.generate(length), dtype=np.uint8)


    def xor_data(self, data, gamma):
        gamma = gamma[:len(data)]
        return bytes(np.bitwise_xor(np.frombuffer(data, dtype=np.uint8), gamma))

    def encrypt_text(self):
        text = self.textEdit.toPlainText().encode('utf-8')
        file_path = self.fileLineEdit.text()

        if text and file_path:
            self.show_error("Ошибка: выберите либо текст, либо файл, но не оба")
            return
        if not text and not file_path:
            self.show_error("Ошибка: введите текст или выберите файл")
            return

        seed = self.lcg_seed
        if text:
            gamma = self.generate_gamma(len(text), seed)
            encrypted_text = self.xor_data(text, gamma)
            self.textBrowser.setPlainText(base64.b64encode(encrypted_text).decode('utf-8')) 
        elif file_path:
            with open(file_path, 'rb') as f:
                data = f.read()
            gamma = self.generate_gamma(len(data), seed)
            encrypted_data = self.xor_data(data, gamma)
            save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить зашифрованный файл")
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(encrypted_data)

    def decrypt_text(self):
        text = self.textEdit.toPlainText()
        file_path = self.fileLineEdit.text()

        if text and file_path:
            self.show_error("Ошибка: выберите либо текст, либо файл, но не оба")
            return
        if not text and not file_path:
            self.show_error("Ошибка: введите текст или выберите файл")
            return

        seed = self.lcg_seed
        if text:
            try:
                text_bytes = base64.b64decode(text) 
                gamma = self.generate_gamma(len(text_bytes), seed)
                decrypted_text = self.xor_data(text_bytes, gamma)
                self.textBrowser.setPlainText(decrypted_text.decode('utf-8', errors='ignore'))
            except ValueError:
                self.show_error("Ошибка: некорректный ввод (ожидался Base64)")
        elif file_path:
            with open(file_path, 'rb') as f:
                data = f.read()
            gamma = self.generate_gamma(len(data), seed)
            decrypted_data = self.xor_data(data, gamma)
            save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить расшифрованный файл")
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(decrypted_data)


    def clear_text(self):
        self.textEdit.clear()
        self.fileLineEdit.clear()
        self.textBrowser.clear()
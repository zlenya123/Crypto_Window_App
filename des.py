from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
import base64
from des_cipher import decrypt, decrypt_bytes, encrypt_bytes_with_key, generate_des_key, encrypt_with_key
from gam import LCGSettingsDialog

class DesCipherDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.ico"))
        self.setWindowTitle("DES Шифрование")
        self.resize(500, 400)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.generated_key = None
        self.encrypted_bits = None
        self.lcg_seed = 1
        self.lcg_a = 1664525
        self.lcg_c = 1013904223
        self.lcg_m = 2**32
        
        layout = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel("DES")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        layout.addWidget(separator)
        
        self.configureLCGButton = QtWidgets.QPushButton("Настроить ЛКГ", self)
        self.configureLCGButton.clicked.connect(self.configure_lcg)
        layout.addWidget(self.configureLCGButton)
        
        self.textEdit = QtWidgets.QTextEdit()
        layout.addWidget(QtWidgets.QLabel("Текст:"))
        layout.addWidget(self.textEdit)
        
        self.keyLabel = QtWidgets.QLabel("Ключ:")
        layout.addWidget(self.keyLabel)
        self.keyTextBrowser = QtWidgets.QTextEdit()
        layout.addWidget(self.keyTextBrowser)
        
        self.manualKeyCheckbox = QtWidgets.QCheckBox("Ввести ключ вручную")
        self.manualKeyCheckbox.stateChanged.connect(self.toggle_key_input)
        layout.addWidget(self.manualKeyCheckbox)

        self.generateKeyButton = QtWidgets.QPushButton("Сгенерировать ключ")
        self.generateKeyButton.clicked.connect(self.generate_random_key)
        layout.addWidget(self.generateKeyButton)
        self.keyTextBrowser.setReadOnly(True)

        self.textBrowser = QtWidgets.QTextBrowser()
        layout.addWidget(QtWidgets.QLabel("Результат:"))
        layout.addWidget(self.textBrowser)
        
        button_layout = QtWidgets.QHBoxLayout()
        self.encryptButton = QtWidgets.QPushButton("Зашифровать")
        self.encryptButton.clicked.connect(self.encrypt_text)
        button_layout.addWidget(self.encryptButton)
        self.decryptButton = QtWidgets.QPushButton("Расшифровать")
        self.decryptButton.clicked.connect(self.decrypt_text)
        button_layout.addWidget(self.decryptButton)
        self.clearButton = QtWidgets.QPushButton("Очистить")
        self.clearButton.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clearButton)
        layout.addLayout(button_layout)
        self.encryptFileButton = QtWidgets.QPushButton("Зашифровать файл")
        self.encryptFileButton.clicked.connect(self.encrypt_file)
        layout.addWidget(self.encryptFileButton)
        self.decryptFileButton = QtWidgets.QPushButton("Расшифровать файл")
        self.decryptFileButton.clicked.connect(self.decrypt_file)
        layout.addWidget(self.decryptFileButton)
        self.setLayout(layout)

    def toggle_key_input(self, state):
        self.keyTextBrowser.setReadOnly(not bool(state))

    def generate_random_key(self):
        key = generate_des_key(self.lcg_seed, self.lcg_a, self.lcg_c, self.lcg_m)
        self.keyTextBrowser.setPlainText(''.join(map(str, key)))


    def show_error(self, message):
        msg = QtWidgets.QMessageBox(self)
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setWindowTitle("Ошибка")
        msg.setText(message)
        msg.exec_()

    def configure_lcg(self):
        dialog = LCGSettingsDialog(self)
        dialog.seedEdit.setText(str(self.lcg_seed))
        dialog.aEdit.setText(str(self.lcg_a))
        dialog.cEdit.setText(str(self.lcg_c))
        dialog.mEdit.setText(str(self.lcg_m))
        if dialog.exec_():
            self.lcg_seed, self.lcg_a, self.lcg_c, self.lcg_m = dialog.get_settings()

    def validate_key(self, key_string):
        if not all(c in '01' for c in key_string):
            raise ValueError("Ключ должен содержать только 0 и 1.")
        if len(key_string) != 64:
            raise ValueError("Ключ должен состоять из 64 бит (включая биты чётности).")
        return list(map(int, key_string))


    def encrypt_text(self):
        text = self.textEdit.toPlainText()
        if not text:
            self.show_error("Введите текст для шифрования.")
            return

        if self.manualKeyCheckbox.isChecked():
            key_string = self.keyTextBrowser.toPlainText().strip()
            try:
                key = self.validate_key(key_string)
            except ValueError as ve:
                self.show_error(str(ve))
                return
        else:
            key = generate_des_key(self.lcg_seed, self.lcg_a, self.lcg_c, self.lcg_m)
            self.keyTextBrowser.setPlainText(''.join(map(str, key)))
        self.encrypted_bits = encrypt_with_key(text, key)
        self.textBrowser.setPlainText(base64.b64encode(bytes(self.encrypted_bits)).decode('utf-8'))


    def decrypt_text(self):
        encrypted_base64 = self.textEdit.toPlainText().strip()
        key_string = self.keyTextBrowser.toPlainText().strip()
        
        if not encrypted_base64 or not key_string:
            self.show_error("Нет данных для расшифровки. Введите зашифрованные данные и ключ.")
            return
        
        try:
            encrypted_bits = list(map(int, base64.b64decode(encrypted_base64)))
            try:
                key = self.validate_key(key_string)
            except ValueError as ve:
                self.show_error(str(ve))
                return
            decrypted = decrypt(encrypted_bits, key)
            self.textBrowser.setPlainText(decrypted)
        except Exception as e:
            self.show_error(f"Произошла ошибка при расшифровке: {str(e)}")

    def clear_all(self):
        self.textEdit.clear()
        self.textBrowser.clear()
        self.keyTextBrowser.clear()
        self.encrypted_bits = None
        self.generated_key = None

    def encrypt_file(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл для шифрования")
        if not path:
            return

        with open(path, "rb") as f:
            data = f.read()

        if self.manualKeyCheckbox.isChecked():
            key_string = self.keyTextBrowser.toPlainText().strip()
            try:
                key = self.validate_key(key_string)
            except ValueError as ve:
                self.show_error(str(ve))
                return
        else:
            key = generate_des_key(self.lcg_seed, self.lcg_a, self.lcg_c, self.lcg_m)
            self.keyTextBrowser.setPlainText(''.join(map(str, key)))

        encrypted_bits = encrypt_bytes_with_key(data, key)
        save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить зашифрованный файл", filter="*.enc")
        if save_path:
            with open(save_path, "wb") as f:
                f.write(bytes(encrypted_bits))
            QtWidgets.QMessageBox.information(self, "Успех", "Файл успешно зашифрован.")

    def decrypt_file(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите зашифрованный файл")
        if not path:
            return

        key_string = self.keyTextBrowser.toPlainText().strip()
        if not key_string:
            self.show_error("Введите ключ для расшифровки.")
            return

        try:
            key = self.validate_key(key_string)
        except ValueError as ve:
            self.show_error(str(ve))
            return

        with open(path, "rb") as f:
            encrypted_bits = list(f.read())

        try:
            decrypted_bytes = decrypt_bytes(encrypted_bits, key)
            save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить расшифрованный файл")
            if save_path:
                with open(save_path, "wb") as f:
                    f.write(decrypted_bytes)
                QtWidgets.QMessageBox.information(self, "Успех", "Файл успешно расшифрован.")
        except Exception as e:
            self.show_error(f"Ошибка при расшифровке: {e}")


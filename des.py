from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
import base64
from des_cipher import encrypt_bytes_with_key, decrypt_bytes, generate_des_key
from gam import LCGSettingsDialog

class DesCipherDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.ico"))
        self.setWindowTitle("DES Шифрование")
        self.resize(500, 400)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.lcg_seed = 1
        self.lcg_a = 1664525
        self.lcg_c = 1013904223
        self.lcg_m = 2**32

        layout = QtWidgets.QVBoxLayout()

        title = QtWidgets.QLabel("DES")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)
        layout.addWidget(self._separator())

        self.configureLCGButton = QtWidgets.QPushButton("Настроить ЛКГ")
        self.configureLCGButton.clicked.connect(self.configure_lcg)
        layout.addWidget(self.configureLCGButton)

        self.textEdit = QtWidgets.QTextEdit()
        layout.addWidget(QtWidgets.QLabel("Текст:"))
        layout.addWidget(self.textEdit)

        self.keyLabel = QtWidgets.QLabel("Ключ:")
        layout.addWidget(self.keyLabel)
        self.keyTextBrowser = QtWidgets.QTextEdit()
        self.keyTextBrowser.setReadOnly(True)
        layout.addWidget(self.keyTextBrowser)

        self.manualKeyCheckbox = QtWidgets.QCheckBox("Ввести ключ вручную")
        self.manualKeyCheckbox.stateChanged.connect(self.toggle_key_input)
        layout.addWidget(self.manualKeyCheckbox)

        self.generateKeyButton = QtWidgets.QPushButton("Сгенерировать ключ")
        self.generateKeyButton.clicked.connect(self.generate_random_key)
        layout.addWidget(self.generateKeyButton)

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

    def _separator(self):
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        return separator

    def toggle_key_input(self, state):
        self.keyTextBrowser.setReadOnly(not bool(state))

    def generate_random_key(self):
        key = generate_des_key(self.lcg_seed, self.lcg_a, self.lcg_c, self.lcg_m)
        self.keyTextBrowser.setPlainText(''.join(map(str, key)))

    def show_error(self, message):
        QtWidgets.QMessageBox.critical(self, "Ошибка", message)

    def configure_lcg(self):
        dialog = LCGSettingsDialog(self)
        dialog.seedEdit.setText(str(self.lcg_seed))
        dialog.aEdit.setText(str(self.lcg_a))
        dialog.cEdit.setText(str(self.lcg_c))
        dialog.mEdit.setText(str(self.lcg_m))
        if dialog.exec_():
            self.lcg_seed, self.lcg_a, self.lcg_c, self.lcg_m = dialog.get_settings()

    def validate_key(self, key_string):
        if not all(c in '01' for c in key_string) or len(key_string) != 64:
            raise ValueError("Ключ должен состоять из 64 бит (0 и 1).")
        return list(map(int, key_string))

    def get_key(self):
        if self.manualKeyCheckbox.isChecked():
            key_string = self.keyTextBrowser.toPlainText().strip()
            return self.validate_key(key_string)
        else:
            key = generate_des_key(self.lcg_seed, self.lcg_a, self.lcg_c, self.lcg_m)
            self.keyTextBrowser.setPlainText(''.join(map(str, key)))
            return key

    def encrypt_text(self):
        text = self.textEdit.toPlainText()
        if not text:
            self.show_error("Введите текст для шифрования.")
            return
        try:
            key = self.get_key()
            encrypted = encrypt_bytes_with_key(text.encode('utf-8'), key)
            self.textBrowser.setPlainText(base64.b64encode(encrypted).decode('utf-8'))
        except Exception as e:
            self.show_error(f"Ошибка при шифровании: {e}")

    def decrypt_text(self):
        encrypted_base64 = self.textEdit.toPlainText().strip()
        if not encrypted_base64:
            self.show_error("Введите зашифрованный текст.")
            return
        try:
            key = self.get_key()
            encrypted_bytes = base64.b64decode(encrypted_base64)
            decrypted = decrypt_bytes(encrypted_bytes, key)
            self.textBrowser.setPlainText(decrypted.decode('utf-8', errors='ignore'))
        except Exception as e:
            self.show_error(f"Ошибка при расшифровке: {e}")

    def clear_all(self):
        self.textEdit.clear()
        self.textBrowser.clear()
        self.keyTextBrowser.clear()

    def encrypt_file(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл для шифрования")
        if not path:
            return
        try:
            with open(path, "rb") as f:
                data = f.read()
            key = self.get_key()
            encrypted_data = encrypt_bytes_with_key(data, key)
            save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить зашифрованный файл", filter="*.enc")
            if save_path:
                with open(save_path, "wb") as f:
                    f.write(encrypted_data)
                QtWidgets.QMessageBox.information(self, "Успех", "Файл успешно зашифрован.")
        except Exception as e:
            self.show_error(f"Ошибка при шифровании файла: {e}")

    def decrypt_file(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите зашифрованный файл")
        if not path:
            return
        try:
            with open(path, "rb") as f:
                encrypted_data = f.read()
            key = self.get_key()
            decrypted_data = decrypt_bytes(encrypted_data, key)
            save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить расшифрованный файл")
            if save_path:
                with open(save_path, "wb") as f:
                    f.write(decrypted_data)
                QtWidgets.QMessageBox.information(self, "Успех", "Файл успешно расшифрован.")
        except Exception as e:
            self.show_error(f"Ошибка при расшифровке файла: {e}")

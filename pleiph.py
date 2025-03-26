from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIcon
from alp import ALPHABETS

class PlayfairCipherDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.ico"))
        self.setWindowTitle("Шифр Плейфера")
        self.setGeometry(100, 100, 500, 380)
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

    def prepare_alphabet(self, key):
        unique_key = "".join(sorted(set(key), key=key.index))
        full_alphabet = "".join(ALPHABETS.values())
        for char in full_alphabet:
            if char not in unique_key:
                unique_key += char
        return [list(unique_key[i:i+16]) for i in range(0, 128, 16)]

    def find_position(self, matrix, char):
        for r, row in enumerate(matrix):
            if char in row:
                return r, row.index(char)
        return None, None

    def playfair_cipher(self, text, key, decrypt=False):
        matrix = self.prepare_alphabet(key)
        allowed_chars = set(ALPHABETS['ru_lower'] + ALPHABETS['ru_upper'] + ALPHABETS['en_lower'] + ALPHABETS['en_upper'] + ALPHABETS['digits'])
        
        filtered_text = "".join([char for char in text if char in allowed_chars])
        
        pairs = []
        i = 0
        while i < len(filtered_text):
            a = filtered_text[i]
            b = filtered_text[i + 1] if i + 1 < len(filtered_text) else "X"
            
            if a == b:
                b = "X"
                i += 1
            else:
                i += 2
            
            pairs.append((a, b))
        
        result = []
        for a, b in pairs:
            row1, col1 = self.find_position(matrix, a)
            row2, col2 = self.find_position(matrix, b)
            
            if row1 == row2:
                result.append(matrix[row1][(col1 + (1 if not decrypt else -1)) % 16])
                result.append(matrix[row2][(col2 + (1 if not decrypt else -1)) % 16])
            elif col1 == col2:
                result.append(matrix[(row1 + (1 if not decrypt else -1)) % 8][col1])
                result.append(matrix[(row2 + (1 if not decrypt else -1)) % 8][col2])
            else:
                result.append(matrix[row1][col2])
                result.append(matrix[row2][col1])
        
        return "".join(result)


    def encrypt_text(self):
        text = self.textEdit.toPlainText()
        key = self.keyEdit.text()
        if not key:
            self.show_error("Ошибка: введите ключ")
            return
        encrypted_text = self.playfair_cipher(text, key)
        self.textBrowser.setPlainText(encrypted_text)

    def decrypt_text(self):
        text = self.textEdit.toPlainText()
        key = self.keyEdit.text()
        if not key:
            self.show_error("Ошибка: введите ключ")
            return
        decrypted_text = self.playfair_cipher(text, key, decrypt=True)
        self.textBrowser.setPlainText(decrypted_text)

    def clear_text(self):
        self.textEdit.clear()
        self.keyEdit.clear()
        self.textBrowser.clear()

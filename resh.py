from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIcon
import re

class RichelieuDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.ico"))
        self.setWindowTitle("Шифр Ришелье")
        self.setGeometry(100, 100, 500, 330)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        
        self.label = QtWidgets.QLabel("Исходный текст:", self)
        self.label.setGeometry(20, 0, 100, 20)
        
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(20, 20, 460, 80)
        
        self.patternLabel = QtWidgets.QLabel("Перестановки (Пример: (2,3,1,4,5)", self)
        self.patternLabel.setGeometry(20, 200, 250, 20)
        
        self.patternEdit = QtWidgets.QLineEdit(self)
        self.patternEdit.setGeometry(20, 220, 460, 30)
        self.patternEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r"(\(\d+(,\d+)*\))+")))
        
        self.resultLabel = QtWidgets.QLabel("Результат:", self)
        self.resultLabel.setGeometry(20, 100, 100, 20)
        
        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setGeometry(20, 120, 460, 80)
        
        self.Button = QtWidgets.QPushButton("Шифровать", self)
        self.Button.setGeometry(100, 270, 100, 30)
        self.Button.clicked.connect(self.encrypt)

        self.Button2 = QtWidgets.QPushButton("Расшифровать", self)
        self.Button2.setGeometry(210, 270, 100, 30)
        self.Button2.clicked.connect(self.decrypt)

        self.clearButton = QtWidgets.QPushButton("Очистить", self)
        self.clearButton.setGeometry(320, 270, 100, 30)
        self.clearButton.clicked.connect(self.clear_text)
    
    def show_error(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setWindowIcon(QIcon("icon.ico"))
        msg.setWindowTitle("Ошибка")
        msg.setText(message)
        msg.exec_()
    
    
    def validate_pattern(self, pattern_str, text_length):
        if not re.fullmatch(r"(\(\d+(,\d+)*\))+$", pattern_str):
            return False
        groups = re.findall(r"\((.*?)\)", pattern_str)
        total_numbers = 0
        
        for group in groups:
            numbers = list(map(int, group.split(',')))
            if sorted(numbers) != list(range(1, len(numbers) + 1)):
                return False  # Проверка, что числа идут последовательно
            total_numbers += len(numbers)
        
        return total_numbers <= text_length
        
    def parse_permutations(self, pattern_str, text_length):
        if not self.validate_pattern(pattern_str, text_length):
            return []
        return [list(map(int, group.split(','))) for group in re.findall(r"\((.*?)\)", pattern_str)]
    
    def richelieu_cipher(self, text, key_groups, reverse=False):
        text_list = list(text)
        index = 0
        
        for group in key_groups:
            if index + len(group) > len(text_list):
                break  
            
            indices = [index + i for i in range(len(group))]
            index += len(group)
            
            if reverse:
                order = [group.index(i + 1) for i in range(len(group))]
            else:
                order = [i - 1 for i in group]
            
            temp = [text_list[indices[i]] for i in order]
            for i, val in zip(indices, temp):
                text_list[i] = val
        
        return "".join(text_list)
    

    def encrypt(self):
        text = self.textEdit.toPlainText()
        pattern_str = self.patternEdit.text()
        key_groups = self.parse_permutations(pattern_str, len(text))
        
        if not text or not key_groups:
            self.show_error("Ошибка: проверьте ввод.")
            return
        
        encrypted_text = self.richelieu_cipher(text, key_groups)
        self.textBrowser.setText(encrypted_text)
    
    def decrypt(self):
        text = self.textEdit.toPlainText()
        pattern_str = self.patternEdit.text()
        key_groups = self.parse_permutations(pattern_str, len(text))
        
        if not text or not key_groups:
            self.show_error("Ошибка: проверьте ввод.")
            return
        
        decrypted_text = self.richelieu_cipher(text, key_groups, reverse=True)
        self.textBrowser.setText(decrypted_text)

    def clear_text(self):
        self.textEdit.clear()
        self.textBrowser.clear()
        self.patternEdit.clear()
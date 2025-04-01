from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIcon
from collections import Counter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random

# Таблицы вероятностей
RUSSIAN_PROBABILITIES = {
    'о': 0.090, 'е': 0.072, 'а': 0.062, 'и': 0.062, 'н': 0.053,
    'т': 0.053, 'с': 0.045, 'р': 0.040, 'в': 0.038, 'л': 0.035,
    'к': 0.028, 'м': 0.026, 'д': 0.025, 'п': 0.023, 'у': 0.021,
    'я': 0.018, 'ы': 0.016, 'з': 0.016, 'ь': 0.014, 'б': 0.014,
    'г': 0.013, 'ч': 0.012, 'й': 0.010, 'х': 0.009, 'ж': 0.007,
    'ю': 0.006, 'ш': 0.006, 'ц': 0.004, 'щ': 0.003, 'э': 0.003,
    'ф': 0.002, 'ё': 0.001, 'ъ': 0.001  # Добавляем буквы 'ё' и 'ъ'
}

ENGLISH_PROBABILITIES = {
    'e': 0.123, 't': 0.096, 'a': 0.081, 'o': 0.079, 'n': 0.072,
    'i': 0.071, 's': 0.066, 'r': 0.060, 'h': 0.051, 'l': 0.040,
    'd': 0.036, 'c': 0.032, 'u': 0.031, 'p': 0.023, 'f': 0.023,
    'm': 0.022, 'w': 0.020, 'y': 0.019, 'b': 0.016, 'g': 0.016,
    'v': 0.009, 'k': 0.005, 'x': 0.002, 'q': 0.002, 'j': 0.001,
    'z': 0.001
}

class HistogramWindow(QtWidgets.QDialog):
    def __init__(self, freq_data):
        super().__init__()
        self.setWindowTitle("Гистограмма")
        self.setGeometry(150, 150, 800, 600)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        
        self.figure = Figure(figsize=(8, 5))
        self.canvas = FigureCanvas(self.figure)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.plot_histogram(freq_data)

    def plot_histogram(self, freq_data):
        ax = self.figure.add_subplot(111)
        ax.clear()
        sorted_freq_data = dict(sorted(freq_data.items()))
        ax.bar(sorted_freq_data.keys(), sorted_freq_data.values(), color='skyblue')
        ax.set_title('Частота символов')
        ax.set_xlabel('Символы')
        ax.set_ylabel('Частота (%)')

        # Установка подписей оси X без поворота
        ax.set_xticks(range(len(sorted_freq_data)))
        ax.set_xticklabels(sorted_freq_data.keys(), rotation=0, ha='center')
        ax.tick_params(axis='x', which='both', labelsize=8)

        # Автоматическая настройка макета
        self.figure.tight_layout()

        self.canvas.draw()

class SubstitutionTableWindow(QtWidgets.QDialog):
    def __init__(self, language="ru", substitution_table=None, available_chars=None):
        super().__init__()
        self.language = language
        self.setWindowTitle(f"Таблица замен ({'Русский' if language == 'ru' else 'Английский'})")
        self.setGeometry(150, 150, 600, 400)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Исходный символ", "Замена"])
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSortingEnabled(True)

        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.tableWidget)

        self.saveButton = QtWidgets.QPushButton("Сохранить", self)
        self.saveButton.clicked.connect(self.save_table)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.scrollArea)
        layout.addWidget(self.saveButton)
        self.setLayout(layout)

        self.available_chars = available_chars if available_chars else set()
        self.load_table(substitution_table)

    def load_table(self, substitution_table):
        probabilities = RUSSIAN_PROBABILITIES if self.language == "ru" else ENGLISH_PROBABILITIES
        self.substitution_table = substitution_table if substitution_table else {char: char for char in probabilities.keys()}
        self.tableWidget.setRowCount(len(probabilities))

        for row, char in enumerate(sorted(probabilities.keys())):
            item_original = QtWidgets.QTableWidgetItem(char)
            item_original.setFlags(item_original.flags() & ~QtCore.Qt.ItemIsEditable)
            self.tableWidget.setItem(row, 0, item_original)

            # Создаем QLineEdit для редактирования замены
            line_edit = QtWidgets.QLineEdit(self.substitution_table[char])
            line_edit.setMaxLength(1)  # Разрешаем только один символ
            line_edit.textChanged.connect(lambda text, row=row: self.on_text_changed(text, row))
            self.tableWidget.setCellWidget(row, 1, line_edit)

    def on_text_changed(self, text, row):
        original_char = self.tableWidget.item(row, 0).text()
        new_value = text

        if not new_value:
            return

        if self.language == "ru" and not all(c.isalpha() and c in RUSSIAN_PROBABILITIES for c in new_value):
            QtWidgets.QMessageBox.warning(self, "Ошибка", "В таблицу для русских символов можно вводить только русские символы!")
            line_edit = self.tableWidget.cellWidget(row, 1)
            line_edit.setText(self.substitution_table[original_char])
            return

        if self.language == "en" and not all(c.isalpha() and c in ENGLISH_PROBABILITIES for c in new_value):
            QtWidgets.QMessageBox.warning(self, "Ошибка", "В таблицу для английских символов можно вводить только английские символы!")
            line_edit = self.tableWidget.cellWidget(row, 1)
            line_edit.setText(self.substitution_table[original_char])
            return

        old_value = self.substitution_table[original_char]

        # Проверяем, есть ли дубликаты и обновляем соответствующие строки
        for r in range(self.tableWidget.rowCount()):
            if r == row:
                continue
            line_edit = self.tableWidget.cellWidget(r, 1)
            if line_edit.text() == new_value:
                # Найдено совпадение с другим символом
                other_char = self.tableWidget.item(r, 0).text()
                # Переназначаем старое значение для этой буквы
                line_edit.setText(old_value)
                self.substitution_table[other_char] = old_value
                break

        # Обновляем текущий символ
        self.substitution_table[original_char] = new_value

    def save_table(self):
        for row in range(self.tableWidget.rowCount()):
            original = self.tableWidget.item(row, 0).text()
            replacement = self.tableWidget.cellWidget(row, 1).text()
            self.substitution_table[original] = replacement
        QtWidgets.QMessageBox.information(self, "Успех", "Таблица замен сохранена!")
        self.accept()

class FrequencyAnalysisDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.ico"))
        self.setWindowTitle("Частотный анализ")
        self.setGeometry(100, 100, 500, 400)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        # Текстовый ввод
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(20, 20, 460, 80)

        # Кнопки
        self.loadButton = QtWidgets.QPushButton("Загрузить из файла", self)
        self.loadButton.clicked.connect(self.load_from_file)

        self.clearButton = QtWidgets.QPushButton("Очистить", self)
        self.clearButton.clicked.connect(self.clear_text)

        # Гистограмма
        self.plotButton = QtWidgets.QPushButton("Построить гистограмму", self)
        self.plotButton.clicked.connect(self.plot_histogram)

        # Дополнительные кнопки
        self.ruSubstitutionButton = QtWidgets.QPushButton("Таблица замен (Русский)", self)
        self.ruSubstitutionButton.clicked.connect(lambda: self.open_substitution_table("ru"))

        self.enSubstitutionButton = QtWidgets.QPushButton("Таблица замен (Английский)", self)
        self.enSubstitutionButton.clicked.connect(lambda: self.open_substitution_table("en"))

        self.decryptButton = QtWidgets.QPushButton("Дешифровать текст", self)
        self.decryptButton.clicked.connect(self.decrypt_text)

        self.saveDecryptedButton = QtWidgets.QPushButton("Сохранить расшифрованный текст", self)
        self.saveDecryptedButton.clicked.connect(self.save_decrypted_text)

        self.decryptedBrowser = QtWidgets.QTextBrowser(self)
        self.decryptedBrowser.setPlaceholderText("Расшифрованный текст будет отображён здесь")

        # Макет
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.textEdit)

        buttonLayout = QtWidgets.QGridLayout()
        buttonLayout.addWidget(self.loadButton, 0, 0)
        buttonLayout.addWidget(self.clearButton, 0, 1)
        buttonLayout.addWidget(self.plotButton, 1, 0, 1, 2)
        buttonLayout.addWidget(self.ruSubstitutionButton, 2, 0)
        buttonLayout.addWidget(self.enSubstitutionButton, 2, 1)
        buttonLayout.addWidget(self.decryptButton, 3, 0)
        buttonLayout.addWidget(self.saveDecryptedButton, 3, 1)
        layout.addLayout(buttonLayout)

        layout.addWidget(self.decryptedBrowser)

        self.setLayout(layout)

        self.freq_data = None
        self.substitution_tables = {"ru": {}, "en": {}}
        self.available_chars = {"ru": set(), "en": set()}
        self.decrypted_text = ""

    def load_from_file(self):
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выбрать файл", "", "Текстовые файлы (*.txt);;Все файлы (*)", options=options)
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.textEdit.setText(file.read())

    def clear_text(self):
        self.textEdit.clear()
        self.decryptedBrowser.clear()
        self.freq_data = None
        self.available_chars = {"ru": set(), "en": set()}
        self.decrypted_text = ""

    def analyze_text(self):
        text = self.textEdit.toPlainText()
        if not text:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите текст для анализа")
            return

        # Подсчет частоты, игнорируя пробелы и неалфавитные символы
        text_lower = text.lower()
        text_filtered = ''.join([char for char in text_lower if char.isalpha() and (char in RUSSIAN_PROBABILITIES or char in ENGLISH_PROBABILITIES)])
        freq = Counter(text_filtered)
        total_chars = sum(freq.values())

        self.freq_data = {char: round(count / total_chars * 100, 2) for char, count in freq.items()}

        # Автоматическая генерация таблицы замен
        if any(char in RUSSIAN_PROBABILITIES for char in text_lower):
            self.generate_substitution_table("ru")
        if any(char in ENGLISH_PROBABILITIES for char in text_lower):
            self.generate_substitution_table("en")

    def generate_substitution_table(self, language):
        probabilities = RUSSIAN_PROBABILITIES if language == "ru" else ENGLISH_PROBABILITIES
        sorted_chars_by_freq = sorted(self.freq_data, key=self.freq_data.get, reverse=True)
        sorted_chars_by_prob = sorted(probabilities, key=probabilities.get, reverse=True)

        substitution_table = {}
        available_chars = set()

        for orig_char, prob_char in zip(sorted_chars_by_freq, sorted_chars_by_prob):
            if orig_char in probabilities:
                substitution_table[orig_char] = prob_char
                available_chars.add(prob_char)

        # Заполняем оставшиеся символы
        for orig_char in probabilities:
            if orig_char not in substitution_table:
                for prob_char in sorted_chars_by_prob:
                    if prob_char not in available_chars:
                        substitution_table[orig_char] = prob_char
                        available_chars.add(prob_char)
                        break

        self.substitution_tables[language] = substitution_table
        self.available_chars[language] = available_chars

    def plot_histogram(self):
        self.analyze_text()
        if not self.freq_data:
            return

        self.hist_window = HistogramWindow(self.freq_data)
        self.hist_window.exec_()

    def open_substitution_table(self, language):
        table_window = SubstitutionTableWindow(language, self.substitution_tables.get(language), self.available_chars.get(language))
        if table_window.exec_():
            self.substitution_tables[language] = table_window.substitution_table
            self.available_chars[language] = table_window.available_chars

    def decrypt_text(self):
        encrypted_text = self.textEdit.toPlainText()
        if not encrypted_text:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите текст для дешифровки")
            return

        if not self.substitution_tables["ru"] and not self.substitution_tables["en"]:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Сначала настройте таблицу замен!")
            return

        language = "ru" if self.substitution_tables["ru"] else "en"
        substitution_table = self.substitution_tables[language]

        # Сохранение регистра символов
        decrypted_text = []
        for char in encrypted_text:
            if char.lower() in substitution_table:
                if char.isupper():
                    decrypted_text.append(substitution_table[char.lower()].upper())
                else:
                    decrypted_text.append(substitution_table[char.lower()])
            else:
                decrypted_text.append(char)

        self.decrypted_text = ''.join(decrypted_text)
        self.decryptedBrowser.setText(self.decrypted_text)

    def save_decrypted_text(self):
        if not self.decrypted_text:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Сначала дешифруйте текст!")
            return

        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Текстовые файлы (*.txt);;Все файлы (*)", options=options)
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.decrypted_text)
            QtWidgets.QMessageBox.information(self, "Успех", "Расшифрованный текст сохранен!")
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from collections import Counter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class HistogramWindow(QtWidgets.QDialog):
    def __init__(self, freq_data):
        super().__init__()
        self.setWindowTitle("Гистограмма")
        self.setGeometry(150, 150, 600, 400)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.plot_histogram(freq_data)

    def plot_histogram(self, freq_data):
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.bar(freq_data.keys(), freq_data.values(), color='skyblue')
        ax.set_title('Частота символов')
        ax.set_xlabel('Символы')
        ax.set_ylabel('Частота (%)')
        self.canvas.draw()

class FrequencyAnalysisDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.ico"))
        self.setWindowTitle("Частотный анализ")
        self.setGeometry(100, 100, 500, 300)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        
        # Текстовый ввод
        self.label = QtWidgets.QLabel("Исходный текст:", self)
        self.label.setGeometry(20, 0, 100, 20)

        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(20, 20, 460, 80)
        
        # Кнопки
        self.loadButton = QtWidgets.QPushButton("Загрузить из файла", self)
        self.loadButton.setGeometry(20, 220, 140, 30)
        self.loadButton.clicked.connect(self.load_from_file)
        
        self.analyzeButton = QtWidgets.QPushButton("Анализировать", self)
        self.analyzeButton.setGeometry(180, 220, 140, 30)
        self.analyzeButton.clicked.connect(self.analyze_text)
        
        self.clearButton = QtWidgets.QPushButton("Очистить", self)
        self.clearButton.setGeometry(340, 220, 140, 30)
        self.clearButton.clicked.connect(self.clear_text)
        
        # Вывод результатов
        self.resultLabel = QtWidgets.QLabel("Результат:", self)
        self.resultLabel.setGeometry(20, 100, 100, 20)
        
        self.resultBrowser = QtWidgets.QTextBrowser(self)
        self.resultBrowser.setGeometry(20, 120, 460, 80)
        
        # Гистограмма
        self.plotButton = QtWidgets.QPushButton("Построить гистограмму", self)
        self.plotButton.setGeometry(20, 260, 460, 30)
        self.plotButton.clicked.connect(self.plot_histogram)
        
        self.freq_data = None
    
    def load_from_file(self):
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выбрать файл", "", "Текстовые файлы (*.txt);;Все файлы (*)", options=options)
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.textEdit.setText(file.read())

    def clear_text(self):
        self.textEdit.clear()
        self.resultBrowser.clear()
        self.freq_data = None
    
    def analyze_text(self):
        text = self.textEdit.toPlainText()
        if not text:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите текст для анализа")
            return
        
        # Подсчет частоты
        text = text.lower()
        text = ''.join([char for char in text if char.isalnum() or char.isspace()])
        freq = Counter(text)
        total_chars = sum(freq.values())
        
        self.freq_data = {char: round(count / total_chars * 100, 2) for char, count in freq.items()}
        
        result = "Частота символов:\n"
        for char, percent in self.freq_data.items():
            result += f"{char}: {percent:.2f}%\n"
        
        self.resultBrowser.setText(result)
    
    def plot_histogram(self):
        if not self.freq_data:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Сначала выполните анализ текста")
            return

        self.hist_window = HistogramWindow(self.freq_data)
        self.hist_window.exec_()

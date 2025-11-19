from PySide6 import QtCore
print(QtCore.__version__)


from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Моё первое приложение на PySide6')
        self.setGeometry(1000, 500, 600, 400)
        button = QPushButton('Нажми меня', self)
        button.clicked.connect(self.on_button_clicked)
        button.setGeometry(200, 150, 200, 50)

    def on_button_clicked(self):
        print('Кнопка нажата!')

if __name__== "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()

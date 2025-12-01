from PyQt6.QtWidgets import QApplication
from components.MainWindow import MainWindow

app = QApplication([])
window = MainWindow()
window.show()
app.exec()

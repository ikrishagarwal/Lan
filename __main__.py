from PyQt6.QtWidgets import QApplication
from components.MainWindow import MainWindow

app = QApplication([])
app.setApplicationDisplayName("Lan Config")

window = MainWindow()
window.show()
app.exec()

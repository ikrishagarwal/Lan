from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QCoreApplication
from components.MainWindow import MainWindow

app = QApplication([])
# app.setApplicationDisplayName("Lan Config")

QCoreApplication.setOrganizationName("LanConfig")
QCoreApplication.setApplicationName("Lan Config")

window = MainWindow()
window.show()
app.exec()

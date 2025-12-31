import platform
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtGui import QIcon
from components.MainWindow import MainWindow
from globals import resource_path

if platform.system() == "Windows":
  import ctypes
  app_id = 'dev.ikrish.lanconfig.v1'
  ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

app = QApplication([])
app.setWindowIcon(QIcon(resource_path("assets/icon.png")))

QCoreApplication.setOrganizationName("LanConfig")
QCoreApplication.setApplicationName("Lan Config")

window = MainWindow()
window.show()
app.exec()

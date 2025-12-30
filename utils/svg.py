from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QByteArray
from PyQt6.QtSvgWidgets import QSvgWidget


class ColorSvgWidget(QSvgWidget):
  def __init__(self, path: str, color: str, size=24):
    super().__init__()

    self.path = path
    self.setFixedSize(size, size)
    self.setColor(color)

  def setColor(self, color: str):
    with open(self.path, 'r') as f:
      svg_data = f.read()

      new_data = svg_data.replace("currentColor", color)
      self.load(QByteArray(new_data.encode('utf-8')))


class ColorIcon(QIcon):
  def __init__(self, path: str, color: str):
    super().__init__()

    self.path = path
    self.setColor(color)

  def setColor(self, color: str):
    with open(self.path, 'r') as f:
      svg_data = f.read()

      new_data = svg_data.replace("currentColor", color)
      byte_data = QByteArray(new_data.encode('utf-8'))

      pixmap = QPixmap()
      pixmap.loadFromData(byte_data)
      self.addPixmap(pixmap)

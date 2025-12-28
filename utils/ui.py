from PyQt6.QtWidgets import QLabel, QFrame, QSizePolicy
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt


class H1(QLabel):
  def __init__(self, text):
    super().__init__(text)
    font_style = QFont(
      'ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"', 18)
    self.setFont(font_style)
    self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)


class H2(QLabel):
  def __init__(self, text):
    super().__init__(text)
    font_style = QFont(
      'ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"', 14)
    self.setFont(font_style)
    self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)


class H3(QLabel):
  def __init__(self, text):
    super().__init__(text)
    font_style = QFont(
      'ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"', 12)
    self.setFont(font_style)
    self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)


class SubText(QLabel):
  def __init__(self, text):
    super().__init__(text)
    font_style = QFont(
      'ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"', 10)
    self.setFont(font_style)

    palette = self.palette()
    palette.setColor(QPalette.ColorRole.WindowText,
                     QColor(Qt.GlobalColor.gray))
    self.setPalette(palette)
    self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)


class Hr(QFrame):
  def __init__(self):
    super().__init__()
    self.setFrameShape(QFrame.Shape.HLine)
    self.setFrameShadow(QFrame.Shadow.Sunken)
    self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)


class VerticalBar(QFrame):
  def __init__(self):
    super().__init__()
    self.setFrameShape(QFrame.Shape.VLine)
    self.setFrameShadow(QFrame.Shadow.Sunken)
    self.setLineWidth(1)
    self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

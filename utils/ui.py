from PyQt6.QtWidgets import QLabel, QFrame, QSizePolicy
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt


class H1(QLabel):
  def __init__(self, text):
    super().__init__(text)
    font = self.font()
    font.setPointSize(18)
    self.setFont(font)
    self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)


class H2(QLabel):
  def __init__(self, text):
    super().__init__(text)
    font = self.font()
    font.setPointSize(14)
    self.setFont(font)
    self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)


class H3(QLabel):
  def __init__(self, text):
    super().__init__(text)
    font = self.font()
    font.setPointSize(12)
    self.setFont(font)
    self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)


class H4(QLabel):
  def __init__(self, text):
    super().__init__(text)
    font = self.font()
    font.setPointSize(11)
    self.setFont(font)
    self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)


class SubText(QLabel):
  def __init__(self, text):
    super().__init__(text)
    font = self.font()
    font.setPointSize(10)
    self.setFont(font)

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

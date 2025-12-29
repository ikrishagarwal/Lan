from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from utils.ui import SubText


class NoAdapter(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)
    self._layout = QVBoxLayout()

    loading_label = SubText("Can't detect any Ethernet Adapters")
    loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    self._layout.addStretch()
    self._layout.addWidget(loading_label)
    self._layout.addStretch()

    self.setLayout(self._layout)

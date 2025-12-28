from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from utils.ui import SubText


class Loader(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setFixedSize(200, 100)

    self._layout = QHBoxLayout()
    self.setLayout(self._layout)

    loading_label = SubText("Loading State ...")
    loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    self._layout.addStretch(1)
    self._layout.addWidget(loading_label)

    # spacer = QSpacerItem(
    #   0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
    # )

    # self._layout.addItem(spacer)
    # self._layout.addStretch(1)

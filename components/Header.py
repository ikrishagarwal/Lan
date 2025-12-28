from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtCore import Qt
import globals
from utils.ui import H2, Hr, SubText


class Header(QWidget):
  def __init__(self):
    super().__init__()

    self._h_layout = QHBoxLayout()
    self._layout = QVBoxLayout()

    self._h_layout.setContentsMargins(0, 0, 0, 0)
    self._h_layout.setSpacing(10)

    header = QVBoxLayout()
    header.setContentsMargins(0, 0, 10, 0)
    header.setSpacing(0)

    title_label = H2(globals.TITLE)
    header.addWidget(title_label)

    sub_text = SubText("Generate commands for Windows, MacOS, and Linux")
    header.addWidget(sub_text)

    server_icon = QSvgWidget("assets/server.svg")
    server_icon.setFixedSize(24, 24)
    # server_icon.setSizePolicy(
    # QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

    self._h_layout.addWidget(server_icon, 0, Qt.AlignmentFlag.AlignVCenter)
    self._h_layout.addLayout(header, 1)

    self._layout.addLayout(self._h_layout)
    self._layout.addWidget(Hr())
    self.setLayout(self._layout)

    self.setSizePolicy(QSizePolicy.Policy.Preferred,
                       QSizePolicy.Policy.Fixed)

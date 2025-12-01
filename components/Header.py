from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtCore import Qt
import globals
from utils.ui import H2, SubText


class Header(QHBoxLayout):
  def __init__(self):
    super().__init__()
    self.setContentsMargins(0, 0, 0, 0)
    self.setSpacing(10)

    header = QVBoxLayout()
    header.setContentsMargins(0, 0, 10, 0)
    header.setSpacing(0)

    title_label = H2(globals.TITLE)
    header.addWidget(title_label)

    sub_text = SubText("Generate commands for Windows, MacOS, and Linux")
    header.addWidget(sub_text)

    server_icon = QSvgWidget("assets/server.svg")
    server_icon.setFixedSize(24, 24)

    self.addWidget(server_icon, 0, Qt.AlignmentFlag.AlignVCenter)
    self.addLayout(header, 1)

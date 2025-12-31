from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QPushButton
from PyQt6.QtCore import Qt
from components.Settings import Settings
import globals
from utils.svg import ColorIcon, ColorSvgWidget
from utils.ui import H2, Hr, SubText


class Header(QWidget):
  def __init__(self):
    super().__init__()

    self.settings_dialog = None

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

    text_color = self.palette().text().color().name()
    server_icon = ColorSvgWidget(globals.resource_path("assets/server.svg"), text_color, size=24)

    self._h_layout.addWidget(server_icon, 0, Qt.AlignmentFlag.AlignVCenter)
    self._h_layout.addLayout(header, 1)

    settings_button = QPushButton()
    settings_button.setFlat(True)

    settings_icon = ColorIcon(globals.resource_path("assets/settings.svg"), text_color)
    settings_button.setIcon(settings_icon)

    settings_button.setStyleSheet("padding: 6px 4px;")
    settings_button.clicked.connect(self.settings_handler)

    self._h_layout.addWidget(settings_button, 0, Qt.AlignmentFlag.AlignVCenter)

    self._layout.addLayout(self._h_layout)
    self._layout.addWidget(Hr())
    self.setLayout(self._layout)

    self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

  def settings_handler(self):
    if self.settings_dialog is None:
      self.settings_dialog = Settings()

    self.settings_dialog.exec()

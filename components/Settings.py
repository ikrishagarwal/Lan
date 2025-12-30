from pathlib import Path
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QFileDialog
from PyQt6.QtCore import QSettings, QUrl
from PyQt6.QtGui import QDesktopServices
from utils.ui import H1, H4
from os import path

default_path = path.abspath(path.join(path.expanduser("~"), ".config", "lan_config.json"))


class Settings(QDialog):
  def __init__(self):
    super().__init__()

    self.setWindowTitle("Settings")
    self.setMinimumSize(400, 400)
    self.setModal(True)

    self.settings = QSettings()

    self._layout = QVBoxLayout()

    label = H1("Settings")
    label.setContentsMargins(1, 1, 1, 12)
    self._layout.addWidget(label)

    config_link_label = H4("Config File Location:")
    self._layout.addWidget(config_link_label)

    self.config_link_input = QLineEdit()
    self.config_link_input.setText(
      self.settings.value("config_path", default_path))
    self.config_link_input.setReadOnly(True)

    browse_button = QPushButton("Change")
    browse_button.setFlat(True)
    browse_button.setFixedWidth(80)
    browse_button.setStyleSheet("padding: 6px 8px;")

    browse_button.clicked.connect(self.change_config_handler)

    config_input_layout = QHBoxLayout()
    config_input_layout.addWidget(self.config_link_input, 1)
    config_input_layout.addWidget(browse_button, 0)

    self._layout.addLayout(config_input_layout)

    self._layout.addStretch()

    # save_button = QPushButton("Save")
    # save_button.setFlat(True)
    # save_button.setFixedWidth(100)
    # save_button.setStyleSheet("""
    #   QPushButton {
    #     outline: none;
    #     font-size: 12px;
    #     font-weight: semibold;
    #     padding: 6px 12px;
    #   }
    # """)

    open_json_button = QPushButton("Open Config")
    open_json_button.setFlat(True)
    open_json_button.setFixedWidth(100)
    open_json_button.setStyleSheet("""
      QPushButton {
        font-size: 12px;
        font-weight: semibold;
        padding: 6px 12px;
      }
    """)

    open_json_button.clicked.connect(self.open_json_handler)

    button_layout = QHBoxLayout()
    button_layout.addStretch()

    # button_layout.addWidget(save_button, 0)
    button_layout.addWidget(open_json_button, 0)
    self._layout.addLayout(button_layout)

    self.setLayout(self._layout)

  def open_json_handler(self):
    config_path = self.settings.value("config_path", default_path)
    file_url = QUrl.fromLocalFile(config_path)
    QDesktopServices.openUrl(file_url)

  def change_config_handler(self):
    current_path = path.dirname(self.settings.value(
      "config_path", path.expanduser("~")))

    folder_name = QFileDialog.getExistingDirectory(
      self, "Select Config Folder", current_path)
    if folder_name:
      new_config_path = path.join(Path(folder_name), "lan_config.json")
      self.settings.setValue("config_path", new_config_path)
      self.config_link_input.setText(new_config_path)

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QHBoxLayout, QPushButton, QSizePolicy
from PyQt6.QtCore import pyqtSignal as Signal
from utils.ui import H2


class Main(QWidget):
  save = Signal(object)

  def __init__(self):
    super().__init__()

    layout = QVBoxLayout()
    self._layout = layout
    label = H2("Configuration")
    label.setObjectName("H2")
    label.setStyleSheet("""
      QLabel#H2 {
        font-weight: bold;
      }
    """)

    layout.addWidget(label)

    form_layout = QFormLayout()
    self.name = QLineEdit()
    self.ip = QLineEdit()
    self.subnet = QLineEdit()
    self.gateway = QLineEdit()
    self.dns_primary = QLineEdit()
    self.dns_secondary = QLineEdit()

    form_layout.addRow("Config Name:", self.name)
    form_layout.addRow("IP Address:", self.ip)
    form_layout.addRow("Subnet Mask:", self.subnet)
    form_layout.addRow("Gateway:", self.gateway)
    form_layout.addRow("Primary DNS:", self.dns_primary)
    form_layout.addRow("Secondary DNS:", self.dns_secondary)

    button_widget = QWidget()
    button_layout = QHBoxLayout()
    save_button = QPushButton("Save")
    apply_button = QPushButton("Apply")

    save_button.clicked.connect(self._save_handler)

    button_layout.addWidget(save_button)
    button_layout.addWidget(apply_button)

    button_widget.setLayout(button_layout)
    form_layout.addWidget(button_widget)

    layout.addLayout(form_layout, 1)

    self.setLayout(layout)

  def _save_handler(self):
    config_data = {
      "name": self.name.text(),
      "ip": self.ip.text(),
      "subnet": self.subnet.text(),
      "gateway": self.gateway.text(),
      "dns_primary": self.dns_primary.text(),
      "dns_secondary": self.dns_secondary.text(),
    }

    self.save.emit(config_data)

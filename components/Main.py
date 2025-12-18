from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QHBoxLayout, QPushButton
from utils.ui import H2


class Main(QWidget):
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
    self.ip = QLineEdit()
    self.subnet = QLineEdit()
    self.gateway = QLineEdit()
    self.dns_primary = QLineEdit()
    self.dns_secondary = QLineEdit()

    form_layout.addRow("IP Address:", self.ip)
    form_layout.addRow("Subnet Mask:", self.subnet)
    form_layout.addRow("Gateway:", self.gateway)
    form_layout.addRow("Primary DNS:", self.dns_primary)
    form_layout.addRow("Secondary DNS:", self.dns_secondary)

    button_widget = QWidget()
    button_layout = QHBoxLayout()
    save_button = QPushButton("Save")
    apply_button = QPushButton("Apply")

    button_layout.addWidget(save_button)
    button_layout.addWidget(apply_button)

    button_widget.setLayout(button_layout)
    form_layout.addWidget(button_widget)

    layout.addLayout(form_layout)

    self.setLayout(layout)

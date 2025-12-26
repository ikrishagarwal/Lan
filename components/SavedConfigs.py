from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, pyqtSignal as Signal
from PyQt6.QtGui import QPalette, QColor
from utils.ui import H3


class SideBar(QWidget):
  selection = Signal(str)

  def __init__(self):
    super().__init__()

    layout = QVBoxLayout()
    heading = H3("Saved Configs")
    heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
    heading.setStyleSheet("""
      QLabel {
        margin-bottom: 0px;
        margin-top: 15px;
        font-weight: bold;
        border-radius: 2px;
      }
    """)
    layout.addWidget(heading, 0)

    self._layout = QVBoxLayout()
    self._layout.setContentsMargins(10, 10, 10, 10)
    # self._layout.setContentsMargins(0, 0, 0, 0)

    list_widget = QWidget()
    list_widget.setLayout(self._layout)
    # layout.addLayout(self._layout, 1)
    layout.addWidget(list_widget, 1)
    self.setLayout(layout)

    self.clear()
    self.set_empty_message()

  def populate(self, configs: dict[str, str]):
    self.clear()

    if not configs or len(configs.keys()) == 0:
      self.set_empty_message()
      return

    for id, name in configs.items():
      button = QPushButton(name, self)
      button.setStyleSheet("""
        QPushButton {
          margin: 0;
          border: 0;
          padding: 5px;
          border-radius: 4px;
        }
        QPushButton:hover {
          background-color: #333;
        }
      """)
      button.clicked.connect(
        lambda _, btn_id=id: self.selection.emit(btn_id))
      button.setFlat(True)

      self._layout.addWidget(button, 0)

    self._layout.addStretch(1)

  def clear(self):
    while self._layout.count():
      child = self._layout.takeAt(0)
      if child and child.widget():
        child.widget().deleteLater()  # type: ignore

  def set_empty_message(self):
    text = QLabel("No saved configurations.")
    palette = text.palette()
    palette.setColor(
      QPalette.ColorRole.WindowText, QColor(Qt.GlobalColor.gray)
    )
    text.setPalette(palette)
    self._layout.addWidget(text)

  def reset(self):
    self.clear()
    self.set_empty_message()

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
from utils.adapter import AdapterLoader
from utils.ui import Hr, VerticalBar
from components.Header import Header
from components.SavedConfigs import SideBar
import globals


class MainWindow(QWidget):
  active_adapter: str | None = None

  def __init__(self):
    super().__init__()

    self.setWindowTitle(globals.TITLE)
    self.setMinimumWidth(560)

    self.network_adapter = AdapterLoader()
    self.network_adapter.finished.connect(self.refresh_adapters)

    v = QVBoxLayout()
    v.setContentsMargins(10, 10, 10, 10)

    v.addLayout(Header())
    v.addWidget(Hr())

    row = QHBoxLayout()
    row.addWidget(QLabel("Adapter:"))

    self.adapter_combo = QComboBox()

    row.addWidget(self.adapter_combo, 1)

    refresh = QPushButton("Refresh")
    refresh.clicked.connect(self.refresh_adapter_menu)

    row.addWidget(refresh)
    v.addLayout(row)

    body_layout = QHBoxLayout()
    self.sidebar = SideBar()

    self.sidebar.populate({
      "config1": "Home Network",
      "config2": "Office Network",
      "config3": "Mobile HotSpot"
    })

    self.sidebar.selection.connect(lambda id: print(f"Selected config: {id}"))

    body_layout.addWidget(self.sidebar)
    body_layout.addWidget(VerticalBar())
    # Placeholder for main content
    body_layout.addWidget(QLabel("Main Content"), 1)

    v.addLayout(body_layout, 1)

    self.setLayout(v)
    self.refresh_adapter_menu()
    self.adapter_combo.currentIndexChanged.connect(self.current_adapter)

  def refresh_adapter_menu(self):
    self.adapter_combo.clear()
    self.adapter_combo.addItem("Loading adapters...")
    self.adapter_combo.setEnabled(False)
    self.adapter_combo.blockSignals(True)

    self.network_adapter.refresh()

  def refresh_adapters(self, adapters=None):
    self.adapter_combo.blockSignals(False)
    self.adapter_combo.clear()

    if not adapters:
      self.adapter_combo.addItem("No adapters found")
    else:
      self.adapter_combo.addItems(
        adapter for adapter in adapters if "ethernet" in adapter.lower())
      self.adapter_combo.setEnabled(True)

  def current_adapter(self):
    cur = self.adapter_combo.currentText()
    self.active_adapter = None if cur == "No adapters found" else cur

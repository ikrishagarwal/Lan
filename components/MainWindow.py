from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
from utils.adapter import AdapterLoader
from utils.ui import Hr, VerticalBar
from components.Header import Header
from components.SavedConfigs import SideBar
from components.Main import Main
from components.Loader import Loader
import globals


class MainWindow(QWidget):
  active_adapter: str | None = None

  def __init__(self):
    super().__init__()

    self.setWindowTitle(globals.TITLE)
    self.setMinimumWidth(560)

    self.network_adapter = AdapterLoader()
    self.network_adapter.finished.connect(self.refresh_adapters)

    # states
    self.is_loading = False

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

    self.loader_widget = Loader()
    v.addWidget(self.loader_widget)

    self.is_loading = True

    body_layout = QHBoxLayout()
    self.sidebar = SideBar()

    # self.sidebar.populate({
    #   "config1": "Home Network",
    #   "config2": "Office Network",
    #   "config3": "Mobile HotSpot"
    # })

    # TODO: also fix this
    self.sidebar.selection.connect(lambda id: print(f"Selected config: {id}"))

    body_layout.addWidget(self.sidebar)
    body_layout.addWidget(VerticalBar())
    body_layout.addWidget(Main(), 1)

    self.body_layout = body_layout
    # v.addLayout(body_layout, 1)

    self.setLayout(v)
    self._layout = v
    self.refresh_adapter_menu()
    self.adapter_combo.currentIndexChanged.connect(self.current_adapter)

  def refresh_adapter_menu(self):
    self.adapter_combo.clear()
    self.adapter_combo.addItem("Loading adapters...")
    self.adapter_combo.setEnabled(False)
    self.adapter_combo.blockSignals(True)

    if not self.is_loading:
      self.is_loading = True
      self._layout.removeItem(self.body_layout)
      self._layout.addWidget(self.loader_widget, 1)

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

    # TODO: if cur is None then show error

    if self.is_loading:
      self.is_loading = False
      self._layout.removeWidget(self.loader_widget)
      self.loader_widget.setParent(None)
      self._layout.addLayout(self.body_layout, 1)
      self.sidebar.reset()

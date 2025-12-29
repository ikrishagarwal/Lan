from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QSizePolicy
from utils.config_manager import ConfigManager
from utils.adapter import AdapterLoader
from utils.ui import VerticalBar
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

    # TODO: change it to use ~/.config/lan_config.json
    self.config = ConfigManager(filename="config/settings.json")

    # states
    self.is_loading = False

    v = QVBoxLayout()
    self._layout = v
    v.setContentsMargins(10, 10, 10, 10)

    v.addWidget(Header(), 0)

    row = QHBoxLayout()
    row.addWidget(QLabel("Adapter:"))

    self.adapter_combo = QComboBox()

    row.addWidget(self.adapter_combo, 1)

    refresh = QPushButton("Refresh")
    refresh.clicked.connect(self.refresh_adapter_menu)

    row.addWidget(refresh)
    v.addLayout(row)

    self.loader_widget = Loader()
    v.addWidget(self.loader_widget, 1)

    self.is_loading = True

    body_layout = QHBoxLayout()
    self.sidebar = SideBar()

    # TODO: populate saved configs on selection change
    self.sidebar.selection.connect(lambda id: print(f"Selected config: {id}"))

    body_layout.addWidget(self.sidebar)
    body_layout.addWidget(VerticalBar())

    main_body_widget = Main()
    main_body_widget.save.connect(self.save_handler)

    body_layout.addWidget(main_body_widget, 1)

    self.body_widget = QWidget()
    self.body_widget.setLayout(body_layout)
    self.body_widget.setVisible(False)

    v.addWidget(self.body_widget, 1)

    v.addStretch(0)
    self.setSizePolicy(QSizePolicy.Policy.Preferred,
                       QSizePolicy.Policy.Preferred)

    self.setLayout(v)

    self.refresh_adapter_menu()
    self.adapter_combo.currentIndexChanged.connect(self.current_adapter)

  def refresh_adapter_menu(self):
    self.adapter_combo.clear()
    self.adapter_combo.addItem("Loading adapters...")
    self.adapter_combo.setEnabled(False)
    self.adapter_combo.blockSignals(True)

    if not self.is_loading:
      self.is_loading = True
      self.loader_widget.setVisible(True)
      self.body_widget.setVisible(False)
      self.sidebar.reset()

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

    print(f"Current adapter: {self.active_adapter}")

    # TODO: if cur is None then show error
    # For now, it's gonna be just stuck in loading screen if it can't find any adapters
    if not self.active_adapter:
      return

    if self.is_loading:
      self.is_loading = False

      self.loader_widget.setVisible(False)
      self.body_widget.setVisible(True)

      self.populate_saved_configs()

  def populate_saved_configs(self):
    if not self.active_adapter:
      print("No active adapter selected. Cannot populate saved configurations.")
      return

    self.sidebar.reset()

    adapter_saved_configs = self.config.get(self.active_adapter) or {}
    saved_config_data = {}

    for key in adapter_saved_configs.keys():
      saved_config_data[key] = key[0:15] + \
        ("..." if len(key) > 15 else "")

    if saved_config_data:
      self.sidebar.populate(saved_config_data)

  def save_handler(self, config_data: dict):
    if not self.active_adapter:
      print("No active adapter selected. Cannot save configuration.")
      return

    saved_data = self.config.get(self.active_adapter) or {}

    data_to_save = config_data.copy()
    data_to_save.pop("name")

    saved_data[config_data["name"]] = data_to_save

    self.config.set(self.active_adapter, saved_data)
    self.populate_saved_configs()

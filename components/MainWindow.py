from logging import config
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QSizePolicy
from components.NoAdapter import NoAdapter
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

    self.config = ConfigManager()

    # we start with a loading state
    self.is_loading = True

    v = QVBoxLayout()
    self._layout = v
    v.setContentsMargins(10, 10, 10, 10)

    v.addWidget(Header(), 0)

    row = QHBoxLayout()

    self.adapter_combo = QComboBox()

    row.addWidget(self.adapter_combo, 1)

    refresh = QPushButton("Refresh")
    refresh.clicked.connect(self.refresh_adapter_menu)

    row.addWidget(refresh)
    v.addLayout(row)

    self.loader_widget = Loader()
    v.addWidget(self.loader_widget, 1)

    self.no_adapter_widget = NoAdapter()
    self.no_adapter_widget.setVisible(False)
    self._layout.addWidget(self.no_adapter_widget, 1)

    body_layout = QHBoxLayout()
    self.sidebar = SideBar()

    self.sidebar.selection.connect(self.saved_config_select_handler)
    self.sidebar.delete.connect(self.delete_saved_config_handler)

    body_layout.addWidget(self.sidebar)
    body_layout.addWidget(VerticalBar())

    self.main_body_widget = Main()
    self.main_body_widget.save.connect(self.save_handler)

    body_layout.addWidget(self.main_body_widget, 1)

    self.body_widget = QWidget()
    self.body_widget.setLayout(body_layout)
    self.body_widget.setVisible(False)

    v.addWidget(self.body_widget, 1)

    v.addStretch(0)
    self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

    self.setLayout(v)

    self.refresh_adapter_menu()
    self.adapter_combo.currentIndexChanged.connect(self.current_adapter)

  def refresh_adapter_menu(self):
    self.adapter_combo.clear()
    self.adapter_combo.addItem("Fetching adapters...")
    self.adapter_combo.setEnabled(False)
    self.adapter_combo.blockSignals(True)

    if not self.is_loading:
      self.is_loading = True
      self.no_adapter_widget.setVisible(False)
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
      # self.adapter_combo.addItems(adapters)
      self.adapter_combo.setEnabled(True)

  def current_adapter(self):
    cur = self.adapter_combo.currentText()
    self.active_adapter = None if cur == "No adapters found" else cur

    if not self.active_adapter:
      self.loader_widget.setVisible(False)
      self.body_widget.setVisible(False)

      self.no_adapter_widget.setVisible(True)
      return

    if self.is_loading:
      self.is_loading = False

      self.no_adapter_widget.setVisible(False)
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
      saved_config_data[key] = key[0:15] + ("..." if len(key) > 15 else "")

    if saved_config_data:
      self.sidebar.populate(saved_config_data)

  def saved_config_select_handler(self, config_name: str):
    if not self.active_adapter:
      print("No active adapter selected. Cannot select configuration.")
      return

    if not config_name:
      print("No configuration name provided.")
      return

    adapter_saved_configs = self.config.get(self.active_adapter) or {}
    config_data = adapter_saved_configs.get(config_name)

    if not config_data:
      print(f"Configuration '{config_name}' not found for adapter '{self.active_adapter}'.")
      return

    self.main_body_widget.populate(config_name, config_data)

  def delete_saved_config_handler(self, config_name: str):
    if not self.active_adapter:
      print("No active adapter selected. Cannot delete configuration.")
      return

    if not config_name:
      print("No configuration name provided.")
      return

    adapter_saved_configs = self.config.get(self.active_adapter) or {}

    if config_name not in adapter_saved_configs:
      print(f"Configuration '{config_name}' not found for adapter '{self.active_adapter}'.")
      return

    adapter_saved_configs.pop(config_name)
    self.config.set(self.active_adapter, adapter_saved_configs)

    self.populate_saved_configs()

  def save_handler(self, config_data: dict):
    if not self.active_adapter:
      print("No active adapter selected. Cannot save configuration.")
      return

    saved_data = self.config.get(self.active_adapter) or {}

    config_to_save = config_data.copy()
    config_to_save.pop("name")
    saved_data[config_data["name"]] = config_to_save

    self.config.set(self.active_adapter, saved_data)
    self.populate_saved_configs()

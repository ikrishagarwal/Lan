from PyQt6.QtCore import QSettings
import json
import os


class ConfigManager:
  def __init__(self, filename=None) -> None:
    settings = QSettings()

    default_path = os.path.join(os.path.expanduser("~"), ".config", "lan_config.json")
    self.filepath = filename if filename else settings.value("config_paths", default_path)

    self.config = {}
    self.load()

  def load(self) -> None:
    if os.path.exists(self.filepath):
      try:
        with open(self.filepath, "r") as f:
          self.config = json.load(f)
      except json.JSONDecodeError:
        # config file is corrupted
        self.config = {}
    else:
      self.config = {}

  def save(self) -> None:
    os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

    with open(self.filepath, "w") as f:
      json.dump(self.config, f, indent=2)

  def get(self, key: str):
    return self.config.get(key)

  def set(self, key: str, value) -> None:
    self.config[key] = value
    self.save()

  def as_dict(self) -> dict:
    return self.config

  def load_data(self, data: dict) -> None:
    self.config = data
    self.save()

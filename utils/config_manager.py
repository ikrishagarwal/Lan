import json
import os


class ConfigManager:
  def __init__(self, filename) -> None:
    base_path = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.join(base_path, "../.."))
    self.filepath = os.path.join(project_root, filename)

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

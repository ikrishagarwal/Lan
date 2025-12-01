import subprocess
from typing import List


def run(cmd: List[str], check=True, capture_output=True, text=True) -> subprocess.CompletedProcess:
  return subprocess.run(cmd, check=check, capture_output=capture_output, text=text)

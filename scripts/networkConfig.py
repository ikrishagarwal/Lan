import platform
import shutil
from typing import List
from scripts.utils import run


def list_adapters() -> List[str]:
  os_name = platform.system()
  if os_name == "Windows":
    cmd = ["powershell", "-Command",
           "Get-NetAdapter | Where-Object {$_.Status -ne 'Disabled'} | Select-Object -ExpandProperty Name"]
    try:
      cp = run(cmd)
      names = [line.strip() for line in cp.stdout.splitlines() if line.strip()]
      return names or []
    except Exception:
      try:
        cp = run(["netsh", "interface", "show", "interface"])
        lines = cp.stdout.splitlines()
        names = []
        for line in lines:
          if line and not line.startswith("---") and not line.lower().startswith("admin"):
            parts = line.split()
            if len(parts) >= 4:
              names.append(" ".join(parts[3:]))
        return names
      except Exception:
        return []
  elif os_name == "Darwin":
    try:
      cp = run(["networksetup", "-listallnetworkservices"])
      names = [ln.strip() for ln in cp.stdout.splitlines()
               if ln.strip() and not ln.startswith("An asterisk")]
      return names
    except Exception:
      return []
  elif os_name == "Linux":
    if shutil.which("nmcli"):
      try:
        cp = run(["nmcli", "-t", "-f", "NAME,TYPE", "con", "show"])
        names = []
        for line in cp.stdout.splitlines():
          if not line.strip():
            continue
          name, ctype = (line.split(":", 1) + [""])[:2]
          if ctype in ("ethernet", "wifi"):
            names.append(name)
        return names
      except Exception:
        return []
    return []
  else:
    return []

import subprocess
import shutil
import platform
import ipaddress
from typing import List, Tuple


def run(cmd: List[str], check=True, capture_output=True, text=True) -> subprocess.CompletedProcess:
  return subprocess.run(cmd, check=check, capture_output=capture_output, text=text)


def run_elevated(base_cmd: List[str]) -> Tuple[bool, str]:
  os_name = platform.system()

  try:
    if os_name == "Windows":
      cmd_str = " ".join(base_cmd)
      safe_cmd = cmd_str.replace('"', '\\"')

      wrapper = [
          "powershell",
          "-NoProfile",
          "-Command",
          f"Start-Process powershell -Verb RunAs -Wait -ArgumentList '-NoExit -NoProfile -ExecutionPolicy Bypass -Command \"{safe_cmd}; exit $LASTEXITCODE\"'"
      ]

      cp = subprocess.run(wrapper, capture_output=True, text=True)

      ok = (cp.returncode == 0)
      return ok, "OK" if ok else f"Command failed with code {cp.returncode}"

    else:
      if shutil.which("pkexec"):
        cmd = ["pkexec"] + base_cmd
      else:
        cmd = ["sudo"] + base_cmd

      cp = subprocess.run(cmd, capture_output=True, text=True)
      ok = (cp.returncode == 0)

      err_msg = cp.stderr.strip() if cp.stderr else f"Code {cp.returncode}"
      return ok, "OK" if ok else f"Command failed: {err_msg}"

  except Exception as e:
    return False, str(e)

# def run_elevated(base_cmd: List[str]) -> Tuple[bool, str]:
#   os_name = platform.system()
#   try:
#     if os_name == "Windows":
#       ps_cmd = ' '.join(escape_ps_arg(a) for a in base_cmd)
#       wrapper = [
#           "powershell", "-Command",
#           f"Start-Process powershell -Verb RunAs -ArgumentList '-NoProfile -ExecutionPolicy Bypass -Command {ps_cmd}; exit $LASTEXITCODE' -Wait"
#       ]
#       cp = subprocess.run(wrapper)
#       ok = (cp.returncode == 0)
#       return ok, "OK" if ok else f"Command failed with code {cp.returncode}"
#     else:
#       if shutil.which("pkexec"):
#         cmd = ["pkexec"] + base_cmd
#         cp = subprocess.run(cmd)
#         ok = (cp.returncode == 0)
#         return ok, "OK" if ok else f"Command failed with code {cp.returncode}"
#       else:
#         cmd = ["sudo"] + base_cmd
#         cp = subprocess.run(cmd)
#         ok = (cp.returncode == 0)
#         return ok, "OK" if ok else f"Command failed with code {cp.returncode}"


def escape_ps_arg(s: str) -> str:
  s = s.replace("'", "''")
  return f"'{s}'"


def is_valid_ipv4(addr: str) -> bool:
  try:
    ipaddress.IPv4Address(addr)
    return True
  except Exception:
    return False


def mask_to_prefix(mask: str) -> int:
  parts = mask.split(".")
  if len(parts) != 4:
    raise ValueError("Invalid subnet mask")
  return sum(bin(int(p)).count("1") for p in parts)


def extract_after(text: str, key: str) -> str:
  for line in text.splitlines():
    if key in line:
      return line.split(key, 1)[1].strip()
  return ""


def parse_kv_lines(s: str) -> dict:
  out = {}
  for line in s.splitlines():
    if "=" in line:
      k, v = line.split("=", 1)
      out[k.strip()] = v.strip()
  return out


def prefix_to_mask(prefix: int) -> str:
  if not (0 <= prefix <= 32):
    raise ValueError("Invalid prefix")
  bits = (1 << 32) - (1 << (32 - prefix))
  return ".".join(str((bits >> (24 - 8 * i)) & 0xFF) for i in range(4))

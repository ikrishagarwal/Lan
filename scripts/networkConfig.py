import base64
from typing import List, Optional, Tuple
import platform
import shutil
from typing import List, Tuple, Optional, Dict
from scripts.utils import run, run_elevated, is_valid_ipv4, mask_to_prefix, extract_after, parse_kv_lines, prefix_to_mask
import re


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


def apply_static_ipv4(adapter: str, ip: str, mask: str, gateway: str) -> Tuple[bool, str]:
  if not (is_valid_ipv4(ip) and is_valid_ipv4(gateway)):
    return False, "Invalid IPv4 or gateway."
  try:
    prefix = mask_to_prefix(mask)
  except Exception:
    return False, "Invalid subnet mask."
  os_name = platform.system()
  try:
    if os_name == "Windows":
      ps = f"""
$iface = "{adapter}"
$pref = {prefix}
$ip = "{ip}"
$gw = "{gateway}"
$existing = Get-NetIPAddress -InterfaceAlias $iface -AddressFamily IPv4 -ErrorAction SilentlyContinue | Select-Object -First 1
if ($existing) {{
  Set-NetIPAddress -InterfaceAlias $iface -IPAddress $ip -PrefixLength $pref -DefaultGateway $gw -ErrorAction Stop
}} else {{
  New-NetIPAddress -InterfaceAlias $iface -IPAddress $ip -PrefixLength $pref -DefaultGateway $gw -ErrorAction Stop
}}
"""
      return run_elevated(["powershell", "-Command", ps])
    elif os_name == "Darwin":
      return run_elevated(["networksetup", "-setmanual", adapter, ip, mask, gateway])
    elif os_name == "Linux":
      if not shutil.which("nmcli"):
        return False, "nmcli not found (NetworkManager required)."
      ok, msg = run_elevated(["nmcli", "con", "mod", adapter, "ipv4.method",
                             "manual", "ipv4.addresses", f"{ip}/{prefix}", "ipv4.gateway", gateway])
      if not ok:
        return ok, msg
      return run_elevated(["nmcli", "con", "up", adapter])
    else:
      return False, f"Unsupported OS: {os_name}"
  except Exception as e:
    return False, str(e)


def get_current_config(adapter: str) -> Dict[str, Optional[str]]:
  os_name = platform.system()
  result: Dict[str, Optional[str]] = {"mode": None, "ip": None, "mask": None, "gateway": None}
  try:
    if os_name == "Windows":
      ps = f"""
$ip = Get-NetIPAddress -InterfaceAlias "{adapter}" -AddressFamily IPv4 -ErrorAction SilentlyContinue | Sort-Object -Property PrefixLength -Descending | Select-Object -First 1
$dhcp = (Get-NetIPInterface -InterfaceAlias "{adapter}" -AddressFamily IPv4).Dhcp
if ($ip) {{
  $gw = (Get-NetRoute -InterfaceAlias "{adapter}" -DestinationPrefix "0.0.0.0/0" -ErrorAction SilentlyContinue | Select-Object -First 1).NextHop
  Write-Output "MODE=$dhcp"
  Write-Output "IP=$($ip.IPAddress)"
  Write-Output "PREFIX=$($ip.PrefixLength)"
  Write-Output "GW=$gw"
}} else {{
  Write-Output "MODE=$dhcp"
}}
"""
      cp = run(["powershell", "-Command", ps])
      data = parse_kv_lines(cp.stdout)
      mode = data.get("MODE", "")
      result["mode"] = "DHCP" if mode and mode.lower(
      ).startswith("enable") else "STATIC"
      ip = data.get("IP")
      if ip:
        result["ip"] = ip
        pref = data.get("PREFIX")
        if pref:
          try:
            result["mask"] = prefix_to_mask(int(pref))
          except Exception:
            pass
      gw = data.get("GW")
      if gw:
        result["gateway"] = gw

    elif os_name == "Darwin":
      cp = run(["networksetup", "-getinfo", adapter])
      text = cp.stdout
      ip = re.search(r"IP address:\s*([0-9.]+)", text)
      mask = re.search(r"Subnet mask:\s*([0-9.]+)", text)
      gw = re.search(r"Router:\s*([0-9.]+)", text)
      result["ip"] = ip.group(1) if ip else None
      result["mask"] = mask.group(1) if mask else None
      result["gateway"] = gw.group(1) if gw else None
      dhcp = re.search(r"DHCP Configuration", text, re.I) or (
        "DHCP" in text and "Manual" not in text)
      result["mode"] = "DHCP" if dhcp else "STATIC"

    elif os_name == "Linux":
      if shutil.which("nmcli"):
        cp = run(
          ["nmcli", "-f", "ipv4.method,ipv4.addresses,ipv4.gateway", "con", "show", adapter])
        text = cp.stdout
        method = extract_after(text, "ipv4.method:")
        addrs = extract_after(text, "ipv4.addresses:")
        gw = extract_after(text, "ipv4.gateway:")
        result["mode"] = "DHCP" if method.strip() == "auto" else "STATIC"
        if addrs:
          addr = addrs.split(",")[0].strip()
          if "/" in addr:
            ip, pref = addr.split("/", 1)
            result["ip"] = ip
            try:
              result["mask"] = prefix_to_mask(int(pref))
            except Exception:
              pass
          else:
            result["ip"] = addr
        if gw:
          result["gateway"] = gw.strip()
  except Exception:
    pass
  return result


def apply_dns(adapter: str, servers: Optional[List[str]], family="ipv4") -> Tuple[bool, str]:
  family = family.lower()
  os_name = platform.system()

  if servers is not None and len(servers) == 0:
    servers = None

  try:
    if os_name == "Windows":
      if servers:
        server_str = ",".join(servers)
        ps_cmd = (
            f"Set-DnsClientServerAddress -InterfaceAlias '{adapter}' "
            f"-AddressFamily {family.upper()} -ServerAddresses {server_str} -ErrorAction Stop"
        )
      else:
        ps_cmd = (
            f"Set-DnsClientServerAddress -InterfaceAlias '{adapter}' "
            f"-AddressFamily {family.upper()} -ResetServerAddresses -ErrorAction Stop"
        )

      return run_elevated(["powershell", "-Command", ps_cmd])

    elif os_name == "Darwin":
      args = servers if servers else ["empty"]
      return run_elevated(["networksetup", "-setdnsservers", adapter] + args)

    elif os_name == "Linux":
      if not shutil.which("nmcli"):
        return False, "nmcli not found (NetworkManager required)."

      ignore_auto_flag = f"{family}.ignore-auto-dns"
      dns_flag = f"{family}.dns"

      if servers:
        cmd = [
            "nmcli", "con", "mod", adapter,
            ignore_auto_flag, "yes",
            dns_flag, " ".join(servers)
        ]
      else:
        cmd = [
            "nmcli", "con", "mod", adapter,
            ignore_auto_flag, "no",
            dns_flag, ""
        ]

      ok, msg = run_elevated(cmd)
      if not ok:
        return False, f"Failed to modify connection: {msg}"

      return run_elevated(["nmcli", "device", "reapply", adapter])

    else:
      return False, f"Unsupported OS: {os_name}"

  except Exception as e:
    return False, f"Error applying DNS: {str(e)}"


def get_current_dns(adapter: str, family="ipv4") -> List[str]:
  family = (family or "ipv4").lower()
  os_name = platform.system()
  try:
    if os_name == "Windows":
      fam = "IPv6" if family == "ipv6" else "IPv4"
      ps = f"""
$iface = \"{adapter}\"
$fam = \"{fam}\"
$addrs = (Get-DnsClientServerAddress -InterfaceAlias $iface -AddressFamily $fam -ErrorAction SilentlyContinue).ServerAddresses
if ($addrs) {{
  $addrs | ForEach-Object {{ Write-Output $_ }}
}}
"""
      cp = run(["powershell", "-Command", ps])
      servers = [ln.strip() for ln in cp.stdout.splitlines() if ln.strip()]
      return servers[:2]

    if os_name == "Darwin":
      cp = run(["networksetup", "-getdnsservers", adapter])
      lines = [ln.strip() for ln in cp.stdout.splitlines() if ln.strip()]
      # When no DNS is set, macOS prints a human sentence.
      if any("aren't any dns servers" in ln.lower() for ln in lines):
        return []
      return lines[:2]

    if os_name == "Linux":
      if not shutil.which("nmcli"):
        return []
      field = "ipv6.dns" if family == "ipv6" else "ipv4.dns"
      cp = run(["nmcli", "-f", field, "con", "show", adapter])
      text = cp.stdout
      raw = extract_after(text, f"{field}:")
      if not raw:
        return []
      servers = [s for s in re.split(r"[\s,]+", raw.strip()) if s]
      return servers[:2]

  except Exception:
    return []

  return []

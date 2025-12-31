# Static IP Configurator

A PyQt6 desktop app to view, edit, apply, and save Ethernet adapter network configurations.

The UI lets you:

- Pick an Ethernet adapter
- See current IPv4 settings (IP, subnet mask, gateway)
- See current DNS settings (primary and secondary)
- Apply IPv4 + DNS changes
- Save per-adapter configurations to a JSON file and re-apply them later

## Supported Platforms

- Windows: uses `netsh` / PowerShell networking cmdlets
- macOS: uses `networksetup`
- Linux: uses `nmcli` (NetworkManager)

> NOTE: It's only tested on Windows while it's development phase, so if you find any issues, feel feel to report them and/or create a PR.

## How Saved Configurations Work

- Saved configs are stored as JSON and scoped by adapter name.
- Default config file location is `~/.config/lan_config.json`.
- You can change the config location from the Settings dialog.

## Notes

- Applying network configuration changes requires administrator/root privileges.
- On Linux, if `nmcli` is not available (or NetworkManager is not used), DNS/IP apply operations will not work.

## Requirements

- Python 3.10+ (recommended)
- PyQt6
- Windows: run the app normally, but applying changes will require elevation
- Linux: NetworkManager + `nmcli` (and elevation via `pkexec` or `sudo`)
- macOS: elevation is required to apply changes

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Run

From the project root:

```bash
python __main__.py
```

## Author

- [Krish](https://github.com/ikrishagarwal)

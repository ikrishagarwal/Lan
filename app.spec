# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Helper to collect data recursively while ignoring __pycache__
def collect_pkg_data(package_names):
    datas = []
    for package in package_names:
        if os.path.isfile(package):
            # It's a file (like globals.py)
            datas.append((package, '.'))
            continue
            
        for root, dirs, files in os.walk(package):
            if '__pycache__' in dirs:
                dirs.remove('__pycache__')
            
            for f in files:
                if f.endswith('.pyc'):
                    continue
                source = os.path.join(root, f)
                # Keep directory structure relative to the project root
                dest = os.path.dirname(source)
                datas.append((source, dest))
    return datas

# directories/files to include
my_datas = collect_pkg_data(['assets', 'components', 'scripts', 'utils', 'globals.py'])

a = Analysis(
    ['__main__.py'],
    pathex=[],
    binaries=[],
    datas=my_datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe_name = 'LanConfig'
icon_path = os.path.join('assets', 'lan.ico')

# Platform specific adjustments
if sys.platform == 'win32':
    exe_name += '.exe'
# For Mac, we might need a Bundle, but creating a one-file/one-dir exec is the base.
# .app construction happens with BUNDLE (optional, but good for Mac opt).

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=exe_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path
)

# Optional: Bundle for macOS
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='LanConfig.app',
        icon=icon_path, # PyInstaller might want .icns here, but .ico is sometimes accepted or ignored
        bundle_identifier='dev.ikrish.lanapp'
    )

# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import shutil
from pathlib import Path

# Überprüfe, ob der resources/pdfium Ordner existiert
current_dir = os.getcwd()
pdfium_resource_dir = os.path.join(current_dir, "resources", "pdfium")

if not os.path.exists(pdfium_resource_dir):
    print("WARNUNG: resources/pdfium Verzeichnis nicht gefunden!")
    print("Bitte führen Sie erst extract_pdfium.py aus, um die Binärdateien zu extrahieren.")
    print("Die EXE-Datei wird trotzdem erstellt, aber die PDFium-Binärdateien werden nicht enthalten sein.")

block_cipher = None

# Erstelle die initiale Datenliste
initial_datas = [
    ('resources/Tesseract-OCR/*', 'resources/Tesseract-OCR'),
    ('resources/Tesseract-OCR/tessdata/*', 'resources/Tesseract-OCR/tessdata'),
]

# Füge PDFium-Binärdateien hinzu, wenn sie im resources-Ordner vorhanden sind
# Strategie: pdfium.dll als BINARY (landet im _internal Ordner) + andere DLLs als DATA
pdfium_dll_path = None
if os.path.exists(pdfium_resource_dir):
    pdfium_dll_path = os.path.join(pdfium_resource_dir, 'pdfium.dll')
    
    # Alle anderen DLLs (außer pdfium.dll) ins resources/pdfium Verzeichnis als DATA
    for root, dirs, files in os.walk(pdfium_resource_dir):
        for file in files:
            if file.endswith(('.dll', '.so', '.dylib', '.pyd')) and file != 'pdfium.dll':
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, pdfium_resource_dir)
                # Format: (src_path, dest_path) - dest_path muss vollständig sein
                if os.path.dirname(rel_path) == '.':
                    # Datei liegt direkt im pdfium-Ordner
                    dest_path = os.path.join('resources', 'pdfium', file).replace('\\', '/')
                else:
                    # Datei liegt in einem Unterordner - behalte die Struktur bei
                    dest_path = os.path.join('resources', 'pdfium', rel_path).replace('\\', '/')
                initial_datas.append((file_path, dest_path))
    
    print(f"PDFium-Binärdateien (außer pdfium.dll) aus {pdfium_resource_dir} wurden als DATA hinzugefügt.")

a = Analysis(
    ['pdf_ocr_gui.py'],
    pathex=[],
    binaries=[],
    datas=initial_datas,
    hiddenimports=['pypdfium2'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Füge pdfium.dll als BINARY hinzu (wird dann im _internal Ordner landen, wo PyInstaller sie findet)
# WICHTIG: DLLs müssen als BINARY eingebunden werden, damit sie zur Laufzeit gefunden werden!
if pdfium_dll_path and os.path.exists(pdfium_dll_path):
    # Format für binaries: (dest_name, src_name, typecode)
    # dest_name = Name der Datei im Zielverzeichnis
    # src_name = Quellpfad der Datei
    # typecode = 'BINARY'
    a.binaries += [('pdfium.dll', pdfium_dll_path, 'BINARY')]
    print(f"pdfium.dll wird als BINARY eingebunden (landet im _internal Ordner): {pdfium_dll_path}")

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PDF_Scanner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PDF_Scanner',
) 
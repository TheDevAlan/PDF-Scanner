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

a = Analysis(
    ['pdf_ocr_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('resources/Tesseract-OCR/*', 'resources/Tesseract-OCR'),
        ('resources/Tesseract-OCR/tessdata/*', 'resources/Tesseract-OCR/tessdata'),
    ],
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

# Füge PDFium-Binärdateien hinzu, wenn sie im resources-Ordner vorhanden sind
if os.path.exists(pdfium_resource_dir):
    for root, dirs, files in os.walk(pdfium_resource_dir):
        for file in files:
            if file.endswith(('.dll', '.so', '.dylib', '.pyd')):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, current_dir)
                target_path = os.path.relpath(file_path, pdfium_resource_dir)
                a.datas += [(f'resources/pdfium/{target_path}', file_path, 'DATA')]
    print(f"PDFium-Binärdateien aus {pdfium_resource_dir} wurden zur Spec-Datei hinzugefügt.")

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
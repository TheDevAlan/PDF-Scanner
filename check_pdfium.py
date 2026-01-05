import os
import sys
import importlib.metadata
import pypdfium2 as pdfium

print("PDFium-Informationen:")
print("-" * 50)

# Versuche, die Version aus den Metadaten des Pakets zu bekommen
try:
    version = importlib.metadata.version("pypdfium2")
    print(f"Verwendetes Paket: pypdfium2 Version {version}")
except:
    print("Verwendetes Paket: pypdfium2 (Version konnte nicht ermittelt werden)")

# Überprüfe, welche Attribute bei pdfium verfügbar sind
available_attrs = []
for attr in dir(pdfium):
    if not attr.startswith('_'):
        available_attrs.append(attr)

print(f"Verfügbare Attribute im pdfium-Modul: {', '.join(available_attrs)}")

# Speicherort der Binärdateien
bin_dir = os.path.dirname(pdfium.__file__)
print(f"PDFium-Binärdateien Speicherort: {bin_dir}")

print("-" * 50)

# Versuche die enthaltenen DLLs aufzulisten
print("Enthaltene Binärdateien:")
found_binaries = False
for f in os.listdir(bin_dir):
    if f.endswith('.dll') or f.endswith('.so') or f.endswith('.dylib'):
        print(f"- {f}")
        found_binaries = True

if not found_binaries:
    print("Keine direkten Binärdateien im Paketverzeichnis gefunden.")
    print("Die Binärdateien könnten in Unterverzeichnissen oder als Python-Wheels verpackt sein.")

print("\nQuelle laut PyPI/GitHub:")
print("- GitHub: https://github.com/pypdfium2-team/pypdfium2")
print("- PDFium-Binaries kommen von: https://github.com/bblanchon/pdfium-binaries")
print("- Lizenz: BSD 3-Clause License")

# Zusätzliche Informationen zum Paket anzeigen
print("\nVerzeichnisstruktur des Pakets:")
for root, dirs, files in os.walk(bin_dir, topdown=True):
    for name in dirs:
        print(f"Verzeichnis: {os.path.join(root, name)}")
    
    for name in files:
        if name.endswith(('.dll', '.so', '.dylib', '.pyd')):
            print(f"Binärdatei: {os.path.join(root, name)}")
        elif name.endswith(('.py')):
            print(f"Python-Datei: {os.path.join(root, name)}")

if os.path.exists(pdfium_resource_dir):
    for root, dirs, files in os.walk(pdfium_resource_dir):
        for file in files:
            if file.endswith(('.dll', '.so', '.dylib', '.pyd')):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, current_dir)
                target_path = os.path.relpath(file_path, pdfium_resource_dir)
                a.datas += [(f'resources/pdfium/{target_path}', file_path, 'DATA')]

PDFIUM_PATH = os.path.join(BASE_PATH, "resources", "pdfium") 
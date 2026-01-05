import os
import sys
import shutil
import pypdfium2 as pdfium
import pypdfium2_raw  # Importiere das raw-Paket direkt

def main():
    """Extrahiert PDFium-Binärdateien in den resources/pdfium Ordner"""
    # Pfad zum pypdfium2_raw-Paket
    pdfium_raw_dir = os.path.dirname(pypdfium2_raw.__file__)
    
    # Zielordner für die Extraktion
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(current_dir, "resources", "pdfium")
    
    # Erstelle Zielordner, falls er nicht existiert
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"Ordner erstellt: {target_dir}")
    
    # Suche nach den Binärdateien und kopiere sie
    binaries_copied = 0
    
    # Suche direkt im pypdfium2_raw-Verzeichnis
    print(f"Suche in: {pdfium_raw_dir}")
    for filename in os.listdir(pdfium_raw_dir):
        if filename.endswith(('.dll', '.so', '.dylib', '.pyd')):
            src = os.path.join(pdfium_raw_dir, filename)
            dst = os.path.join(target_dir, filename)
            shutil.copy2(src, dst)
            binaries_copied += 1
            print(f"Kopiert: {filename}")
    
    # Rekursive Suche nach Binärdateien in Unterverzeichnissen
    for root, dirs, files in os.walk(pdfium_raw_dir):
        for filename in files:
            if filename.endswith(('.dll', '.so', '.dylib', '.pyd')):
                rel_dir = os.path.relpath(root, pdfium_raw_dir)
                if rel_dir != '.':  # Überspringe das Hauptverzeichnis, das bereits behandelt wurde
                    src = os.path.join(root, filename)
                    # Erstelle das Zielverzeichnis
                    target_subdir = os.path.join(target_dir, rel_dir)
                    if not os.path.exists(target_subdir):
                        os.makedirs(target_subdir)
                    dst = os.path.join(target_subdir, filename)
                    shutil.copy2(src, dst)
                    binaries_copied += 1
                    print(f"Kopiert: {os.path.join(rel_dir, filename)}")
    
    if binaries_copied == 0:
        print("Keine Binärdateien gefunden!")
    else:
        print(f"\nErfolgreich {binaries_copied} Binärdateien nach {target_dir} kopiert.")
        print("Diese Dateien werden nun vom Programm verwendet, wenn es als .exe ausgeführt wird.")

if __name__ == "__main__":
    main() 
# PDF Dokumenten-Scanner

Ein Programm zur automatischen Erkennung und Umbenennung von Prüfvermerken und Schlussbescheiden basierend auf OCR.

## Funktionen

- Erkennt Prüfvermerke und Schlussbescheide
- Extrahiert automatisch die Projekt-Nummer
- Benennt Dateien nach dem Schema: `[Projektnummer]_[Dokumenttyp].pdf`
- Benutzerfreundliche grafische Oberfläche
- Fortschrittsanzeige während der Verarbeitung
- Speichert umbenannte Dateien in einem datierten Ordner

## Installation

### Voraussetzungen

- Windows Betriebssystem
- Die ausführbare Datei enthält bereits alle notwendigen Komponenten

### Verwendung der .exe

1. Laden Sie die neueste Version aus dem [Releases]([https://github.com/IHR_USERNAME/PDF-Scanner/releases](https://github.com/TheDevAlan/PDF-Scanner/releases/tag/v1.0.0)) Bereich herunter
2. Entpacken Sie die ZIP-Datei
3. Starten Sie `PDF_Scanner.exe`
4. Wählen Sie PDF-Dateien über den "Dateien hinzufügen" Button
5. Klicken Sie auf "Start"

Die umbenannten Dateien werden im Download-Ordner in einem neuen Ordner mit dem aktuellen Datum gespeichert.

## Entwicklung

### Voraussetzungen

- Python 3.7 oder höher
- Tesseract OCR
- Poppler für Windows

### Installation für Entwickler

1. Repository klonen:
   ```
   git clone https://github.com/IHR_USERNAME/PDF-Scanner.git
   ```

2. Abhängigkeiten installieren:
   ```
   pip install -r requirements.txt
   ```

3. Programm starten:
   ```
   python pdf_ocr_gui.py
   ```

### .exe erstellen

```
pyinstaller PDF_Scanner.spec
```

## Lizenz

[MIT](LICENSE)

## Autor

Ihr Name/Organisation 

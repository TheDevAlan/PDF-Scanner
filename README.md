# PDF Dokumenten-Scanner

Ein Programm zur automatischen Erkennung und Umbenennung von Prüfvermerken und Schlussbescheiden mittels OCR-Technologie.

## Funktionen

- Automatische Erkennung von Prüfvermerken und Schlussbescheiden
- Extraktion der Projekt-Nummer
- Automatische Umbenennung nach dem Schema: `[Projektnummer]_[Dokumenttyp].pdf`
- Benutzerfreundliche grafische Oberfläche
- Fortschrittsanzeige
- Speicherung in datumsbezogenen Ordnern

## Installation

### Voraussetzungen

- Windows Betriebssystem
- Die ausführbare Datei enthält bereits alle notwendigen Komponenten

### Verwendung der .exe

1. Laden Sie die neueste Version aus dem [Releases](https://github.com/TheDevAlan/PDF-Scanner/releases) Bereich herunter
2. Entpacken Sie die ZIP-Datei
3. Starten Sie `PDF_Scanner.exe`
4. Wählen Sie PDF-Dateien über "Dateien hinzufügen"
5. Klicken Sie auf "Start"

Die umbenannten Dateien werden im Download-Ordner in einem neuen Ordner mit dem aktuellen Datum gespeichert (Format: `Prüfvermerke_YYYY-MM-DD`).

## Autor

Entwickelt von Alan Gawlik

---

# [EN] PDF Document Scanner

A Windows application that automatically processes, recognizes, and renames specific German document types (Audit Notes and Final Notices) using OCR technology.

## Key Features

- Automatic recognition of "Prüfvermerk" (Audit Notes) and "Schlussbescheid" (Final Notices)
- Project number extraction
- Automatic file renaming following the pattern: `[ProjectNumber]_[DocumentType].pdf`
- User-friendly GUI (in German)
- Progress tracking
- Date-based folder organization

## Installation

1. Download the latest release from the [Releases](https://github.com/TheDevAlan/PDF-Scanner/releases) page
2. Extract the ZIP file
3. Run `PDF_Scanner.exe`

Note: The application interface is in German as it is specifically designed for processing German documents.

## For Developers

### Prerequisites

- Python 3.7 or higher
- Required packages: see `requirements.txt`

### Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/TheDevAlan/PDF-Scanner.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python pdf_ocr_gui.py
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Developed by Alan Gawlik

## Acknowledgments

- Tesseract OCR for text recognition
- Poppler for PDF processing
- Python community for various libraries

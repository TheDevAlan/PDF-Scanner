# PDF Dokumenten-Scanner

Ein Programm zur automatischen Erkennung und Umbenennung von PDF-Dokumenten mittels OCR-Technologie.

## Funktionen

- Automatische Erkennung verschiedener Dokumenttypen:
  - Prüfvermerk
  - Schlussbescheid
  - Kursorische Prüfung
  - Anhörung
  - Widerrufsbescheid
  - Auswertung Sachbericht
  - Zwischennachweis
  - Beleganforderung
  - Archivierungsverfügung
  - Änderungsbescheid
  - Kurzantrag
  - Antrag
  - Förderzusage
  - Antragsprüfvermerk
  - Zuwendungsbescheid
  - Verwendungsnachweis
  - Mittelanforderung
  - Auszahlungsblatt
  - Erinnerungsschreiben
  - Mahnschreiben
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

Die umbenannten Dateien werden im Download-Ordner in einem neuen Ordner mit dem aktuellen Datum gespeichert (Format: `Dokumentenscans_YYYY-MM-DD`).

## Autor

Entwickelt von Alan Gawlik

---

# [EN] PDF Document Scanner

A Windows application that automatically processes, recognizes, and renames various German document types using OCR technology.

## Key Features

- Automatic recognition of multiple document types including:
  - Prüfvermerk (Audit Notes)
  - Schlussbescheid (Final Notices)
  - Kursorische Prüfung (Cursory Review)
  - Anhörung (Hearing)
  - Widerrufsbescheid (Revocation Notice)
  - Auswertung Sachbericht (Report Evaluation)
  - Zwischennachweis (Interim Proof)
  - Beleganforderung (Document Request)
  - Archivierungsverfügung (Archiving Order)
  - Änderungsbescheid (Amendment Notice)
  - Kurzantrag (Short Application)
  - Antrag (Application)
  - Förderzusage (Funding Commitment)
  - Antragsprüfvermerk (Application Audit Note)
  - Zuwendungsbescheid (Grant Notice)
  - Verwendungsnachweis (Proof of Use)
  - Mittelanforderung (Fund Request)
  - Auszahlungsblatt (Payment Sheet)
  - Erinnerungsschreiben (Reminder Letter)
  - Mahnschreiben (Dunning Letter)
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

4. Extract PDFium binaries (only required for development):
   ```bash
   python extract_pdfium.py
   ```

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert – siehe [LICENSE](LICENSE) Datei für Details.

### Verwendete Bibliotheken und Lizenzen

Dieses Programm verwendet Open-Source-Software mit den folgenden Lizenzen:

- **pypdfium2** - BSD-3-Clause, Apache-2.0, CC-BY-4.0, Fair Use & Drittanbieter-Lizenzen  
  - Copyright © 2014-2024 PDFium Authors  
  - Die vollständige Lizenz finden Sie unter: [PDFium Lizenz](https://github.com/pypdfium2-team/pypdfium2/tree/main/LICENSES)  
  - PDFium enthält zusätzlich Drittanbieter-Code unter verschiedenen Lizenzen, die unter `LicenseRef-PdfiumThirdParty.txt` dokumentiert sind.  

- **Tesseract OCR** - Apache 2.0  
  - Copyright © 2006-2024 Google Inc.  
  - Die vollständige Lizenz: [Tesseract OCR Lizenz](https://github.com/tesseract-ocr/tesseract/blob/main/LICENSE)  

Gemäß den Anforderungen der jeweiligen Lizenzen wird hiermit bestätigt, dass dieses Produkt Software enthält, die von den oben genannten Projekten entwickelt wurde.

## Acknowledgments

- Tesseract OCR for text recognition
- PDFium for PDF processing
- Python community for various libraries

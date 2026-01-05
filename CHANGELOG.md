# Changelog

## Version 1.4.0 (January 05, 2026)

### New Features
- **Additional Document Types**: Added automatic detection and renaming for the following document types:
  - Kursorische Prüfung
  - Anhörung
  - Widerrufsbescheid
  - Auswertung Sachbericht
  - Zwischennachweis
  - Archivierungsverfügung
  - Änderungsbescheid

### Behaviour Changes
- **Target Folder**: All renamed files are now stored in `~/Downloads/Dokumentenscans_YYYY-MM-DD` instead of `~/Downloads/Prüfvermerke_YYYY-MM-DD`.
- **UI Text**: Updated the description text in the main window to reflect the broader set of supported document types.

## Version 1.3.0 (March 06, 2025)

### Main Changes
- **Library Change**: Switched from pdf2image/Poppler to pypdfium2
- **License Compliance**: Improved open-source license compliance using PDFium (BSD-3-Clause License)
- **DPI-Awareness**: Improved display on high-resolution screens
- **UI Improvements**: Modern fonts and consistent layout

### New Features
- **Dynamic Window Size**: Better adaptation to different screen resolutions

### Technical Improvements
- **PDFium Integration**: Using the PDFium library for PDF rendering
- **Improved Build Scripts**: Automatic extraction of PDFium binaries
- **Resource Management**: Improved management of external resources

### Documentation
- Updated README with information about used libraries and their licenses
- Detailed developer documentation

## Version 1.2.0 (February 13, 2025)

### New Features
- **Document Request Support**: Added support for document requests ("Beleganforderungen")
- **Updated GUI Text**: Texts in the user interface updated accordingly
- **Automatic Detection**: Implemented automatic detection and renaming of document requests

## Version 1.1.0 (February 01, 2025)

### Main Changes
- **Bilingual Documentation**: Added English documentation alongside German
- **Code Documentation**: Improved code comments and documentation
- **Author Information**: Added detailed author information throughout the project
- **UI Language**: UI remains in German for local users

## Version 1.0.0 (Initial Release)

- First public version
- PDF to image conversion with pdf2image/Poppler
- OCR functionality with Tesseract
- Automatic detection and renaming of documents 
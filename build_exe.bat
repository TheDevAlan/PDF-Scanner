@echo off
echo ========================================
echo PDF Scanner - EXE Build Script
echo ========================================
echo.

echo Schritt 0: Lösche alte Build-Ordner...
if exist "dist" (
    echo Lösche dist-Ordner...
    rmdir /s /q "dist"
)
if exist "build" (
    echo Lösche build-Ordner...
    rmdir /s /q "build"
)
echo.

echo Schritt 1: Extrahiere PDFium-Binärdateien...
python extract_pdfium.py
if errorlevel 1 (
    echo FEHLER: PDFium-Extraktion fehlgeschlagen!
    pause
    exit /b 1
)
echo.

echo Schritt 2: Erstelle EXE-Datei mit PyInstaller...
pyinstaller PDF_Scanner.spec
if errorlevel 1 (
    echo FEHLER: PyInstaller-Build fehlgeschlagen!
    pause
    exit /b 1
)
echo.

echo ========================================
echo Build erfolgreich abgeschlossen!
echo ========================================
echo Die EXE-Datei befindet sich in: dist\PDF_Scanner\PDF_Scanner.exe
echo.
pause


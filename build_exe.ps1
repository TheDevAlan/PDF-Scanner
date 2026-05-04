Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PDF Scanner - EXE Build Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Schritt 0: Lösche alte Build-Ordner..." -ForegroundColor Yellow
if (Test-Path "dist") {
    Write-Host "Lösche dist-Ordner..." -ForegroundColor Gray
    Remove-Item -Path "dist" -Recurse -Force
}
if (Test-Path "build") {
    Write-Host "Lösche build-Ordner..." -ForegroundColor Gray
    Remove-Item -Path "build" -Recurse -Force
}
Write-Host ""

Write-Host "Schritt 1: Extrahiere PDFium-Binärdateien..." -ForegroundColor Yellow
python extract_pdfium.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "FEHLER: PDFium-Extraktion fehlgeschlagen!" -ForegroundColor Red
    Read-Host "Drücken Sie Enter zum Beenden"
    exit 1
}
Write-Host ""

Write-Host "Schritt 2: Erstelle EXE-Datei mit PyInstaller..." -ForegroundColor Yellow
pyinstaller PDF_Scanner.spec
if ($LASTEXITCODE -ne 0) {
    Write-Host "FEHLER: PyInstaller-Build fehlgeschlagen!" -ForegroundColor Red
    Read-Host "Drücken Sie Enter zum Beenden"
    exit 1
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "Build erfolgreich abgeschlossen!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "Die EXE-Datei befindet sich in: dist\PDF_Scanner\PDF_Scanner.exe" -ForegroundColor Green
Write-Host ""
Read-Host "Drücken Sie Enter zum Beenden"


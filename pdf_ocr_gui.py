import os
import sys
import shutil
import ctypes
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import pytesseract
from PIL import Image, ImageDraw
import re

# Aktiviere High-DPI-Unterstützung für Windows
if sys.platform.startswith('win'):
    # Füge DPI-Awareness hinzu, um Skalierungsprobleme zu vermeiden
    try:
        # Windows 8.1 und höher
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # PROCESS_SYSTEM_DPI_AWARE
    except Exception:
        try:
            # Windows 8.0 und niedriger
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

def get_base_path():
    """Determines the base path for resources, distinguishes between .exe and Python script"""
    if getattr(sys, 'frozen', False):
        # When running as .exe
        return os.path.dirname(sys.executable)
    else:
        # When running as script
        return os.path.dirname(os.path.abspath(__file__))

# Setze den Pfad für PDFium-Bibliotheken VOR dem Import von pypdfium2
BASE_PATH = get_base_path()
PDFIUM_PATH = os.path.join(BASE_PATH, "resources", "pdfium")

# Wenn wir als .exe ausgeführt werden und der PDFium-Ordner existiert, füge ihn zum Systempfad hinzu
if getattr(sys, 'frozen', False) and os.path.exists(PDFIUM_PATH):
    # Füge den Pfad zur PATH-Umgebungsvariable hinzu
    os.environ["PATH"] = PDFIUM_PATH + os.pathsep + os.environ.get("PATH", "")
    
    # Setze auch die spezifische Umgebungsvariable für pypdfium2
    os.environ["PYPDFIUM2_PDFIUM_LIBRARY"] = os.path.join(PDFIUM_PATH, "pdfium.dll")
    
    print(f"PDFium-Pfad gesetzt auf: {PDFIUM_PATH}")
    print(f"PYPDFIUM2_PDFIUM_LIBRARY: {os.environ.get('PYPDFIUM2_PDFIUM_LIBRARY')}")

# Erst NACH dem Setzen des Pfads importieren wir pypdfium2
import pypdfium2 as pdfium
import io

# Set resource paths
TESSERACT_PATH = os.path.join(BASE_PATH, "resources", "Tesseract-OCR", "tesseract.exe")

# Set environment variables
os.environ['TESSDATA_PREFIX'] = os.path.join(BASE_PATH, "resources", "Tesseract-OCR", "tessdata")

# Check if PDFium resources exist and set environment variables if needed
if os.path.exists(PDFIUM_PATH):
    # Add PDFium path to PATH environment variable
    os.environ["PATH"] = PDFIUM_PATH + os.pathsep + os.environ.get("PATH", "")
    print(f"PDFium-Binärdateien gefunden in: {PDFIUM_PATH}")
else:
    print("PDFium-Binärdateien nicht im resources-Ordner gefunden. Verwende installiertes Paket.")

# Check Tesseract path
if not os.path.exists(TESSERACT_PATH):
    messagebox.showerror("Fehler", f"Tesseract-Pfad nicht gefunden: {TESSERACT_PATH}")
    sys.exit(1)

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

class AboutDialog:
    def __init__(self, parent):
        self.dialog = Toplevel(parent)
        self.dialog.title("Über PDF Dokumenten-Scanner")
        self.dialog.geometry("600x400")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Titel
        title_frame = Frame(self.dialog)
        title_frame.pack(fill=X, pady=10)
        
        title_label = Label(
            title_frame, 
            text="PDF Dokumenten-Scanner", 
            font=("Segoe UI", 14, "bold")
        )
        title_label.pack()
        
        version_label = Label(
            title_frame, 
            text="Version 1.1.0", 
            font=("Segoe UI", 10)
        )
        version_label.pack()
        
        # Beschreibung
        desc_frame = Frame(self.dialog)
        desc_frame.pack(fill=X, pady=10, padx=20)
        
        desc_label = Label(
            desc_frame,
            text="Ein Programm zur automatischen Erkennung und Umbenennung von PDF-Dokumenten mittels OCR.",
            font=("Segoe UI", 9),
            wraplength=550,
            justify=LEFT
        )
        desc_label.pack(anchor=W)
        
        # Lizenzinformationen
        license_frame = Frame(self.dialog)
        license_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        license_label = Label(
            license_frame,
            text="Lizenzinformationen:",
            font=("Segoe UI", 9, "bold"),
            justify=LEFT
        )
        license_label.pack(anchor=W)
        
        license_text = Text(
            license_frame,
            wrap=WORD,
            font=("Segoe UI", 9),
            height=15,
            width=80
        )
        license_text.insert("1.0", LICENSE_INFO)
        license_text.config(state=DISABLED)
        
        license_scroll = Scrollbar(license_frame, command=license_text.yview)
        license_text.config(yscrollcommand=license_scroll.set)
        
        license_scroll.pack(side=RIGHT, fill=Y)
        license_text.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Schließen-Button
        button_frame = Frame(self.dialog)
        button_frame.pack(fill=X, pady=10)
        
        close_button = Button(
            button_frame,
            text="Schließen",
            command=self.dialog.destroy,
            width=10
        )
        close_button.pack(pady=5)
        
        # Zentriere den Dialog auf dem Hauptfenster
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = parent.winfo_rootx() + (parent.winfo_width() - width) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - height) // 2
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")

class PDFOCRGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Dokumenten-Scanner")
        
        # Verwende die native Windows-Skalierung für die Fenstergröße
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        width = int(screen_width * 0.5)  # 50% der Bildschirmbreite
        height = int(screen_height * 0.4)  # 40% der Bildschirmhöhe
        self.root.geometry(f"{width}x{height}")
        
        # Moderne Schriftart für bessere DPI-Skalierung
        default_font = ("Segoe UI", 9)
        heading_font = ("Segoe UI", 12)
        
        # Configure style
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#f0f0f0")
        style.configure("TButton", font=default_font)
        style.configure("TLabel", font=default_font)
        
        # Main frame
        self.main_frame = ttk.Frame(root, style="Custom.TFrame", padding="20")
        self.main_frame.pack(fill=BOTH, expand=True)
        
        # Menüleiste
        self.create_menu()
        
        # File frame
        self.file_frame = ttk.Frame(self.main_frame, style="Custom.TFrame", padding="10")
        self.file_frame.pack(fill=BOTH, expand=True, pady=10)
        
        # Info label
        self.info_label = ttk.Label(
            self.file_frame,
            text="PDF-Dokumente auswählen\n(Verschiedene Dokumenttypen werden automatisch erkannt)",
            font=heading_font
        )
        self.info_label.pack(pady=10)
        
        # File button
        self.file_button = ttk.Button(
            self.file_frame,
            text="Dateien hinzufügen",
            command=self.add_files
        )
        self.file_button.pack(pady=5)
        
        # Listbox for files
        self.files_listbox = Listbox(
            self.file_frame,
            width=50,
            height=10,
            selectmode=EXTENDED,
            font=default_font
        )
        self.files_listbox.pack(fill=BOTH, expand=True)
        
        # Buttons
        self.button_frame = ttk.Frame(self.main_frame, style="Custom.TFrame")
        self.button_frame.pack(fill=X, pady=10)
        
        self.clear_button = ttk.Button(
            self.button_frame,
            text="Liste leeren",
            command=self.clear_list
        )
        self.clear_button.pack(side=LEFT, padx=5)
        
        self.start_button = ttk.Button(
            self.button_frame,
            text="Start",
            command=self.process_files
        )
        self.start_button.pack(side=RIGHT, padx=5)
        
        # Progress frame
        self.progress_frame = ttk.Frame(self.main_frame)
        self.progress_frame.pack(fill=X, pady=10)
        
        # Progress bar
        self.progress_var = DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
        
        # Percentage label
        self.percent_label = ttk.Label(
            self.progress_frame,
            text="0%",
            width=5,
            font=default_font
        )
        self.percent_label.pack(side=RIGHT)
        
        # Status label
        self.status_label = ttk.Label(
            self.main_frame,
            text="Bereit",
            font=default_font
        )
        self.status_label.pack(pady=5)
        
        self.pdf_files = []
    
    def create_menu(self):
        """Erstellt die Menüleiste"""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # Datei-Menü
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Datei", menu=file_menu)
        file_menu.add_command(label="Dateien hinzufügen", command=self.add_files)
        file_menu.add_command(label="Liste leeren", command=self.clear_list)
        file_menu.add_separator()
        file_menu.add_command(label="Beenden", command=self.root.destroy)
        
        # Hilfe-Menü
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Hilfe", menu=help_menu)
        help_menu.add_command(label="Über", command=self.show_about)
    
    def show_about(self):
        """Zeigt den Über-Dialog an"""
        AboutDialog(self.root)

    def update_progress(self, value, status_text=None):
        """Updates the progress bar and percentage display"""
        self.progress_var.set(value)
        self.percent_label.config(text=f"{int(value)}%")
        if status_text:
            self.status_label.config(text=status_text)
        self.root.update()

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="PDF-Dateien auswählen",
            filetypes=[("PDF Dateien", "*.pdf")]
        )
        
        for file in files:
            if file not in self.pdf_files:
                self.pdf_files.append(file)
                self.files_listbox.insert(END, os.path.basename(file))

    def clear_list(self):
        self.files_listbox.delete(0, END)
        self.pdf_files.clear()
        self.update_progress(0, "Bereit")

    def pdf_to_image(self, pdf_path, page_num=0):
        """Convert a PDF page to a PIL Image using PDFium"""
        try:
            # Open the PDF
            pdf_document = pdfium.PdfDocument(pdf_path)
            
            # Get the first page
            page = pdf_document[page_num]
            
            # Render page to an image with higher resolution (300 DPI)
            bitmap = page.render(scale=3.0)
            
            # Convert to PIL Image
            pil_image = bitmap.to_pil()
            
            return pil_image
            
        except Exception as e:
            print(f"Error converting PDF to image: {e}")
            return None

    def extract_info_from_pdf(self, pdf_path):
        """Extracts the project number and verifies the document type (Audit Note or Final Notice)."""
        try:
            # Convert first page of PDF to image
            img = self.pdf_to_image(pdf_path)
            if img is None:
                return None
            
            # Try German OCR first, fall back to English if not available
            try:
                text = pytesseract.image_to_string(img, lang='deu')
            except:
                text = pytesseract.image_to_string(img, lang='eng')
            
            # Debug output of recognized text
            print("Recognized Text:")
            print(text)
            print("-" * 50)
            
            # Search for project number using various patterns
            patterns = [
                r'Projekt-Nr\.:\s*(\d+)',
                r'Projekt-Nr\s*:\s*(\d+)',
                r'Projektnr\.?\s*:?\s*(\d+)',
                r'Projekt\s*[-.]?\s*Nr\.?\s*:?\s*(\d+)',
                r'Projekt\s*[-.]?\s*Nummer\s*:?\s*(\d+)',
                r'Projekt-Nr\.?:\s*(\d+)'
            ]
            
            projekt_nr = None
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    projekt_nr = match.group(1)
                    break
            
            if not projekt_nr:
                # Look for a number with exactly 10 digits
                numbers = re.findall(r'\b\d{10}\b', text)
                if numbers:
                    projekt_nr = numbers[0]
            
            if not projekt_nr:
                messagebox.showwarning(
                    "Keine Projekt-Nr. gefunden",
                    f"Konnte keine Projekt-Nr. in {os.path.basename(pdf_path)} finden."
                )
                return None
            
            # Identify document type
            if any(term in text for term in ["Prüfvermerk", "Prufvermerk", "Prüf vermerk", "Pruf vermerk"]):
                return f"{projekt_nr}_Prüfvermerk"
            elif any(term in text for term in ["Schlussbescheid", "Schluss bescheid", "Schlußbescheid", "Schluß bescheid"]):
                return f"{projekt_nr}_Schlussbescheid"
            elif any(term in text for term in ["Kursorische Prüfung", "Kursorische Prufung", "KursorischePrüfung", "KursorischePrufung", "kursorische prüfung", "kursorische prufung"]):
                return f"{projekt_nr}_Kursorische Prüfung"
            elif any(term in text for term in ["Anhörung", "Anhoerung", "anhörung", "anhoerung"]):
                return f"{projekt_nr}_Anhörung"
            elif any(term in text for term in ["Widerrufsbescheid", "Widerruf bescheid", "Widerrufbescheid", "widerrufsbescheid"]):
                return f"{projekt_nr}_Widerrufsbescheid"
            elif any(term in text for term in ["Auswertung Sachbericht", "AuswertungSachbericht", "Auswertung Sach-Bericht", "auswertung sachbericht"]):
                return f"{projekt_nr}_Auswertung Sachbericht"
            elif any(term in text for term in ["Zwischennachweis", "Zwischen nachweis", "Zwischen-Nachweis", "zwischennachweis"]):
                return f"{projekt_nr}_Zwischennachweis"
            elif any(term in text for term in ["Beleganforderung", "Beleg-Anforderung", "Beleg Anforderung", "beleganforderung"]):
                return f"{projekt_nr}_Beleganforderung"
            elif any(term in text for term in ["Archivierungsverfügung", "Archivierungsverfuegung", "Archivierung verfügung", "Archivierung-Verfügung", "archivierungsverfügung"]):
                return f"{projekt_nr}_Archivierungsverfügung"
            elif any(term in text for term in ["Änderungsbescheid", "Aenderungsbescheid", "Änderung bescheid", "Änderung-Bescheid", "aenderungsbescheid"]):
                return f"{projekt_nr}_Änderungsbescheid"
            elif any(term in text for term in ["Kurzantrag", "Kurz antrag", "Kurz-Antrag", "kurzantrag"]):
                return f"{projekt_nr}_Kurzantrag"
            elif any(term in text for term in ["Antrag", "antrag"]):
                return f"{projekt_nr}_Antrag"
            elif any(term in text for term in ["Förderzusage", "Foerderzusage", "Förder zusage", "Förder-Zusage", "foerderzusage"]):
                return f"{projekt_nr}_Förderzusage"
            elif any(term in text for term in ["Antragsprüfvermerk", "Antragsprufvermerk", "Antragsprüf vermerk", "Antrags-Prüfvermerk", "antragsprüfvermerk"]):
                return f"{projekt_nr}_Antragsprüfvermerk"
            elif any(term in text for term in ["Zuwendungsbescheid", "Zuwendung bescheid", "Zuwendung-Bescheid", "zuwendungsbescheid"]):
                return f"{projekt_nr}_Zuwendungsbescheid"
            elif any(term in text for term in ["Verwendungsnachweis", "Verwendung nachweis", "Verwendung-Nachweis", "verwendungsnachweis"]):
                return f"{projekt_nr}_Verwendungsnachweis"
            elif any(term in text for term in ["Mittelanforderung", "Mittel anforderung", "Mittel-Anforderung", "mittelanforderung"]):
                return f"{projekt_nr}_Mittelanforderung"
            elif any(term in text for term in ["Auszahlungsblatt", "Auszahlung blatt", "Auszahlung-Blatt", "auszahlungsblatt"]):
                return f"{projekt_nr}_Auszahlungsblatt"
            elif any(term in text for term in ["Erinnerungsschreiben", "Erinnerung schreiben", "Erinnerung-Schreiben", "erinnerungsschreiben"]):
                return f"{projekt_nr}_Erinnerungsschreiben"
            elif any(term in text for term in ["Mahnschreiben", "Mahn schreiben", "Mahn-Schreiben", "mahnschreiben"]):
                return f"{projekt_nr}_Mahnschreiben"
            else:
                messagebox.showwarning(
                    "Unbekannter Dokumenttyp",
                    f"Die Datei {os.path.basename(pdf_path)} scheint kein bekannter Dokumenttyp zu sein."
                )
                return None
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der Verarbeitung von {os.path.basename(pdf_path)}: {str(e)}")
            return None

    def process_files(self):
        if not self.pdf_files:
            messagebox.showinfo("Information", "Bitte fügen Sie zuerst PDF-Dateien hinzu.")
            return
        
        # Disable buttons during processing
        self.start_button.config(state='disabled')
        self.clear_button.config(state='disabled')
        self.file_button.config(state='disabled')
        
        try:
            # Create target directory in Downloads folder
            downloads_path = os.path.expanduser("~/Downloads")
            date_str = datetime.now().strftime("%Y-%m-%d")
            target_dir = os.path.join(downloads_path, f"Dokumentenscans_{date_str}")
            
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            
            total_files = len(self.pdf_files)
            processed_files = 0
            
            for pdf_path in self.pdf_files:
                # Update status and progress bar
                status_text = f"Verarbeite: {os.path.basename(pdf_path)}"
                progress = (processed_files / total_files) * 100
                self.update_progress(progress, status_text)
                
                new_name = self.extract_info_from_pdf(pdf_path)
                if new_name:
                    new_filename = f"{new_name}.pdf"
                    target_path = os.path.join(target_dir, new_filename)
                    
                    # Prevent duplicates
                    counter = 1
                    while os.path.exists(target_path):
                        new_filename = f"{new_name}_{counter}.pdf"
                        target_path = os.path.join(target_dir, new_filename)
                        counter += 1
                    
                    try:
                        shutil.copy2(pdf_path, target_path)
                    except Exception as e:
                        messagebox.showerror("Fehler", f"Fehler beim Kopieren von {os.path.basename(pdf_path)}: {str(e)}")
                
                processed_files += 1
                progress = (processed_files / total_files) * 100
                self.update_progress(progress)
            
            # Set progress bar to 100% and show "Finished"
            self.update_progress(100, "Fertig!")
            
            messagebox.showinfo(
                "Erfolg",
                f"Verarbeitung abgeschlossen!\nDie umbenannten Dateien befinden sich in:\n{target_dir}"
            )
        
        finally:
            # Re-enable buttons
            self.start_button.config(state='normal')
            self.clear_button.config(state='normal')
            self.file_button.config(state='normal')

def main():
    try:
        root = Tk()
        app = PDFOCRGUI(root)
        root.mainloop()
    except Exception as e:
        print("Ein Fehler ist aufgetreten:")
        print(str(e))
        input("Drücken Sie Enter zum Beenden...")

if __name__ == "__main__":
    main() 
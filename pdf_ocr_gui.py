import os
import sys
import shutil
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import pytesseract
from PIL import Image
import re
from pdf2image import convert_from_path

def get_base_path():
    """Determines the base path for resources, distinguishes between .exe and Python script"""
    if getattr(sys, 'frozen', False):
        # When running as .exe
        return os.path.dirname(sys.executable)
    else:
        # When running as Python script
        return os.path.dirname(os.path.abspath(__file__))

# Set resource paths
BASE_PATH = get_base_path()
POPPLER_PATH = os.path.join(BASE_PATH, "resources", "poppler")
TESSERACT_PATH = os.path.join(BASE_PATH, "resources", "Tesseract-OCR", "tesseract.exe")

# Set Tesseract environment variable
os.environ['TESSDATA_PREFIX'] = os.path.join(BASE_PATH, "resources", "Tesseract-OCR", "tessdata")

# Check paths
if not os.path.exists(POPPLER_PATH):
    messagebox.showerror("Fehler", f"Poppler-Pfad nicht gefunden: {POPPLER_PATH}")
    sys.exit(1)

if not os.path.exists(TESSERACT_PATH):
    messagebox.showerror("Fehler", f"Tesseract-Pfad nicht gefunden: {TESSERACT_PATH}")
    sys.exit(1)

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

class PDFOCRGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Dokumenten-Scanner")
        self.root.geometry("600x400")
        
        # Configure style
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#f0f0f0")
        
        # Main frame
        self.main_frame = ttk.Frame(root, style="Custom.TFrame", padding="20")
        self.main_frame.pack(fill=BOTH, expand=True)
        
        # File frame
        self.file_frame = ttk.Frame(self.main_frame, style="Custom.TFrame", padding="10")
        self.file_frame.pack(fill=BOTH, expand=True, pady=10)
        
        # Info label
        self.info_label = ttk.Label(
            self.file_frame,
            text="PDF-Dokumente auswählen\n(Prüfvermerke, Schlussbescheide und Beleganforderungen)",
            font=("Helvetica", 12)
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
            selectmode=EXTENDED
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
            width=5
        )
        self.percent_label.pack(side=RIGHT)
        
        # Status label
        self.status_label = ttk.Label(
            self.main_frame,
            text="Bereit",
            font=("Helvetica", 10)
        )
        self.status_label.pack(pady=5)
        
        self.pdf_files = []

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

    def extract_info_from_pdf(self, pdf_path):
        """Extracts the project number and verifies the document type (Audit Note or Final Notice)."""
        try:
            pages = convert_from_path(pdf_path, first_page=1, last_page=1, poppler_path=POPPLER_PATH)
            if not pages:
                return None
            
            # Try German OCR first, fall back to English if not available
            try:
                text = pytesseract.image_to_string(pages[0], lang='deu')
            except:
                text = pytesseract.image_to_string(pages[0], lang='eng')
            
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
            elif any(term in text for term in ["Beleganforderung", "Beleg-Anforderung", "Beleg Anforderung"]):
                return f"{projekt_nr}_Beleganforderung"
            else:
                messagebox.showwarning(
                    "Unbekannter Dokumenttyp",
                    f"Die Datei {os.path.basename(pdf_path)} scheint weder ein Prüfvermerk, ein Schlussbescheid noch eine Beleganforderung zu sein."
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
            target_dir = os.path.join(downloads_path, f"Prüfvermerke_{date_str}")
            
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
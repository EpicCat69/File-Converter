import os
import subprocess
from tkinter import Tk, filedialog, Label, Button, StringVar, OptionMenu, messagebox
from PIL import Image
from pydub import AudioSegment
import pandas as pd
from fpdf import FPDF
from docx2pdf import convert as docx2pdf_convert

# Conversion types and logic mapping
CONVERSIONS = {
    "Image: PNG -> JPG": ("image", "png", "jpg"),
    "Image: JPG -> PNG": ("image", "jpg", "png"),
    "Image: PNG -> WEBP": ("image", "png", "webp"),
    "Image: JPG -> ICO": ("image", "jpg", "ico"),
    "Audio: MP3 -> WAV": ("audio", "mp3", "wav"),
    "Audio: WAV -> MP3": ("audio", "wav", "mp3"),
    "Audio: MP3 -> OGG": ("audio", "mp3", "ogg"),
    "Audio: OGG -> WAV": ("audio", "ogg", "wav"),
    "Text: TXT -> PDF": ("txt_to_pdf", "txt", "pdf"),
    "Data: CSV -> JSON": ("csv_json", "csv", "json"),
    "Data: JSON -> CSV": ("csv_json", "json", "csv"),
    "Data: JSON -> lSX": ("json_xlsx", "json", "xlsx"),
    "Data: XLSX -> CSV": ("xlsx_csv", "xlsx", "csv"),
    "Doc: DOCX -> PDF": ("docx_pdf", "docx", "pdf"),
    "PDF -> TXT": ("pdf_txt", "pdf", "txt")
}

def is_ffmpeg_available():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

FFMPEG_AVAILABLE = is_ffmpeg_available()

def convert_file(filepath, conversion_type):
    category, from_ext, to_ext = CONVERSIONS[conversion_type]
    base, _ = os.path.splitext(filepath)
    output_path = f"{base}_converted.{to_ext}"

    try:
        if category == "image":
            img = Image.open(filepath)
            img.convert("RGB").save(output_path)
        elif category == "audio":
            if not FFMPEG_AVAILABLE:
                raise EnvironmentError("FFmpeg is not installed or not in PATH.")
            sound = AudioSegment.from_file(filepath, format=from_ext)
            sound.export(output_path, format=to_ext)
        elif category == "txt_to_pdf":
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)
            for line in text.split('\n'):
                pdf.multi_cell(0, 10, line)
            pdf.output(output_path)
        elif category == "csv_json":
            if from_ext == "csv":
                df = pd.read_csv(filepath)
                df.to_json(output_path, orient="records", indent=4)
            else:
                df = pd.read_json(filepath)
                df.to_csv(output_path, index=False)
        elif category == "json_xlsx":
            df = pd.read_json(filepath)
            df.to_excel(output_path, index=False)
        elif category == "xlsx_csv":
            df = pd.read_excel(filepath)
            df.to_csv(output_path, index=False)
        elif category == "docx_pdf":
            docx2pdf_convert(filepath, output_path)
        elif category == "pdf_txt":
            try:
                from PyPDF2 import PdfReader
                reader = PdfReader(filepath)
                with open(output_path, "w", encoding="utf-8") as f:
                    for page in reader.pages:
                        f.write(page.extract_text() or "")
            except ImportError:
                raise ImportError("Please install PyPDF2 to extract text from PDFs.")
        messagebox.showinfo("Success", f"File converted and saved as:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Conversion Error", f"Failed to convert:\n{str(e)}")

def browse_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        selected_file.set(filepath)

def perform_conversion():
    filepath = selected_file.get()
    if not filepath:
        messagebox.showwarning("No File", "Please select a file first.")
        return
    convert_file(filepath, conversion_choice.get())

# GUI
root = Tk()
root.title("Universal File Converter")

Label(root, text="Selected file:").pack(pady=(10, 0))
selected_file = StringVar()
Label(root, textvariable=selected_file, wraplength=400).pack(padx=10)

Button(root, text="Browse", command=browse_file).pack(pady=5)

Label(root, text="Choose conversion type:").pack(pady=(10, 0))
conversion_choice = StringVar(value=list(CONVERSIONS.keys())[0])
OptionMenu(root, conversion_choice, *CONVERSIONS.keys()).pack(pady=5)

Button(root, text="Convert", command=perform_conversion).pack(pady=15)

root.mainloop()

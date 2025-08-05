# File-Converter
A desktop file converter built with Python. Supports images, audio, documents, spreadsheets, and text. Includes smart format detection, error handling, and a clean GUI using Tkinter. FFmpeg fallback for audio conversions. Easy to use and extend.


---

## ✨ Features

- ✅ Image conversions (JPG, PNG, WEBP, ICO)
- 🎧 Audio conversions (MP3, WAV, OGG) using FFmpeg
- 📄 Document conversions (TXT ➝ PDF, DOCX ➝ PDF, PDF ➝ TXT)
- 📊 Spreadsheet conversions (CSV, XLSX, JSON)
- 🎛️ Automatic format handling
- 🛑 Error messages for missing tools or bad files
- 🪟 GUI made with Tkinter

---

## 📦 Supported Conversions

| From            | To                       |
|-----------------|--------------------------|
| PNG, JPG        | JPG, PNG, WEBP, ICO      |
| MP3, WAV, OGG   | MP3, WAV, OGG            |
| TXT             | PDF                      |
| DOCX            | PDF                      |
| PDF             | TXT                      |
| CSV, JSON, XLSX | CSV, JSON, XLSX          |

---

## 🖥️ How to Run

1. **Install dependencies:**

```bash
pip install pillow pandas pydub fpdf openpyxl python-docx docx2pdf PyPDF2
```

2. Make sure FFmpeg is installed (for audio):

  - [Download FFmpeg](https://ffmpeg.org/download.html)

  - Add it to your system PATH

3. Run the app:

---

## 🛠 Packaging (Optional)

To make it a standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed file_converter.py
```

## 🧱 Notes
  - 🧪 Tested on Python 3.11 — not compatible with Python 3.13 due to missing audioop module.
    
  - 🧰 Replace or refactor pydub audio conversion if you plan to use Python 3.13+

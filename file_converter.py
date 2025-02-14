# file_converter.py

import os
import unicodedata
import re
from docx2pdf import convert


def normalize_filename(filename):
    nfkd_form = unicodedata.normalize('NFKD', filename)
    only_ascii = nfkd_form.encode('ASCII', 'ignore').decode('ASCII')
    only_ascii = re.sub(r'\s+', '_', only_ascii)
    return only_ascii


def convert_docx_to_pdf(input_file, output_file):
    try:
        # Normalisiere den Basis-Dateinamen
        base = os.path.basename(input_file)
        filename, ext = os.path.splitext(base)
        safe_filename = normalize_filename(filename)
        # Aktualisiere den output_file Pfad mit dem sicheren Dateinamen
        output_file = os.path.join(os.path.dirname(output_file), safe_filename + ".pdf")

        convert(input_file, output_file)
        if not os.path.exists(output_file):
            print(f"Konvertierung abgeschlossen, aber {output_file} wurde nicht gefunden.")
        else:
            print(f"[DOCX -> PDF] {input_file} konvertiert nach {output_file}")
    except Exception as e:
        print(f"Fehler beim Konvertieren von {input_file}: {e}")

def convert_docx_to_pdf(input_file, output_file):
    try:
        # Normalisiere den Basis-Dateinamen, falls notwendig:
        from docx2pdf import convert
        convert(input_file, output_file)
        if not os.path.exists(output_file):
            print(f"Konvertierung abgeschlossen, aber {output_file} wurde nicht gefunden.")
        else:
            print(f"[DOCX -> PDF] {input_file} konvertiert nach {output_file}")
    except Exception as e:
        print(f"Fehler beim Konvertieren von {input_file}: {e}")

def convert_msg_to_pdf(input_file, output_file):
    """
    Konvertiert eine MSG-Datei in eine PDF-Datei.
    Hier wird die Konvertierung mit extract_msg und ReportLab durchgeführt.
    """
    try:
        # Wir importieren hier lokal, damit diese Funktion unabhängig funktioniert.
        import extract_msg
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter

        msg = extract_msg.Message(input_file)
        msg_sender = msg.sender
        msg_date = msg.date
        msg_subject = msg.subject
        msg_body = msg.body

        c = canvas.Canvas(output_file, pagesize=letter)
        width, height = letter
        textobject = c.beginText(40, height - 40)
        lines = [
            f"Subject: {msg_subject}",
            f"From: {msg_sender}",
            f"Date: {msg_date}",
            "",
            msg_body
        ]
        for line in lines:
            for subline in line.split("\n"):
                textobject.textLine(subline)
        c.drawText(textobject)
        c.showPage()
        c.save()
        print(f"[MSG -> PDF] {input_file} konvertiert nach {output_file}")
    except Exception as e:
        print(f"Fehler beim Konvertieren von {input_file}: {e}")
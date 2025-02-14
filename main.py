import os
from docx_redactor import process_docx
from pdf_redactor import redact_pdf
from file_converter import convert_docx_to_pdf, convert_msg_to_pdf

def main():
    # Ordner vom Benutzer abfragen
    folder = input("Bitte geben Sie den Pfad zum Ordner ein, der verarbeitet werden soll:\n").strip()
    if not os.path.isdir(folder):
        print("Der angegebene Pfad ist kein gültiger Ordner!")
        return

    # Frage, ob DOCX und MSG in PDF umgewandelt werden sollen
    conv_choice = input("Möchten Sie DOCX und MSG Dateien in PDF umwandeln? (j/n): ").strip().lower()

    # Erstelle Unterordner:
    conv_folder = os.path.join(folder, "converted")
    redacted_folder = os.path.join(folder, "redacted")
    os.makedirs(conv_folder, exist_ok=True)
    os.makedirs(redacted_folder, exist_ok=True)

    pdf_files_to_process = []

    if conv_choice == 'j':
        # Konvertierungszweig: Alle DOCX und MSG werden in PDFs umgewandelt
        for file in os.listdir(folder):
            full_path = os.path.join(folder, file)
            if os.path.isfile(full_path):
                filename, ext = os.path.splitext(file)
                ext = ext.lower()
                if ext == ".docx":
                    output_pdf = os.path.join(conv_folder, filename + ".pdf")
                    print(f"Konvertiere DOCX: {full_path}")
                    convert_docx_to_pdf(full_path, output_pdf)
                    if os.path.exists(output_pdf):
                        pdf_files_to_process.append(output_pdf)
                    else:
                        print(f"Warnung: Konvertierte Datei nicht gefunden: {output_pdf}")
                elif ext == ".msg":
                    output_pdf = os.path.join(conv_folder, filename + ".pdf")
                    print(f"Konvertiere MSG: {full_path}")
                    convert_msg_to_pdf(full_path, output_pdf)
                    if os.path.exists(output_pdf):
                        pdf_files_to_process.append(output_pdf)
                    else:
                        print(f"Warnung: Konvertierte Datei nicht gefunden: {output_pdf}")
        # Zusätzlich: Füge alle vorhandenen PDFs aus dem Ursprungsordner hinzu
        for file in os.listdir(folder):
            full_path = os.path.join(folder, file)
            if os.path.isfile(full_path):
                _, ext = os.path.splitext(file)
                if ext.lower() == ".pdf":
                    pdf_files_to_process.append(full_path)
    else:
        # Kein Konvertierungszweig:
        # - DOCX werden direkt redaktiert (als DOCX)
        # - MSG werden trotzdem in PDF konvertiert, weil für MSG keine native Redaction existiert
        # - Vorhandene PDFs werden verarbeitet
        for file in os.listdir(folder):
            full_path = os.path.join(folder, file)
            if os.path.isfile(full_path):
                filename, ext = os.path.splitext(file)
                ext = ext.lower()
                if ext == ".pdf":
                    pdf_files_to_process.append(full_path)
                elif ext == ".docx":
                    output_docx = os.path.join(redacted_folder, file)
                    print(f"Verarbeite DOCX: {full_path}")
                    process_docx(full_path, output_docx)
                elif ext == ".msg":
                    output_pdf = os.path.join(conv_folder, filename + ".pdf")
                    print(f"Konvertiere MSG: {full_path}")
                    convert_msg_to_pdf(full_path, output_pdf)
                    if os.path.exists(output_pdf):
                        pdf_files_to_process.append(output_pdf)
                    else:
                        print(f"Warnung: Konvertierte Datei nicht gefunden: {output_pdf}")

    # Entferne eventuelle Duplikate
    pdf_files_to_process = list(set(pdf_files_to_process))

    # Verarbeitung der PDFs: Redaktion
    for pdf_file in pdf_files_to_process:
        base = os.path.basename(pdf_file)
        output_file = os.path.join(redacted_folder, base)
        if os.path.exists(pdf_file):
            print(f"Verarbeite PDF: {pdf_file}")
            redact_pdf(pdf_file, output_file)
        else:
            print(f"PDF nicht gefunden, überspringe: {pdf_file}")

    print("Verarbeitung abgeschlossen!")
    print(f"Die redacted Dateien befinden sich im Unterordner 'redacted'.")

if __name__ == '__main__':
    main()
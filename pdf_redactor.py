import fitz  # PyMuPDF
import re


def redact_pdf(file_path, output_path):
    """
    Liest eine PDF-Datei, sucht nach sensiblen Mustern und schwärzt die entsprechenden Bereiche.
    (Verwendet lokale Regex-Muster.)
    """
    doc = fitz.open(file_path)

    # Lokale Regex-Muster (ähnlich wie bei DOCX):
    patterns = [
         r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',  # E-Mail-Adressen
        r'\b\+?\d[\d\s-]{7,}\d\b',                              # Telefonnummern
        r'\b(?:Herr|Frau|Dr\.|Prof\.)\s+[A-ZÄÖÜ][a-zäöüß]+(?:\s+[A-ZÄÖÜ][a-zäöüß]+)?\b',  # Namen mit Titeln
        r'\b[A-ZÄÖÜ][a-zäöüß]+(?:\s+[A-ZÄÖÜ][a-zäöüß]+)+\b',     # Generische Namen (mindestens 2 Wörter)
        r'\b(?:[A-ZÄÖÜ][a-zäöüß]+(?:\s+[A-ZÄÖÜ][a-zäöüß]+)*)\s+(?:Straße|Strasse|Weg|Gasse|Platz|Allee|Damm|Ring|Ufer)\s+\d+[a-zA-Z]?\b'  # Adressen
    ]

    for page in doc:
        redaction_areas = []
        page_text = page.get_text()
        for pattern in patterns:
            for match in re.finditer(pattern, page_text):
                matched_str = match.group()
                areas = page.search_for(matched_str)
                redaction_areas.extend(areas)
        for rect in redaction_areas:
            page.add_redact_annot(rect, fill=(0, 0, 0))
        page.apply_redactions()

    doc.save(output_path)
    print(f"PDF-Redaktion abgeschlossen: {output_path}")

# Auch hier kannst du die Funktion direkt testen.
import openai

# Setze deinen API-Key – idealerweise über eine Umgebungsvariable!
openai.api_key = 'Your Open AI API key'


def redact_text_api(text):
    """
    Schickt den gesamten Text an die API, die sensible Daten schwärzt.
    Erwartet wird, dass der zurückgelieferte Text bereits die
    sensiblen Informationen durch '[REDACTED]' ersetzt hat.
    """
    prompt = (
        "Bitte redigiere den folgenden Text, indem du alle sensiblen "
        "personenbezogenen Daten (wie Namen, Adressen, E-Mail-Adressen, Telefonnummern) "
        "schwärzt oder entfernst. Ersetze die geschwärzten Bereiche durch den Platzhalter '[REDACTED]'.\n\n"
        f"Text:\n{text}"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )

    redacted_text = response.choices[0].message.content.strip()
    return redacted_text


# Testweise:
if __name__ == '__main__':
    sample_text = "Herr Mustermann wohnt in der Musterstraße 12, E-Mail: mustermann@example.com, Tel: 123-456-7890."
    print("Redacted Text (API):\n", redact_text_api(sample_text))
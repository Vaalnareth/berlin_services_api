import requests
from bs4 import BeautifulSoup

def extract_info(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Debugging: Ausgabe der gesamten HTML-Struktur
    print("HTML-Struktur der Seite:")
    print(soup.prettify()[:50000])  # Nur die ersten 10000 Zeichen anzeigen

    # Extrahieren des Titels
    title_element = soup.find('h1')
    title = title_element.text.strip() if title_element else "Kein Titel gefunden"

    # Funktion zum Extrahieren von Listenüberschriften
    def extract_list_titles(soup, section_title):
        section = soup.find('h2', string=section_title)
        if section:
            content = section.find_next('div', class_='htmlBox')
            if content:
                list_items = content.find_all('li')
                return [item.text.strip() for item in list_items]
        return []

    # Funktion zum Extrahieren von Textabschnitten
    def extract_section_text(soup, section_title):
        section = soup.find('h2', string=section_title)
        if section:
            content = section.find_next('div', class_='htmlBox')
            if content:
                return content.text.strip()
        return ""

    # Debugging: Ausgabe der HTML-Struktur der relevanten Abschnitte
    def debug_section(soup, section_title):
        section = soup.find('h2', string=section_title)
        if section:
            content = section.find_next('div', class_='htmlBox')
            if content:
                print(f"HTML-Struktur des Abschnitts '{section_title}':")
                print(content.prettify())  # Gesamten Inhalt des Abschnitts anzeigen

    # Debugging: Ausgabe der HTML-Struktur der relevanten Abschnitte
    debug_section(soup, 'Voraussetzungen')
    debug_section(soup, 'Erforderliche Unterlagen')
    debug_section(soup, 'Gebühren')
    debug_section(soup, 'Rechtsgrundlagen')

    # Extrahieren der gewünschten Informationen
    voraussetzungen = extract_list_titles(soup, 'Voraussetzungen')
    erforderliche_unterlagen = extract_list_titles(soup, 'Erforderliche Unterlagen')
    gebuehren = extract_section_text(soup, 'Gebühren')
    rechtsgrundlagen = extract_list_titles(soup, 'Rechtsgrundlagen')

    # Extrahieren der Formulare
    formulare = []
    form_elements = soup.select('.form-links a')
    for form_element in form_elements:
        form_url = form_element['href']
        formulare.append(form_url)

    # Ausgabe der extrahierten Informationen
    print(f"Titel: {title}")
    print(f"Voraussetzungen: {voraussetzungen}")
    print(f"Erforderliche Unterlagen: {erforderliche_unterlagen}")
    print(f"Formulare: {formulare}")
    print(f"Gebühren: {gebuehren}")
    print(f"Rechtsgrundlagen: {rechtsgrundlagen}")

if __name__ == "__main__":
    url = "https://service.berlin.de/dienstleistung/329616/"
    extract_info(url)
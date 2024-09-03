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

    # Extracting the title
    title_element = soup.find('h1')
    title = title_element.text.strip() if title_element else "Kein Titel gefunden"

    # Function to extract content between sections
    def extract_section_content(header):
        content = []
        if header:
            section = header.find_next_sibling()
            while section and section.name != 'h2':
                content.append(section.get_text(separator="\n").strip())
                section = section.find_next_sibling()
        return "\n".join(content) if content else "Keine Informationen gefunden"

    # Extracting the desired information
    voraussetzungen_header = soup.find('h2', string='Voraussetzungen')
    voraussetzungen = extract_section_content(voraussetzungen_header)

    unterlagen_header = soup.find('h2', string='Erforderliche Unterlagen')
    erforderliche_unterlagen = extract_section_content(unterlagen_header)

    gebuehren_header = soup.find('h2', string='Gebühren')
    gebuehren = extract_section_content(gebuehren_header) or "Keine Gebühren gefunden"

    rechtsgrundlagen_header = soup.find('h2', string='Rechtsgrundlagen')
    rechtsgrundlagen = extract_section_content(rechtsgrundlagen_header)

    formular_header = soup.find('h2', string='Formulare')
    formulare = "Keine Formulare gefunden"
    if formular_header:
        formular_list = formular_header.find_next_sibling('ul')
        if formular_list:
            formular_links = formular_list.find_all('a')
            formulare = [{'title': link.text.strip(), 'url': link['href']} for link in formular_links]

    # Outputting the extracted information
    print(f"Titel:\n- {title}\n")
    print("Voraussetzungen:")
    print(f"- {voraussetzungen}\n")
    
    print("Erforderliche Unterlagen:")
    print(f"- {erforderliche_unterlagen}\n")

    print("Gebühren:")
    print(f"- {gebuehren}\n")
    
    print("Rechtsgrundlagen:")
    print(f"- {rechtsgrundlagen}\n")
    
    print("Formulare:")
    if isinstance(formulare, str):
        print(f"- {formulare}")
    else:
        for form in formulare:
            print(f"- {form['title']}: {form['url']}")

    # Returning the extracted data in a dictionary format
    return {
        'title': title,
        'voraussetzungen': voraussetzungen,
        'erforderliche_unterlagen': erforderliche_unterlagen,
        'gebuehren': gebuehren,
        'rechtsgrundlagen': rechtsgrundlagen,
        'formulare': formulare
    }

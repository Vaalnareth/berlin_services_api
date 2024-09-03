import requests
from requests.exceptions import RequestException, Timeout
from bs4 import BeautifulSoup
from app.models import Service, Form
from app.db import get_session
import logging
from tqdm import tqdm

# Konfigurieren Sie das Logging
logging.basicConfig(level=logging.WARNING)  # Ändern Sie das Level zu WARNING, um weniger detaillierte Informationen auszugeben
logger = logging.getLogger(__name__)

MAX_URL_LENGTH = 2048  # Setzen Sie die maximale Länge der URL

def extract_info(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching the URL: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extracting the title
    title_element = soup.find('h1')
    title = title_element.text.strip() if title_element else None

    if title is None:
        logger.error(f"NULL title found for URL: {url}")

    # Function to extract content between sections
    def extract_section_content(header):
        content = []
        section = header.find_next_sibling()
        while section and section.name != 'h2':
            content.append(section.get_text(separator="\n").strip())
            section = section.find_next_sibling()
        return "\n".join(content)

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
    formulare = []
    if formular_header:
        formular_list = formular_header.find_next_sibling('ul')
        if formular_list:
            formular_links = formular_list.find_all('a')
            formulare = [{'title': link.text.strip(), 'url': link['href']} for link in formular_links]

    return {
        "title": title,
        "voraussetzungen": voraussetzungen,
        "erforderliche_unterlagen": erforderliche_unterlagen,
        "gebuehren": gebuehren,
        "rechtsgrundlagen": rechtsgrundlagen,
        "formulare": formulare
    }

def crawl_data():
    base_url = "https://service.berlin.de/dienstleistungen/"
    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
    except (RequestException, Timeout) as e:
        logger.error(f"Error fetching the main page: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Debugging: HTML-Inhalt der Hauptseite ausgeben
    logger.debug(f"HTML content of the main page: {soup.prettify()[:1000]}...")  # Nur die ersten 1000 Zeichen anzeigen

    services = []
    service_links = soup.select('div.span7 a')
    logger.info(f"Found {len(service_links)} service links.")

    # Verwenden Sie tqdm, um eine Fortschrittsanzeige hinzuzufügen
    for link in tqdm(service_links, desc="Scraping services"):
        service_url = link['href']
        logger.info(f"Crawling service URL: {service_url}")
        service_data = extract_info(service_url)
        if not service_data:
            continue

        if service_data['title'] is None:
            logger.error(f"NULL title found for service URL: {service_url}")
            continue

        logger.info(f"Service Title: {service_data['title']}")
        logger.debug(f"Prerequisites: {service_data['voraussetzungen'][:100]}...")  # Nur die ersten 100 Zeichen anzeigen
        logger.debug(f"Required Documents: {service_data['erforderliche_unterlagen'][:100]}...")  # Nur die ersten 100 Zeichen anzeigen
        logger.debug(f"Fees: {service_data['gebuehren'][:100]}...")  # Nur die ersten 100 Zeichen anzeigen
        logger.debug(f"Legal Basis: {service_data['rechtsgrundlagen'][:100]}...")  # Nur die ersten 100 Zeichen anzeigen
        logger.debug(f"Forms: {service_data['formulare']}")

        with get_session() as session:
            # Dienstleistung erstellen
            service = Service(
                title=service_data['title'],
                voraussetzungen=service_data['voraussetzungen'],
                erforderliche_unterlagen=service_data['erforderliche_unterlagen'],
                gebuehren=service_data['gebuehren'],
                rechtsgrundlagen=service_data['rechtsgrundlagen']
            )
            services.append(service)

            for form_data in service_data['formulare']:
                if form_data['title'] is None:
                    logger.error(f"NULL title found for form URL: {form_data['url']} in service URL: {service_url}")
                    continue
                if len(form_data['url']) > MAX_URL_LENGTH:
                    logger.error(f"URL too long for form URL: {form_data['url']} in service URL: {service_url}")
                    continue
                form = Form(title=form_data['title'], url=form_data['url'], service=service)
                service.forms.append(form)

            session.add_all(services)
            session.commit()
            logger.info("Data committed to the database.")

if __name__ == "__main__":
    crawl_data()
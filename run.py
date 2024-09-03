from app.scraper import crawl_data
from app.db import init_db
from dotenv import load_dotenv

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()

if __name__ == "__main__":
    init_db()
    crawl_data()
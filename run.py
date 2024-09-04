from app.scraper import crawl_data
from app.db import init_db
from dotenv import load_dotenv
import uvicorn

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()

if __name__ == "__main__":
    init_db()
    crawl_data()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
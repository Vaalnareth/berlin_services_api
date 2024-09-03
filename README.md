# Berlin Services API

A little project for training in handling API and webscraping for a MySQL-Database.

## Installation

### Voraussetzungen

- Python 3.8 oder höher
- MySQL-Server
- MySQL-Client

### Schritte zur Installation

1. Klonen Sie das Repository:

   ```sh
   git clone https://github.com/yourusername/berlin_services_api.git
   cd berlin_services_api
   ```
2. Erstellen und aktivieren Sie eine virtuelle Umgebung:

   ```sh
   python -m venv venv
   source venv/bin/activate  # Auf Windows: venv\Scripts\activate
   ```
3. Installieren Sie die Python-Abhängigkeiten:

   ```sh
   pip install -r requirements.txt
   ```
4. Installieren Sie den MySQL-Client:

   - **Ubuntu/Debian**:

     ```sh
     sudo apt-get install mysql-client
     ```
   - **macOS**:

     ```sh
     brew install mysql-client
     ```
   - **Windows**:

     Laden Sie den MySQL-Client von der [MySQL-Website](https://dev.mysql.com/downloads/mysql/) herunter und installieren Sie ihn.
5. Erstellen Sie eine [`.env`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fc%3A%2FUsers%2FAdmin%2FDocuments%2FDataSmart%2FProjekte%2FScraper%2F.env%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "c:\Users\Admin\Documents\DataSmart\Projekte\Scraper\.env")-Datei im Hauptverzeichnis und fügen Sie Ihre Umgebungsvariablen hinzu, basierend auf der [`.env.example`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fc%3A%2FUsers%2FAdmin%2FDocuments%2FDataSmart%2FProjekte%2FScraper%2F.env.example%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "c:\Users\Admin\Documents\DataSmart\Projekte\Scraper\.env.example")-Datei:

   ```sh
   cp .env.example .env
   ```

   Bearbeiten Sie die [`.env`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fc%3A%2FUsers%2FAdmin%2FDocuments%2FDataSmart%2FProjekte%2FScraper%2F.env%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "c:\Users\Admin\Documents\DataSmart\Projekte\Scraper\.env")-Datei und fügen Sie Ihre tatsächlichen Werte hinzu.
6. Initialisieren Sie die Datenbank und starten Sie den Scraping-Prozess:

   ```sh
   python run.py
   ```

## Nutzung

Starten Sie die FastAPI-Anwendung:

```sh
uvicorn main:app --reload
```

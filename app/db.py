from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import create_engine as sqlalchemy_create_engine, text
from sqlalchemy.exc import OperationalError
from config import config
import os
from contextlib import contextmanager

# Bestimmen Sie die Umgebung (Standard ist Entwicklung)
env = os.getenv("ENV", "development")
DATABASE_URL = config[env].SQLALCHEMY_DATABASE_URI

# Manuelles Parsen der Datenbank-URL, um Verbindungsparameter zu extrahieren
url_parts = DATABASE_URL.split('/')
database_name = url_parts[-1]
base_url = '/'.join(url_parts[:-1])

# Manuell die Verbindungs-URL ohne den Datenbankteil konstruieren
temp_url = f"{base_url}/"

# Erstellen Sie eine temporäre Engine, um eine Verbindung zum MySQL-Server herzustellen
temp_engine = sqlalchemy_create_engine(temp_url)

try:
    # Erstellen Sie die Datenbank, falls sie nicht existiert
    with temp_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {database_name}"))
        conn.execute(text(f"USE {database_name}"))
except OperationalError as e:
    print(f"Fehler beim Verbinden mit der Datenbank: {e}")
    raise

# Erstellen Sie die eigentliche Engine für die Anwendung
engine = create_engine(DATABASE_URL)

def init_db():
    SQLModel.metadata.create_all(engine)
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE service MODIFY COLUMN voraussetzungen TEXT"))
        conn.execute(text("ALTER TABLE service MODIFY COLUMN erforderliche_unterlagen TEXT"))
        conn.execute(text("ALTER TABLE service MODIFY COLUMN gebuehren TEXT"))
        conn.execute(text("ALTER TABLE service MODIFY COLUMN rechtsgrundlagen TEXT"))
        conn.execute(text("ALTER TABLE form MODIFY COLUMN url VARCHAR(2048)"))  # Hier die Länge der URL-Spalte ändern
        conn.execute(text("ALTER TABLE form MODIFY COLUMN title VARCHAR(2048)"))  # Hier die Länge der Title-Spalte ändern

@contextmanager
def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
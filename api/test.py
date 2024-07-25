import pytest
from fastapi.testclient import TestClient
import sys
import os

# Ajouter le chemin du projet au PYTHONPATH
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from main import app, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base

# Créez une base de données de test en mémoire
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créez toutes les tables de la base de données
Base.metadata.create_all(bind=engine)

# Remplacez la dépendance get_db par une session de test
@pytest.fixture(scope="module")
def client():
    def _get_test_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as c:
        yield c

# Test de l'endpoint /source_info/{source_info}
def test_read_source_info(client):
    response = client.get("/source_info/test_source")
    assert response.status_code == 404
    assert response.json() == {"detail": "Source not found"}

# Test de l'endpoint /region/{region}
def test_read_region(client):
    response = client.get("/region/test_region")
    assert response.status_code == 404
    assert response.json() == {"detail": "Region not found"}

# Test de l'endpoint /formacode/{code}
def test_read_formacode(client):
    response = client.get("/formacode/test_code")
    assert response.status_code == 404
    assert response.json() == {"detail": "Formacode not found"}

# Ajoutez d'autres tests en fonction des cas d'utilisation spécifiques

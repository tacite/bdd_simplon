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
    """
    ## client()

    Fixture to create a FastAPI test client with an in-memory SQLite database.

    Uses an override of the `get_db` dependency to provide a test database session.

    Yields:
        TestClient: The FastAPI test client.
    """
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
    """
    ## test_read_source_info()

    Tests the /source_info/{source_info} endpoint to check behavior when the source is not found.

    Uses the test client to send a GET request to the endpoint with a test source.
    Verifies that the response has HTTP status 404 and contains the expected error message.
    """
    response = client.get("/source_info/test_source")
    assert response.status_code == 404
    assert response.json() == {"detail": "Source not found"}

# Test de l'endpoint /region/{region}
def test_read_region(client):
    """
    ## test_read_region()

    Tests the /region/{region} endpoint to check behavior when the region is not found.

    Uses the test client to send a GET request to the endpoint with a test region.
    Verifies that the response has HTTP status 404 and contains the expected error message.
    """
    response = client.get("/region/test_region")
    assert response.status_code == 404
    assert response.json() == {"detail": "Region not found"}

# Test de l'endpoint /formacode/{code}
def test_read_formacode(client):
    """
    ## test_read_formacode()
    
    Tests the /formacode/{code} endpoint to check behavior when the formacode is not found.

    Uses the test client to send a GET request to the endpoint with a test code.
    Verifies that the response has HTTP status 404 and contains the expected error message.
    """
    response = client.get("/formacode/test_code")
    assert response.status_code == 404
    assert response.json() == {"detail": "Formacode not found"}

# Ajoutez d'autres tests en fonction des cas d'utilisation spécifiques

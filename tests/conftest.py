import sys; print(sys.path)
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    yield TestClient(app)


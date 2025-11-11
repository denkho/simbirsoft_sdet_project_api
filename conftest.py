import pytest
from api.client import APIClient
from config.config import Config


@pytest.fixture(scope="session")
def base_url():
    return Config.HOST


@pytest.fixture(scope="session")
def client(base_url):
    return APIClient(base_url)


@pytest.fixture
def entity(client):
    payload = {
        "addition": {"additional_info": "Fixture", "additional_number": 123},
        "important_numbers": [10, 20],
        "title": "Тестовая сущность",
        "verified": True,
    }
    response = client.post(Config.ENDPOINTS["create"], json=payload)
    entity_id = int(response.text)

    yield entity_id, payload

    client.delete(Config.ENDPOINTS["delete"].format(id=entity_id))

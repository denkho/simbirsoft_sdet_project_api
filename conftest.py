import pytest
import requests
from config import Config


@pytest.fixture
def base_url():
    return Config.HOST


@pytest.fixture
def entity(base_url):
    payload = {
        "addition": {"additional_info": "Test info", "additional_number": 121325},
        "important_numbers": [12, 84, 586],
        "title": "Test entity for API testing",
        "verified": True,
    }

    response = requests.post(
        f"{base_url}{Config.ENDPOINTS['create']}", json=payload
    )
    assert response.status_code == 200
    entity_id = int(response.text)

    yield entity_id, payload

    # Удаляем сущность после теста
    del_response = requests.delete(
        f"{base_url}{Config.ENDPOINTS['delete'].format(id=entity_id)}"
    )
    assert del_response.status_code in (200, 204)

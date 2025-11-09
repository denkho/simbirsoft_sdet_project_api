import requests
from config import Config


def test_create_entity(base_url):
    payload = {
        "addition": {"additional_info": "Creation", "additional_number": 999},
        "important_numbers": [1, 2, 3],
        "title": "New Entity for test",
        "verified": True,
    }
    response = requests.post(
        f"{base_url}{Config.ENDPOINTS['create']}", json=payload
    )
    assert response.status_code == 200
    entity_id = int(response.text)
    assert entity_id > 0
    requests.delete(f"{base_url}{Config.ENDPOINTS['delete'].format(id=entity_id)}")

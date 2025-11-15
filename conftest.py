import allure
import pytest
from api.client import APIClient
from config.config import Config
from data import payloads


@pytest.fixture(scope="session")
def base_url():
    return Config.HOST


@pytest.fixture(scope="session")
def client(base_url):
    return APIClient(base_url)


@pytest.fixture
def entity(client):
    """Создание тестовой сущности и ее удаление после теста"""
    payload = payloads.Payloads.SAMPLE_ENTITY
    
    with allure.step("Создание тестовой сущности через POST create"):
        response = client.post(Config.ENDPOINTS["create"], json=payload)
        entity_id = int(response.text)

    yield entity_id, payload
    with allure.step(f"Удаление тестовой сущности через DELETE: {entity_id}"):
        client.delete(Config.ENDPOINTS["delete"].format(id=entity_id))

import allure
import requests
from config import Config
from models import Entity


@allure.suite("API Tests")
class TestAPI:

    @allure.feature("Создание сущности")
    def test_create_entity(self, base_url):
        payload = {
            "addition": {"additional_info": "Создание", "additional_number": 999},
            "important_numbers": [1, 2, 3],
            "title": "Новая сущность",
            "verified": True,
        }

        with allure.step("POST /api/create — создание сущности"):
            response = requests.post(
                f"{base_url}{Config.ENDPOINTS['create']}",
                json=payload,
                timeout=Config.TIMEOUT,
            )
            assert response.status_code == 200

        entity_id = int(response.text)
        assert entity_id > 0

        with allure.step("Очистка созданной сущности"):
            requests.delete(
                f"{base_url}{Config.ENDPOINTS['delete'].format(id=entity_id)}",
                timeout=Config.TIMEOUT,
            )

    @allure.feature("Получение сущности по ID")
    def test_get_entity(self, base_url, entity):
        entity_id, payload = entity
        response = requests.get(
            f"{base_url}{Config.ENDPOINTS['get'].format(id=entity_id)}",
            timeout=Config.TIMEOUT,
        )
        assert response.status_code == 200

        data = response.json()
        obj = Entity(**data)
        assert obj.title == payload["title"]
        assert obj.addition.additional_info == payload["addition"]["additional_info"]

    @allure.feature("Получение всех сущностей")
    def test_get_all_entities(self, base_url):
        response = requests.post(
            f"{base_url}{Config.ENDPOINTS['get_all']}", timeout=Config.TIMEOUT
        )
        assert response.status_code == 200

        data = response.json()

        
        if isinstance(data, dict) and "entity" in data:
            entities = data["entity"]
        else:
            entities = data

        assert isinstance(
            entities, list
        ), f"Ожидался список, а получен {type(entities)}: {data}"

        if entities:
            Entity(**entities[0])

    @allure.feature("Обновление сущности")
    def test_patch_entity(self, base_url, entity):
        entity_id, _ = entity
        payload = {
            "addition": {"additional_info": "Обновлено", "additional_number": 777},
            "important_numbers": [99],
            "title": "Измененная сущность",
            "verified": False,
        }

        with allure.step("PATCH /api/patch/{id} — обновление сущности"):
            response = requests.patch(
                f"{base_url}{Config.ENDPOINTS['patch'].format(id=entity_id)}",
                json=payload,
                timeout=Config.TIMEOUT,
            )
            assert response.status_code in (200, 204)

        with allure.step("Проверка изменений через GET"):
            updated = requests.get(
                f"{base_url}{Config.ENDPOINTS['get'].format(id=entity_id)}",
                timeout=Config.TIMEOUT,
            )
            data = updated.json()
            obj = Entity(**data)
            assert obj.title == payload["title"]
            assert obj.addition.additional_number == 777

    @allure.feature("Удаление сущности")
    def test_delete_entity(self, base_url):
        payload = {
            "addition": {"additional_info": "Удаление", "additional_number": 11},
            "important_numbers": [5],
            "title": "Удаляемая сущность",
            "verified": True,
        }
        create = requests.post(
            f"{base_url}{Config.ENDPOINTS['create']}",
            json=payload,
            timeout=Config.TIMEOUT,
        )
        entity_id = int(create.text)

        delete = requests.delete(
            f"{base_url}{Config.ENDPOINTS['delete'].format(id=entity_id)}",
            timeout=Config.TIMEOUT,
        )
        assert delete.status_code in (200, 204)

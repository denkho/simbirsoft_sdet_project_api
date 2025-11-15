import allure
import pytest
from config.config import Config
from models.models import Entity
from data.payloads import Payloads


@allure.suite("API Tests")
class TestAPI:
    @pytest.mark.critical
    @allure.feature("Создание сущности")
    @allure.title("Тест создания сущности /api/create/")
    def test_create_entity(self, client):
        payload = Payloads.CREATE_ENTITY

        with allure.step("POST /api/create — создание сущности"):
            response = client.post(Config.ENDPOINTS["create"], json=payload)
            client.check_response(response, expected_status=200)

        entity_id = int(response.text)
        assert entity_id > 0, f"Неверный ID сущности: {entity_id}"

        with allure.step("Очистка созданной сущности"):
            client.delete(Config.ENDPOINTS["delete"].format(id=entity_id))

    @pytest.mark.critical
    @allure.feature("Получение сущности по ID")
    @allure.title("Тест получения сущности по ID /api/get/{id}")
    def test_get_entity(self, client, entity):
        entity_id, payload = entity

        with allure.step(f"GET /api/get/{entity_id}"):
            response = client.get(Config.ENDPOINTS["get"].format(id=entity_id))
            client.check_response(response, expected_status=200)

            data = response.json()
            obj = Entity(**data)
            assert (
                obj.title == payload["title"]
            ), f"Ожидалось title={payload['title']}, получено {obj.title}"
            assert (
                obj.addition.additional_info == payload["addition"]["additional_info"]
            ), f"Ожидалось additional_info={payload['addition']['additional_info']}, получено {obj.addition.additional_info}"

    @pytest.mark.high
    @allure.feature("Получение всех сущностей")
    @allure.title("Тест получения всех сущностей /api/getAll")
    def test_get_all_entities(self, client):

        with allure.step("POST /api/getAll"):
            response = client.post(Config.ENDPOINTS["get_all"])
            client.check_response(response, expected_status=200)

            data = response.json()

            if isinstance(data, dict) and "entity" in data:
                entities = data["entity"]
            else:
                entities = data

            assert isinstance(
                entities, list
            ), f"Ожидался список, а получен {type(entities)}: {data}"

            if entities:
                try:
                    Entity(**entities[0])
                except Exception as e:
                    assert False, f"Ошибка десериализации сущности: {e}"

    @pytest.mark.high
    @allure.feature("Обновление сущности")
    @allure.title("Тест обновления сущности /api/patch/{id}")
    def test_patch_entity(self, client, entity):
        entity_id, _ = entity
        payload = Payloads.PATCH_ENTITY

        with allure.step("PATCH /api/patch/{id} — обновление сущности"):
            response = client.patch(
                Config.ENDPOINTS["patch"].format(id=entity_id), json=payload
            )
            client.check_response(response, expected_status=204)

        with allure.step("Проверка изменений через GET"):
            updated = client.get(Config.ENDPOINTS["get"].format(id=entity_id))
            data = updated.json()
            obj = Entity(**data)
            assert (
                obj.title == payload["title"]
            ), f"Ожидалось title={payload['title']}, получено {obj.title}"
            assert (
                obj.addition.additional_number == 777
            ), f"Ожидалось additional_number=777, получено {obj.addition.additional_number}"

    @pytest.mark.medium
    @allure.feature("Удаление сущности")
    @allure.title("Тест удаления сущности /api/delete/{id}")
    def test_delete_entity(self, client):
        payload = Payloads.SAMPLE_ENTITY

        with allure.step("Создание сущности для проверки ее удаления"):
            create = client.post(Config.ENDPOINTS["create"], json=payload)
            entity_id = int(create.text)

        with allure.step(f"Удаление сущности через DELETE /api/delete/{entity_id}"):
            delete = client.delete(Config.ENDPOINTS["delete"].format(id=entity_id))
            client.check_response(delete, expected_status=204)

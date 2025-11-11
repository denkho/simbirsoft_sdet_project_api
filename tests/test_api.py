import allure
from config.config import Config
from models.models import Entity
from data.payloads import Payloads


@allure.suite("API Tests")
class TestAPI:

    @allure.title("Создание сущности")
    def test_create_entity(self, client):
        payload = Payloads.CREATE_ENTITY

        with allure.step("POST /api/create — создание сущности"):
            response = client.post(Config.ENDPOINTS["create"], json=payload)
            assert (
                response.status_code == 200
            ), f"Ошибка создания сущности: {response.text}"

        entity_id = int(response.text)
        assert entity_id > 0, f"Неверный ID сущности: {entity_id}"

        with allure.step("Очистка созданной сущности"):
            client.delete(Config.ENDPOINTS["delete"].format(id=entity_id))

    @allure.title("Получение сущности по ID")
    def test_get_entity(self, client, entity):
        entity_id, payload = entity
        response = client.get(Config.ENDPOINTS["get"].format(id=entity_id))
        assert (
            response.status_code == 200
        ), f"Ошибка получения сущности {entity_id}: {response.text}"

        data = response.json()
        obj = Entity(**data)
        assert (
            obj.title == payload["title"]
        ), f"Ожидалось title={payload['title']}, получено {obj.title}"
        assert (
            obj.addition.additional_info == payload["addition"]["additional_info"]
        ), f"Ожидалось additional_info={payload['addition']['additional_info']}, получено {obj.addition.additional_info}"

    @allure.title("Получение всех сущностей")
    def test_get_all_entities(self, client):
        response = client.post(Config.ENDPOINTS["get_all"])
        assert (
            response.status_code == 200
        ), f"Ошибка получения всех сущностей: {response.text}"

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

    @allure.title("Обновление сущности")
    def test_patch_entity(self, client, entity):
        entity_id, _ = entity
        payload = Payloads.PATCH_ENTITY

        with allure.step("PATCH /api/patch/{id} — обновление сущности"):
            response = client.patch(
                Config.ENDPOINTS["patch"].format(id=entity_id), json=payload
            )
            assert response.status_code in (
                200,
                204,
            ), f"Ошибка обновления сущности {entity_id}: {response.text}"

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

    @allure.title("Удаление сущности")
    def test_delete_entity(self, client):
        payload = Payloads.SAMPLE_ENTITY

        create = client.post(Config.ENDPOINTS["create"], json=payload)
        entity_id = int(create.text)

        delete = client.delete(Config.ENDPOINTS["delete"].format(id=entity_id))
        assert delete.status_code in (
            200,
            204,
        ), f"Ошибка удаления сущности {entity_id}: {delete.text}"

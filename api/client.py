import allure
import logging
import requests
from config.config import Config


# Логирование
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


if not logger.hasHandlers():
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    fh = logging.FileHandler(Config.LOG_PATH, mode="a", encoding="utf-8")
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


class APIClient:
    def __init__(self, base_url=Config.HOST):
        self.base_url = base_url
        self.session = requests.Session()
        self.timeout = Config.TIMEOUT

    def _request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"

        logger.info(f"REQUEST: {method.upper()} {url}")

        if "json" in kwargs:
            logger.info(f"PAYLOAD: {kwargs['json']}")

        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs,
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"NETWORK ERROR: {e}")
            raise RuntimeError(f"Ошибка сети при выполнении запроса {e}")

        logger.info(f"STATUS: {response.status_code}")
        logger.info(f"BODY: {response.text}")


        allure.attach(
            response.text,
            name="Response Body",
            attachment_type=allure.attachment_type.JSON,
        )

        
        if response.status_code >= 500:
            raise RuntimeError(
                f"Ошибка сервера {response.status_code}: {response.text}"
            )
        return response

    # Методы
    def post(self, endpoint, **kwargs):
        return self._request("post", endpoint, **kwargs)

    def get(self, endpoint, **kwargs):
        return self._request("get", endpoint, **kwargs)

    def patch(self, endpoint, **kwargs):
        return self._request("patch", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._request("delete", endpoint, **kwargs)
    
    def check_response(self, response, expected_status=200):
        """Проверка кода ответа и вывод текста ошибки"""
        if response.status_code != expected_status:
            raise AssertionError(
                f"Ожидался статус {expected_status}, "
                f"получен {response.status_code}: {response.text}"
            )

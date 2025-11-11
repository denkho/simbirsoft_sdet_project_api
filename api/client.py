import requests
from config.config import Config


class APIClient:
    def __init__(self, base_url=Config.HOST):
        self.base_url = base_url

    def post(self, endpoint, json=None):
        return requests.post(
            f"{self.base_url}{endpoint}", json=json, timeout=Config.TIMEOUT
        )

    def get(self, endpoint):
        return requests.get(f"{self.base_url}{endpoint}", timeout=Config.TIMEOUT)

    def patch(self, endpoint, json=None):
        return requests.patch(
            f"{self.base_url}{endpoint}", json=json, timeout=Config.TIMEOUT
        )

    def delete(self, endpoint):
        return requests.delete(f"{self.base_url}{endpoint}", timeout=Config.TIMEOUT)

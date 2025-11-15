import os


class Config:
    HOST = "http://localhost:8080"

    ENDPOINTS = {
        "create": "/api/create",
        "delete": "/api/delete/{id}",
        "get": "/api/get/{id}",
        "get_all": "/api/getAll",
        "patch": "/api/patch/{id}",
    }

    TIMEOUT = 10

    LOG_DIR = "logs"
    LOG_FILE = "api_client.log"
    LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)
    os.makedirs(LOG_DIR, exist_ok=True) 

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

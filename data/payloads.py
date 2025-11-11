class Payloads:
    SAMPLE_ENTITY = {
        "addition": {"additional_info": "Test entity", "additional_number": 1321},
        "importan_numbers": [13, 31, 66, 131],
        "title": "Entity Title",
        "verified": True,
    }

    CREATE_ENTITY = {
        "addition": {"additional_info": "Создание", "additional_number": 999},
        "important_numbers": [1, 2, 3],
        "title": "Новая сущность",
        "verified": True,
    }

    PATCH_ENTITY = {
        "addition": {"additional_info": "Обновлено", "additional_number": 777},
        "important_numbers": [99],
        "title": "Измененная сущность",
        "verified": False,
    }

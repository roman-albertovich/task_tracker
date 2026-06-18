def test_create_task_api_success(client):
    """Интеграционный тест: успешное создание задачи через HTTP POST"""
    payload = {
        "name": "Интеграционный тест",
        "description": "Проверить сквозной сценарий работы API и PostgreSQL",
        "author": "QA Automation Lead"
    }

    # Делаем имитиацю POST-запроса на эндпойнт приложения
    response = client.post("/tasks", json=payload)

    # Проверяем код ответа (Ожидаем 201)
    assert response.status_code == 201

    # Парсим JSON-ответ сервера
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]
    assert data["author"] == payload["author"]
    assert data["status"] == "NEW"
    assert "id" in data # Проверяем, что база сгененировала UUID
    assert "date_created" in data
    assert "date_updated" in data

def test_get_tasks_api(client):
    """Интеграционный тест: получение списка задач"""
    # Сначала создадим одну задачу, чтобы список не был пустым
    payload = {
        "name": "Задача для проверки GET",
        "author": "Support Engineer"
    }
    client.post("/tasks", json=payload)

    # Выполянем GET-запрос
    response = client.get("/tasks")

    assert response.status_code == 200
    data = response.json()

    # Ожидаем, что вернулся массив (list) и в нём есть как минимум одна наша задача
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[-1]["name"] == payload["name"]
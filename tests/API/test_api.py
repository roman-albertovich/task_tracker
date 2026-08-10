import allure

@allure.feature("Tasks API")
@allure.story("Create a new task")
def test_create_task_api_success(client):
    """Интеграционный тест: успешное создание задачи через HTTP POST"""
    with allure.step("Fill payload"):
        payload = {
        "name": "Интеграционный тест",
        "description": "Проверить сквозной сценарий работы API и PostgreSQL",
        "author": "QA Automation Lead"
        }

    with allure.step("Imitation POST in endpoint app"):
        response = client.post("/tasks", json=payload)

    with allure.step("Chek answer code 201"):
        assert response.status_code == 201

    with allure.step("Parsing JSON data of server"):
        data = response.json()
        assert data["name"] == payload["name"]
        assert data["description"] == payload["description"]
        assert data["author"] == payload["author"]
        assert data["status"] == "NEW"
        assert "id" in data # Проверяем, что база сгененировала UUID
        assert "date_created" in data
        assert "date_updated" in data

@allure.story("Get a tasks list")
def test_get_tasks_api(client):
    """Интеграционный тест: получение списка задач"""
    # Сначала создадим одну задачу, чтобы список не был пустым
    with allure.step("Fill payload a new task"):
        payload = {
        "name": "Задача для проверки GET",
        "author": "Support Engineer"
        }
    with allure.step("Send request to create the task"):
        client.post("/tasks", json=payload)

    with allure.step("Send GET request to find the task"):
        response = client.get("/tasks")

    with allure.step("Check answer code 200"):
        assert response.status_code == 200
    data = response.json()

    with allure.step("Check result list"):
    # Ожидаем, что вернулся массив (list) и в нём есть как минимум одна наша задача
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[-1]["name"] == payload["name"]
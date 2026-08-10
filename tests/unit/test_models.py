import pytest
from pydantic import ValidationError
from app.models import TaskCreate
import allure

@allure.feature("Test models")
@allure.story("Create a new valid task")
@allure.severity(allure.severity_level.CRITICAL)
def test_task_create_success():
    with allure.step("Fill payload"):
        """Позитивный тест: валидные данные должны успешно проходить проверку"""
        payload = {
        "name": "Написать автотесты",
        "description": "Покрыть unit-тестами слой валидации Pydantic",
        "author": "Инженер поддержки"
        }

    with allure.step("Initializing the model"):
        # Инициализурем модель
        task = TaskCreate(**payload)
    with allure.step("Check matching value the payload"):
        # Проверяем, что Pydantic правильно сопоставил поля
        assert task.name == payload["name"]
        assert task.description == payload["description"]
        assert task.author == payload["author"]

@allure.feature("Test models")
@allure.story("Create a new task with invalid 'name'")
@allure.severity(allure.severity_level.NORMAL)
def test_task_create_name_too_long():
    with allure.step("Fill invalid name"):
        """Негативный тест: имя задачи ровно 101 символ (граница > 100)"""
        invalid_name = "X" * 101  # Генерируем слишком длинную строку

    with allure.step("Fill payload"):
        payload = {
        "name": invalid_name,
        "description": "Тест граничных значений",
        "author": "QA"
        }
    with allure.step("Check that the ValidationError is received"):
        # Ожидаем, что Pydantic выбросит ошибку ValidationError
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(**payload)

    with allure.step("Check that the ValidationError for 'name' value"):
        # Проверяем, что ошибка локализована именно на поле 'name'
        assert "name" in str(exc_info.value)

@allure.feature("Test models")
@allure.story("Create a new task with invalid 'author'")
@allure.severity(allure.severity_level.NORMAL)
def test_task_create_author_empty():
    with allure.step("Fill payload with empty author"):
        """негативный тест: пустая строка в авторе (min_leght=1)"""
        payload = {
        "name":"Валидная задача",
        "description": "Описание",
        "author": ""
        }

    with allure.step("Check that the ValidationError is received"):
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(**payload)

    with allure.step("Check that the ValidationError for 'author' value"):
        assert "author" in str(exc_info.value)

@allure.feature("Test models")
@allure.story("Create a new task with invalid 'description'")
@allure.severity(allure.severity_level.NORMAL)
def test_task_create_description_too_long():
    with allure.step("Fill payload with too long description"):
        """Негативный тест: описание ровно 541 символ (граница > 540)"""
        payload = {
        "name": "Валидная задача",
        "description": "D" * 541,
        "author": "Tech Support"
        }

    with allure.step("Check that the ValidationError is received"):
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(**payload)

    with allure.step("Check that the ValidationError for 'description' value"):
        assert "description" in str(exc_info.value)
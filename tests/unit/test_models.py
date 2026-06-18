import pytest
from pydantic import ValidationError
from app.models import TaskCreate

def test_task_create_success():
    """Позитивный тест: валидные данные должны успешно проходить проверку"""
    payload = {
        "name": "Написать автотесты",
        "description": "Покрыть unit-тестами слой валидации Pydantic",
        "author": "Инженер поддержки"
    }

    # Инициализурем модель
    task = TaskCreate(**payload)

    # Проверяем, что Pydantic правильно сопоставил поля
    assert task.name == payload["name"]
    assert task.description == payload["description"]
    assert task.author == payload["author"]


def test_task_create_name_too_long():
    """Негативный тест: имя задачи ровно 101 символ (граница > 100)"""
    invalid_name = "X" * 101  # Генерируем слишком длинную строку

    payload = {
        "name": invalid_name,
        "description": "Тест граничных значений",
        "author": "QA"
    }

    # Ожидаем, что Pydantic выбросит ошибку ValidationError
    with pytest.raises(ValidationError) as exc_info:
        TaskCreate(**payload)

    # Проверяем, что ошибка локализована именно на поле 'name'
    assert "name" in str(exc_info.value)


def test_task_create_author_empty():
    """негативный тест: пустая строка в авторе (min_leght=1)"""
    payload = {
        "name":"Валидная задача",
        "description": "Описание",
        "author": ""
    }

    with pytest.raises(ValidationError) as exc_info:
        TaskCreate(**payload)

    assert "author" in str(exc_info.value)


def test_task_create_description_too_long():
    """Негативный тест: описание ровно 541 символ (граница > 540)"""
    payload = {
        "name": "Валидная задача",
        "description": "D" * 541,
        "author": "Tech Support"
    }

    with pytest.raises(ValidationError) as exc_info:
        TaskCreate(**payload)

    assert "description" in str(exc_info.value)
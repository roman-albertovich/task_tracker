import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import DATABASE_URL, get_db
from app.main import app

engine = create_engine(DATABASE_URL)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Фикстура, которая создаёт изолированную транзацию в БД для каждого теста"""
    connection = engine.connect()
    # Стартуем транзацкцию на уровене соединения
    transaction = connection.begin()
    # Связываем сесию SQLAlchemy с этим соединением
    session = TestingSession(bind=connection)

    yield session

    # По окончанию теста откатываем все изменения. В БД ничего сохранится физически.
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Фикстура для HTTP-клиента, которая подменяет реализацию сессию БД на тестовую"""
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    # Переопределяем зависимость get_db в FastAPI на нашу тестовую транзационную сессию
    app.dependency_overrides[get_db] = _get_test_db

    with TestClient(app) as test_client:
        yield test_client

    # Сбрасываем переопределние после теста
    app.dependency_overrides.clear()
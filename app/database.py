from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL подключения к локальной PostgreSQL
# Формат: postgresql://пользователь:пароль@хост:порт/имя_бд
DATABASE_URL = "postgresql://myuser:mypassword@localhost/mydatabase"

# Создаём движок SQLAlchemy
engine = create_engine(DATABASE_URL)

# Создаём фабрику сессий для выполнения запросов
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency (зависимость) для FastAPI
# Он будет открывать сессию при каждом запросе к API и закрывать её после завершения.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

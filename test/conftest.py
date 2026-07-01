import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine , StaticPool
from sqlalchemy.orm import sessionmaker
from database.connect import Base , get_db
from main import app

TEST_DB_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DB_URL,connect_args={"check_same_thread": False},poolclass=StaticPool)
TestingSessionLocal = sessionmaker(bind = test_engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client ():
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
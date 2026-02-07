import pytest
from fastapi.testclient import TestClient

from chinese_practice.db import Base, engine
from chinese_practice.main import create_app


@pytest.fixture()
def client() -> TestClient:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return TestClient(create_app())


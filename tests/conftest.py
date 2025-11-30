"""
Configuration globale pour pytest
"""

import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services_crud.auth import hash_password
from models import Employee


# Configuration des marqueurs pytest
def pytest_configure(config):
    pass


@pytest.fixture(scope="session")
def test_db_engine():
    engine = create_engine(
        os.getenv("DATABASE_URL"),
        pool_pre_ping=True,
    )
    return engine


@pytest.fixture(scope="function")
def test_db_session(test_db_engine):
    """Fixture pour la session de base de données de test"""
    from database import BaseSQL

    # Crée toutes les tables
    BaseSQL.metadata.create_all(bind=test_db_engine)

    # Crée une session
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_db_engine
    )
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        # Supprime toutes les tables après chaque test
        BaseSQL.metadata.drop_all(bind=test_db_engine)


@pytest.fixture(scope="function")
def client():
    """Fixture pour TestClient"""
    from main import app

    return TestClient(app)


@pytest.fixture(scope="session")
def test_employee_password():
    """Fixture pour le mot de passe de test"""
    return "testpassword"


@pytest.fixture(scope="session")
def test_employee_name():
    """Fixture pour le nom d'utilisateur de test"""
    return "testname"


@pytest.fixture(scope="function")
def test_employee(test_db_session, test_employee_password, test_employee_name, test_role):
    """Fixture pour un utilisateur de test"""

    employee = Employee(name=test_employee_name, password=hash_password(test_employee_password), role=test_role)
    test_db_session.add(employee)
    test_db_session.commit()
    test_db_session.refresh(employee)

    yield employee

    test_db_session.delete(employee)
    test_db_session.commit()

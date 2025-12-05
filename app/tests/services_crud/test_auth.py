
from services_crud.auth import (
    hash_password,
    check_password,
    generate_access_token,
    _encode_jwt,
    decode_jwt,
)
from exceptions.employee import EmployeeNotFound, IncorrectPassword
from models.employee import Employee
from fastapi import HTTPException
import pytest
import serializers


def test_hash_password():
    """Test de la fonction hash_password"""
    password = "testpassword"
    hashed_password = hash_password(password)

    assert hashed_password is not None
    assert isinstance(hashed_password, str)
    assert hashed_password != password


def test_check_password_correct():
    """Test que check_password retourne True avec le bon mot de passe"""
    password = "testpassword"
    hashed_password = hash_password(password)

    assert check_password(password, hashed_password) is True


def test_check_password_incorrect():
    """Test que check_password retourne False avec un mauvais mot de passe"""
    password = "testpassword"
    hashed_password = hash_password(password)

    assert check_password("wrongpassword", hashed_password) is False


def test_check_password_empty():
    """Test que check_password retourne False avec un mot de passe vide"""
    password = "testpassword"
    hashed_password = hash_password(password)

    assert check_password("", hashed_password) is False


def test_check_password_invalid_hash():
    """Test que check_password raise une erreur si le hash est invalide"""
    password = "testpassword"
    with pytest.raises(ValueError):
        check_password(password, "invalid_hash_format")


def test_generate_access_token(test_db_session, test_employee):
    """Test que generate_access_token retourne un token JWT"""
    user_employee = Employee(name="testuser", password="testpassword",role="Cashier")
    token = generate_access_token(test_db_session, user_employee)

    assert token is not None
    assert isinstance(token, str)

def test_generate_access_token(test_db_session, test_employee):
    """Test que generate_access_token retourne un token JWT"""
    
    # 1. On prépare les données de login. 
    user_login_data = serializers.EmployeeCreate(
        name=test_employee.name,
        password="testpassword", # Le mot de passe brut
        role=test_employee.role
    )

    # 2. Appel de la fonction
    token = generate_access_token(test_db_session, user_login_data)

    # 3. Vérifications
    assert token is not None
    assert isinstance(token, str)


def test_generate_access_token_user_not_found(test_db_session):
    """Test que generate_access_token raise une erreur si l'utilisateur n'est pas trouvé"""
    user_employee = Employee(name="testuser", password="testpassword",role="Cashier")
    with pytest.raises(EmployeeNotFound):
        generate_access_token(test_db_session, user_employee)


def test_generate_access_token_incorrect_password(test_db_session, test_employee):
    """Test que generate_access_token raise une erreur si le mot de passe est incorrect"""
    user_login = Employee(name=test_employee.name, password="wrongpassword", role=test_employee.role)
    with pytest.raises(IncorrectPassword):
        generate_access_token(test_db_session, user_login)


def test_encode_jwt_correct(test_employee):
    """Test que encode_jwt retourne un token JWT"""
    token = _encode_jwt(test_employee)
    assert token is not None
    assert isinstance(token, str)

def test_decode_jwt_correct(test_employee):
    """Test que decode_jwt retourne un utilisateur"""
    token = _encode_jwt(test_employee)
    employee = decode_jwt(token)
    
    assert employee is not None
    assert isinstance(employee, dict)
    assert employee["employee_id"] == str(test_employee.id)


def test_decode_jwt_invalid_token(test_employee):
    """Test que decode_jwt raise une erreur si le token est invalide"""
    token = "invalid_token"
    with pytest.raises(HTTPException) as err:
        decode_jwt(token)
    assert err.value.status_code == 401



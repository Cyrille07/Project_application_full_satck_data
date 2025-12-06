import pytest
from fastapi import HTTPException
from routers import utils
from services_crud.auth import _encode_jwt, JWT_SECRET_KEY, JWT_SECRET_ALGORITHM
from datetime import datetime, timedelta
import jwt

class MockEmployee:
    def __init__(self, id):
        self.id = id

# ==========================================
# TEST 1 : Token Valide (Cas Nominal)
# ==========================================
@pytest.mark.asyncio
async def test_get_employee_id_success():
    """Teste qu'un token valide renvoie bien l'ID."""
    
    # 1. Arrange
    fake_id = "1234-5678-9012"
    employee = MockEmployee(id=fake_id)
    token_string = _encode_jwt(employee)
    
    # CORRECTION : On passe une STRING brute "Bearer <token>"
    # Car votre utils.py fait .startswith("Bearer ")
    auth_header = f"Bearer {token_string}"
    
    # 2. Act
    result_id = await utils.get_employee_id(auth_header)
    
    # 3. Assert
    assert result_id == fake_id


# ==========================================
# TEST 2 : Token Invalide
# ==========================================
@pytest.mark.asyncio
async def test_get_employee_id_invalid_signature():
    """Teste qu'un token modifié/bidon lève une erreur."""
    
    bad_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.Et9HFh..."
    # On passe une STRING
    auth_header = f"Bearer {bad_token}"
    
    with pytest.raises(HTTPException) as excinfo:
        await utils.get_employee_id(auth_header)
    
    assert excinfo.value.status_code in [401, 403]


# ==========================================
# TEST 3 : Token Expiré
# ==========================================
@pytest.mark.asyncio
async def test_get_employee_id_expired_token():
    """Teste qu'un token expiré est rejeté."""
    
    expired_payload = {
        "employee_id": "123",
        "exp": datetime.utcnow() - timedelta(minutes=10)
    }
    
    expired_token = jwt.encode(expired_payload, JWT_SECRET_KEY, algorithm=JWT_SECRET_ALGORITHM)
    # On passe une STRING
    auth_header = f"Bearer {expired_token}"
    
    with pytest.raises(HTTPException) as excinfo:
        await utils.get_employee_id(auth_header)
        
    assert excinfo.value.status_code in [401, 403]


# ==========================================
# TEST 4 : Payload incomplet
# ==========================================
@pytest.mark.asyncio
async def test_get_employee_id_missing_id_in_token():
    """Teste un token valide mais sans 'employee_id'."""
    
    payload = {
        "sub": "wrong_key", 
        "exp": datetime.utcnow() + timedelta(minutes=10)
    }
    
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_SECRET_ALGORITHM)
    # On passe une STRING
    auth_header = f"Bearer {token}"
    
    with pytest.raises(HTTPException):
        await utils.get_employee_id(auth_header)
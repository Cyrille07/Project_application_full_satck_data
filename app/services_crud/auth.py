import base64
import hashlib
import hmac
import os

import jwt
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

import models
from exceptions.employee import EmployeeNotFound, IncorrectPassword, IncorrectRole
from serializers import EmployeeCreate



JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_SECRET_ALGORITHM = os.getenv("JWT_SECRET_ALGORITHM") 
JWT_TIME_DELAY_TOKEN = os.getenv("JWT_TIME_DELAY_TOKEN")


def _encode_jwt(employee: EmployeeCreate) -> str:
    expire = datetime.utcnow() + timedelta(minutes=float(JWT_TIME_DELAY_TOKEN))
    payload={
                "employee_id": str(employee.id),
                "exp": expire, 
            }
    
    return jwt.encode( 
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_SECRET_ALGORITHM,
        )


def decode_jwt(token: str) :
    try:
        auth = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_SECRET_ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError as err:
        raise HTTPException(status_code=401, detail=f"Invalid token: '{err}'")

    return auth



def generate_access_token(db: Session, employee_login: EmployeeCreate ):
    password = employee_login.password
    role = employee_login.role
    name = employee_login.name
    db_employee = ( db.query(models.Employee).filter(models.Employee.name == name).first() )

    if not db_employee:
        raise EmployeeNotFound

    if not check_password(password, db_employee.password):
        raise IncorrectPassword
    
    if str(db_employee.role) != str(role) :
        raise IncorrectRole

    return _encode_jwt(db_employee)



def hash_password(password: str, iterations: int = 600_000) -> str:
    # Generate a random 16-byte salt
    salt = os.urandom(16)
    # Derive the hash using PBKDF2-HMAC-SHA256
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    # Encode salt and hash in base64 for safe storage
    salt_b64 = base64.b64encode(salt).decode("utf-8")
    hash_b64 = base64.b64encode(dk).decode("utf-8")
    # Return full formatted hash string
    return f"pbkdf2_sha256${iterations}${salt_b64}${hash_b64}"



def check_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, iterations, salt_b64, hash_b64 = stored_hash.split("$")
    except Exception:
        raise ValueError("Invalid hash format")

    iterations = int(iterations)
    salt = base64.b64decode(salt_b64)
    stored_dk = base64.b64decode(hash_b64)

    new_dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)

    return hmac.compare_digest(stored_dk, new_dk)

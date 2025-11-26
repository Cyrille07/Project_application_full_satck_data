from typing import Union

from fastapi import Header, HTTPException

from services_crud.auth import decode_jwt

"""
async def verify_authorization_header(
    authorization: str = Header(...),
) -> dict[str, Union[int, dict[str, Union[list[str], int, str]]]]:
    
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No authorization header")

    return decode_jwt(authorization.split("Bearer ")[1])


async def get_employee_id(authorization: str = Header(...)) -> str:
    auth = await verify_authorization_header(authorization)
    try:
        employee_id = str(auth["employee_id"])
    except KeyError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return employee_id


async def verify_authorization_header(
    authorization: str = Header(None),
)-> dict[str, Union[int, dict[str, Union[list[str], int, str]]]]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No authorization header")

    return decode_jwt(authorization.split("Bearer ")[1])


def get_employee_id(authorization: str) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No authorization header")

    token = authorization.split("Bearer ")[1]
    auth = decode_jwt(token)

    try:
        return str(auth["employee_id"])
    except KeyError:
        raise HTTPException(status_code=401, detail="Invalid token")



"""
async def verify_authorization_header(
    authorization: str = Header(...),
) -> dict[str, Union[int, dict[str, Union[list[str], int, str]]]]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No authorization header")

    return decode_jwt(authorization.split("Bearer ")[1])


async def get_employee_id(authorization: str = Header(...)) -> str:
    auth = await verify_authorization_header(authorization)
    try:
        employee_id = str(auth["employee_id"])
    except KeyError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return employee_id


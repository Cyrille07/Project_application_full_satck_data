from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from routers import utils
import database
import serializers
from exceptions.employee import EmployeeNotFound, IncorrectRole
from services_crud import employee as employee_service

employee_router = APIRouter(prefix="/employees")
security = HTTPBearer()

# -----------------------------------------
# CREATE EMPLOYEE
# -----------------------------------------
@employee_router.post("/", tags=["employees"], response_model=serializers.EmployeeOutput)
async def create_employee(
    employee: serializers.EmployeeCreate,
    db: Session = Depends(database.get_db)
):
    try:
        return employee_service.create_employee(db=db, employee=employee)
    except IncorrectRole:
        raise HTTPException(status_code=401, detail="Role not defined, you should choose between : [Cashier, Server, Cook, Chief_of_resto]") 



# -----------------------------------------
# GET 
# -----------------------------------------

# GET EMPLOYEE BY ID
@employee_router.get("/{employee_id}", tags=["employees"], response_model=serializers.EmployeeOutput)
async def get_employee_by_id(employee_id: str ,db: Session = Depends(database.get_db) ):
    try:
        return employee_service.get_employee_by_id(employee_id= employee_id, db=db)
    except EmployeeNotFound:
        raise HTTPException(status_code=404, detail="employee not Found")


# GET ALL EMPLOYEES
@employee_router.get("/", tags=["employees"], response_model=list[serializers.EmployeeOutput])
async def get_all_employees(db: Session = Depends(database.get_db)):
    return employee_service.get_all_employees(db=db)



# -----------------------------------------
# DELETE 
# -----------------------------------------
#----Delete employee by id  
#Supprime uniquement si ya pas de taches 
@employee_router.delete("/{employee_id}", tags=["employees"])
async def delete_employee_by_id(employee_id: str, db: Session = Depends(database.get_db)):
    try:
        return employee_service.delete_employee_by_id(employee_id=employee_id, db=db)
    except EmployeeNotFound as e:
        raise HTTPException(status_code=404, detail="Employee not Found")


#---Delete all employee    
#Uniquement le chef du resto peut le faire
#Double verfifaction par token et par role

"""
@employee_router.delete("/delete_all/{employee_id}", dependencies=[Depends(security)], tags=["employees"])
async def delete_all_employee(employee_id: str = Depends(utils.get_employee_id), db: Session = Depends(database.get_db)):
    try:
        deleted_employees = employee_service.delete_all_employees(employee_id=employee_id, db=db)
        return {"message": f"Deleted {len(deleted_employees)} employees successfully"}
    except IncorrectRole as e:
        raise HTTPException(status_code=403, detail="Only the Chief of resto can delete the users")  # 403 Forbidden
    except EmployeeNotFound:
        raise HTTPException(status_code=404, detail="Employee not Found")
    

"""

@employee_router.delete("/delete_all/{employee_id}", dependencies=[Depends(security)], tags=["employees"])
async def delete_all_employee(
    employee_id: str,  # ID fourni dans l’URL
    token_employee_id: str = Depends(utils.get_employee_id),  # ID issu du JWT
    db: Session = Depends(database.get_db)
):
    try:
        if employee_id != token_employee_id:
            raise HTTPException(
                status_code=403,
                detail="Employee ID mismatch with token — unauthorized operation."
            )

        deleted_employees = employee_service.delete_all_employees(employee_id=employee_id, db=db)
        return {"message": f"Deleted {len(deleted_employees)} employees successfully"}

    except IncorrectRole:
        raise HTTPException(status_code=403, detail="Only the Chief of resto can delete the users")
    except EmployeeNotFound:
        raise HTTPException(status_code=404, detail="Employee not Found")
    

# -----------------------------------------
# UPDATE EMPLOYEE
# -----------------------------------------

@employee_router.put("/updateme", tags=["employees"], response_model=serializers.EmployeeOutput)
async def update_myself(
    employee_update: serializers.EmployeeCreate,
    db: Session = Depends(database.get_db),
    employee_id: str = Depends(utils.get_employee_id),
    
):
    try:
        return employee_service.update_employee(employee_id=employee_id, db=db , employee_update=employee_update)
    except IncorrectRole:
        raise HTTPException(status_code=403, detail="Role not defined, you should choose between : [Cashier, Server, cook, Chief_of_resto]")
    except EmployeeNotFound:
        raise HTTPException(status_code=404, detail="Employee not Found")




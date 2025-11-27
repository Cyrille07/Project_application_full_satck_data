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
    return employee_service.create_employee(db=db, employee=employee)



# -----------------------------------------
# GET 
# -----------------------------------------

# GET EMPLOYEE BY ID
@employee_router.get("/{employee_id}", tags=["employees"], response_model=serializers.EmployeeOutput)
async def get_employee_by_id(employee_id: str ,db: Session = Depends(database.get_db) ):
    return employee_service.get_employee_by_id(employee_id= employee_id, db=db)


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
    return employee_service.delete_employee_by_id(employee_id=employee_id, db=db)


#---Delete all employee    
#Uniquement le chef du resto peut le faire
#Double verfifaction par token et par role
@employee_router.delete("/delete_all/{employee_id}", dependencies=[Depends(security)], tags=["employees"])
async def delete_all_employee(employee_id: str = Depends(utils.get_employee_id), db: Session = Depends(database.get_db)):
    try:
        deleted_employees = employee_service.delete_all_employees(employee_id=employee_id, db=db)
        return {"message": f"Deleted {len(deleted_employees)} employees successfully"}
    except IncorrectRole as e:
        raise HTTPException(status_code=403, detail="Only the Chief of resto can delete the users")  # 403 Forbidden
    except EmployeeNotFound:
        raise HTTPException(status_code=404, detail="User not Found")




# -----------------------------------------
# UPDATE EMPLOYEE
# -----------------------------------------

@employee_router.put("/updateme", tags=["employees"], response_model=serializers.EmployeeOutput)
async def update_myself(
    employee_update: serializers.EmployeeCreate,
    employee_id: str = Depends(utils.get_employee_id),
    db: Session = Depends(database.get_db)
):

    return employee_service.update_employee(
        employee_id=employee_id,
        db=db,
        employee=employee_update
    )


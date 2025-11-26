from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from routers import utils
import database
import serializers
from exceptions.employee import EmployeeNotFound
from services_crud import employee as employee_service

employee_router = APIRouter(prefix="/employees")


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

#Delete employee by id  #Supprime uniquement si ya pas de taches 
@employee_router.delete("/{employee_id}", tags=["employees"])
async def delete_employee_by_id(employee_id: str, db: Session = Depends(database.get_db)):
    return employee_service.delete_employee_by_id(employee_id=employee_id, db=db)


#Delete all employee    #Supprime uniquement si ya pas de taches 
@employee_router.delete("/", tags=["employees"])
async def delete_all_employee(db: Session = Depends(database.get_db)):
    return employee_service.delete_all_employees(db=db)





# -----------------------------------------
# UPDATE EMPLOYEE
# -----------------------------------------
#fonctionnel mais à modifier

@employee_router.put("/updateme", tags=["employees"],
                     response_model=serializers.EmployeeOutput)
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


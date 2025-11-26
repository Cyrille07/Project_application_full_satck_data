from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
import serializers
from exceptions.employee import EmployeeNotFound
from services_crud.auth import hash_password


#--------------------------  CREATE ----------------------------------
#Créer un employé
#Uniquemement certains roles sont autorisés
#Les noms sont uniques , vérifie si un employé avec ce nom n'existe pas déja
def create_employee(db: Session, employee: serializers.EmployeeCreate) -> models.Employee:
    
    authorized_role = ["Cashier", "Server", "Cook", "Chief_of_resto"]

    exist_db_employee = db.query(models.Employee).filter(models.Employee.name == employee.name ).first()
    if exist_db_employee :
        raise  HTTPException(status_code=401, detail ="Employee with this name already exist")

    if employee.role not in authorized_role:
        raise  HTTPException(status_code=401, detail="Role not defined, you should choose between : [Cashier, Server, cook, Chief_of_resto]") 
    
    new_db_employee = models.Employee(name=employee.name, password=hash_password(employee.password), role=employee.role )

    db.add(new_db_employee)
    db.commit()
    db.refresh(new_db_employee)
    return new_db_employee



#----------------------------  GET ----------------------------------
#Get un employé selon son id 
#fonction  utile pour les autres 
#permet de retouver un employee et lance l'erreur s'il n'est pas trouvé
def get_employee_by_id(employee_id: str, db: Session) -> models.Employee:
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not db_employee:
        raise EmployeeNotFound
    return db_employee




#Get tous les employés de la db
def get_all_employees(db: Session, skip: int = 0, limit: int = 10) -> list[models.Employee]:
    records = db.query(models.Employee).offset(skip).limit(limit).all()
    for record in records:
        record.id = str(record.id)
    return records



#----------------------------  UPDATE ----------------------------------
def update_employee(employee_id: str, db: Session, employee: serializers.EmployeeCreate) -> models.Employee:
    db_employee = get_employee_by_id(employee_id, db) #peut raise employeenotfound

    authorized_role = ["Cashier", "Server", "Cook", "Chief_of_resto"]
    if employee.role not in authorized_role:
        raise  HTTPException(status_code=401, detail="Role not defined, you should choose between : [Cashier, Server, cook, Chief_of_resto]") 

    db_employee.name = employee.name
    db_employee.password = hash_password(employee.password)
    db_employee.role = employee.role

    db.commit()
    db.refresh(db_employee)
    return db_employee


#----------------------------  DELETE ----------------------------------

#Un employé qui a donné des taches ou reçues des taches ne peut PAS être supprimé
#Il faut que les champs tasks_written et tasks_received soient VIDES

def delete_employee_by_id(employee_id: str, db: Session) -> models.Employee:
    db_employee = get_employee_by_id(employee_id, db=db)
    
    if db_employee.tasks_written !=[] :
        raise HTTPException(
            status_code=403, detail="impossible to delete the employee: name '"
            + str(db_employee.name) + "', ID: '"+ str(db_employee.id)+"', first DELETE his given tasks")
    
    if db_employee.tasks_received !=[]:
        raise HTTPException(
            status_code=403, detail="impossible to delete the employee: name '"
            + str(db_employee.name) + "', ID: '"+ str(db_employee.id)+"', first DELETE the tasks he has to done. NEVER SKIP JOB !")

    db.delete(db_employee)  
    db.commit()
    return db_employee


def delete_all_employees(db: Session) -> list[models.Employee]:
    records = db.query(models.Employee).all()  
    for record in records:
        delete_employee_by_id(record.id, db=db)
    db.commit()
    return records

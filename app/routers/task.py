from fastapi.security import HTTPBearer
import models
import serializers
import database
from fastapi import APIRouter, Depends, HTTPException
from routers import utils
from exceptions.task import TaskNotFound, TaskAlreadyExists, WrongAuthor
from exceptions.employee import EmployeeNotFound, IncorrectRole
from serializers.task import TaskOutput
from services_crud import task as task_service
from sqlalchemy.orm import Session

task_router = APIRouter(prefix="/tasks")
security=HTTPBearer()

# -----------------------------------------
# CREATE TASK
# -----------------------------------------
@task_router.post("/", tags=["tasks"])
async def create_task(task: serializers.TaskCreate, db: Session = Depends(database.get_db)):
    try:
        return task_service.create_task(task=task, db=db)
    except EmployeeNotFound:
        raise HTTPException(status_code=404, detail="Employee not found")
    except TaskAlreadyExists:
        raise HTTPException(status_code=409, detail="Task already exists")


# -----------------------------------------
# GET ALL TASKS
# -----------------------------------------
@task_router.get("/", tags=["tasks"], response_model=list[TaskOutput])
async def get_all_tasks(db: Session = Depends(database.get_db)):
    return task_service.get_all_tasks(db=db)


# -----------------------------------------
# GET TASK by id
# -----------------------------------------
@task_router.get("/{task_id}", tags=["tasks"], response_model=TaskOutput)
async def get_task_by_id(task_id: str, db: Session = Depends(database.get_db) ):
    try:
        task = task_service.get_task_by_id(task_id=task_id, db=db)
        return task
    except TaskNotFound:
        raise HTTPException(status_code=404, detail="Tasks not found")



# -----------------------------------------
# GET TASK BY AUTHOR id
# -----------------------------------------
@task_router.get("/taskauthor/{author_id}", tags=["tasks"], response_model=list[TaskOutput])
async def get_task_by_author_id(author_id: str, db: Session = Depends(database.get_db) ):
    try:
        return task_service.get_tasks_by_author_id(author_id=author_id, db=db)
    except EmployeeNotFound:
        raise HTTPException(status_code=404, detail="Employee id not found")
    except TaskNotFound:
        raise HTTPException(status_code=404, detail="Has no written Tasks")


# -----------------------------------------
# GET TASK BY RECIPIENT id
# -----------------------------------------
@task_router.get("/taskrecipient/{recipient_id}", tags=["tasks"], response_model=list[TaskOutput])
async def get_task_by_recipient_id(recipient_id: str, db: Session = Depends(database.get_db) ):
    try:
        return task_service.get_tasks_by_recipient_id(recipient_id=recipient_id, db=db)
    except EmployeeNotFound:
        raise HTTPException(status_code=404, detail="Employee id not found")
    except TaskNotFound:
        raise HTTPException(status_code=404, detail="Has not received Tasks")
    



# -----------------------------------------
# DELETE A SPECIFIC TASK 
# -----------------------------------------
@task_router.delete("/deltask/{task_id}", tags=["tasks"])
async def delete_task_by_id(task_id: str, db: Session = Depends(database.get_db)):
    try:
        return task_service.delete_task(task_id=task_id, db=db)
    except TaskNotFound:
        raise HTTPException(status_code=404, detail="Task not found")



# -----------------------------------------
# DELETE ALL TASKS
# -----------------------------------------

@task_router.delete("/deletealltask/{employee_id}",dependencies=[Depends(security)], tags=["tasks"])
async def delete_all_tasks(employee_id: str = Depends(utils.get_employee_id), db: Session = Depends(database.get_db)):
    try:
        return task_service.delete_all_tasks(employee_id=employee_id, db=db)
    except EmployeeNotFound:
        raise HTTPException(status_code=404, detail="Employee Not Found")
    except IncorrectRole:
        raise HTTPException(status_code=404, detail="Incorrect Role, Only the Chief of the resto can delete all the tasks")







# -----------------------------------------
#UPDATE TASK
# -----------------------------------------
@task_router.put("/update_task_by_author_id", dependencies=[Depends(security)], tags=["tasks"], response_model=TaskOutput)
async def udpdate_task_by_author_id(
    task_update: serializers.TaskCreate,
    task_id: str, 
    author_id: str = Depends(utils.get_employee_id),
    db: Session = Depends(database.get_db) ):
    
    try:
        return task_service.update_task_by_author_id(task_id=task_id, author_id= author_id, task_update = task_update, db= db)
    except WrongAuthor:
        raise HTTPException(status_code=404, detail="Only author can delete his task")
    except TaskNotFound:
        raise HTTPException(status_code=404, detail="Task not Found")
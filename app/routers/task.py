from fastapi.security import HTTPBearer
import models
import serializers
import database
from fastapi import APIRouter, Depends, HTTPException
from routers import utils
from exceptions.task import TaskNotFound, TaskAlreadyExists, WrongAuthor
from exceptions.employee import EmployeeNotFound
from routers.utils import get_employee_id
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
# DELETE A SPECIFIC TASK (only author )
# -----------------------------------------
@task_router.delete("/{task_id}", tags=["tasks"])
async def delete_task_by_id(task_id: str, db: Session = Depends(database.get_db), employee_id: str = Depends(get_employee_id) ):
    try:
        return task_service.get_task_by_id(task_id=task_id, db=db, employee_id=employee_id)
    except TaskNotFound:
        raise HTTPException(status_code=404, detail="Task not found")
    except WrongAuthor:
        raise HTTPException(status_code=403, detail="Only the author can delete this task")




# -----------------------------------------
# DELETE ALL TASKS
# -----------------------------------------
#only the chief of resto
@task_router.delete("/", tags=["tasks"])
async def delete_all_tasks(db: Session = Depends(database.get_db)):
    return task_service.delete_all_tasks(db=db)



# -----------------------------------------
# GET ONE TASK by id
# -----------------------------------------
security = HTTPBearer()

@task_router.get("/{task_id}", tags=["tasks"], response_model=TaskOutput)
async def get_task_by_id(task_id: str, db: Session = Depends(database.get_db) ):
    # Récupérer la tâche
    task = task_service.get_task_by_id(task_id=task_id, db=db)

    return task




#UPDATE TASK

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
import pdb
from datetime import datetime

from sqlalchemy.exc import IntegrityError

import models
import serializers
from fastapi import HTTPException
from sqlalchemy.orm import Session

from exceptions.employee import EmployeeNotFound
from services_crud import employee as employee_service
from exceptions.task import TaskNotFound, TaskAlreadyExists, WrongAuthor



# ---------------------------------------------------------
# CREATE TASKS
# ---------------------------------------------------------

def create_task(db: Session, task: serializers.TaskCreate) -> models.Task:
    author_id = task.author_id
    recipient_id = task.recipient_id

    # Vérifier que l’auteur et le destinataire existent
    employee_service.get_employee_by_id(employee_id=author_id, db=db)
    employee_service.get_employee_by_id(employee_id=recipient_id, db=db)

    # Créer la nouvelle tâche
    db_task = models.Task(
        title=task.title,
        content=task.content,
        author_id=author_id,
        recipient_id=recipient_id
    )

    #vérifier que la task existe déja (même:  title, content, recipient_id, author_id)
    exist_db_task = db.query(models.Task).filter(models.Task.title == db_task.title,
                                                models.Task.content == db_task.content, 
                                                models.Task.author_id == db_task.author_id,
                                                models.Task.recipient_id == db_task.recipient_id).first()
    
    if exist_db_task :
        raise TaskAlreadyExists


    db.add(db_task)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Database integrity error.")
    db.refresh(db_task)

    return db_task

# ---------------------------------------------------------
# GET TASKS
# ---------------------------------------------------------
def get_all_tasks(db):
    tasks = db.query(models.Task).all()
    return tasks



def get_task_by_id(task_id: str, db: Session) -> models.Task:
    record = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not record:
        raise TaskNotFound
    record.id = str(record.id)
    return record


def get_tasks_by_author_id(author_id: str, db: Session) -> list[models.Task]:
    records = db.query(models.Task).filter(models.Task.author_id == author_id).all()
    if not records:
        raise TaskNotFound
    for r in records:
        r.id = str(r.id)
    return records


def get_tasks_by_recipient_id(recipient_id: str, db: Session) -> list[models.Task]:
    records = db.query(models.Task).filter(models.Task.recipient_id == recipient_id).all()
    if not records:
        raise TaskNotFound
    for r in records:
        r.id = str(r.id)
    return records


def get_tasks_by_title(title: str, db: Session) -> list[models.Task]:
    records = db.query(models.Task).filter(models.Task.title == title).all()
    for r in records:
        r.id = str(r.id)
    return records


# ---------------------------------------------------------
# UPDATE TASK
# ---------------------------------------------------------
#Un auteur peut modifier la propre task qu'il a écrite pas d'autres
#Le chief_of_resto peut modifier tout post

def update_task_by_author_id(task_id: str, author_id: str, task_update: serializers.TaskCreate, db: Session) -> models.Task:
    db_task = get_task_by_id(task_id=task_id, db=db)

    if author_id != db_task.author_id:
        raise WrongAuthor
    
    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)
    db_task.id = str(db_task.id)
    return db_task


# ---------------------------------------------------------
# DELETE TASK
# ---------------------------------------------------------
#Uniquement le chief of resto pourra tout supprimer

def delete_task(task_id: str, db: Session) -> models.Task:
    db_task = get_task_by_id(task_id=task_id, db=db)
    db.delete(db_task)
    db.commit()
    return db_task


def delete_task_by_author(task_id: str, db: Session, author_id: str) -> models.Task:
    db_task = get_task_by_id(task_id=task_id, db=db)

    if db_task.author_id != author_id:
        raise WrongAuthor

    db.delete(db_task)
    db.commit()
    return db_task


def delete_all_tasks(db: Session) -> list[models.Task]:
    records = db.query(models.Task).all()
    for r in records:
        db.delete(r)
    db.commit()
    return records





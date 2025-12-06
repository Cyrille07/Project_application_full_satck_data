import pytest
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

import models
import serializers
from services_crud import task as task_service
from exceptions.task import TaskAlreadyExists, TaskNotFound, WrongAuthor
from exceptions.employee import EmployeeNotFound, IncorrectRole

# ==========================================
# FIXTURES SPÉCIFIQUES AUX TASKS
# ==========================================

@pytest.fixture(scope="function")
def setup_employees(test_db_session):
    """
    Crée 2 employés (Author et Recipient) pour pouvoir tester les tâches.
    Retourne un dictionnaire avec les objets créés.
    """
    author = models.Employee(name="Writer_Bob", password="pass", role="Server")
    recipient = models.Employee(name="Reader_Alice", password="pass", role="Cook")
    
    test_db_session.add_all([author, recipient])
    test_db_session.commit()
    test_db_session.refresh(author)
    test_db_session.refresh(recipient)
    
    return {"author": author, "recipient": recipient}


# ==========================================
# TESTS CREATE
# ==========================================

def test_create_task_success(test_db_session, setup_employees):
    """Test la création réussie d'une tâche."""
    # 1. Arrange
    author = setup_employees["author"]
    recipient = setup_employees["recipient"]
    
    task_data = serializers.TaskCreate(
        title="Clean table 5",
        content="Customer spilled soup",
        author_id=str(author.id),
        recipient_id=str(recipient.id)
    )

    # 2. Act
    new_task = task_service.create_task(db=test_db_session, task=task_data)

    # 3. Assert
    assert new_task.id is not None
    assert new_task.title == "Clean table 5"
    assert new_task.author_id == author.id
    assert new_task.recipient_id == recipient.id


def test_create_task_duplicate_raises_exception(test_db_session, setup_employees):
    """Test qu'on ne peut pas créer deux fois exactement la même tâche."""
    author = setup_employees["author"]
    recipient = setup_employees["recipient"]
    
    task_data = serializers.TaskCreate(
        title="Duplicate Title",
        content="Content",
        author_id=str(author.id),
        recipient_id=str(recipient.id)
    )

    # Création de la 1ère tâche
    task_service.create_task(test_db_session, task_data)

    # Tentative de création de la 2ème tâche identique -> Doit lever TaskAlreadyExists
    with pytest.raises(TaskAlreadyExists):
        task_service.create_task(test_db_session, task_data)


def test_create_task_unknown_author_raises_exception(test_db_session, setup_employees):
    """Test que ça échoue si l'auteur n'existe pas."""
    recipient = setup_employees["recipient"]
    
    # On invente un ID qui n'existe pas
    fake_author_id = "00000000-0000-0000-0000-000000000000" # UUID format mais faux

    task_data = serializers.TaskCreate(
        title="Ghost Task",
        content="Boo",
        author_id=fake_author_id, 
        recipient_id=str(recipient.id)
    )

    # Votre code appelle employee_service.get_employee_by_id, qui doit lever EmployeeNotFound
    with pytest.raises(EmployeeNotFound):
        task_service.create_task(test_db_session, task_data)


# ==========================================
# TESTS GET
# ==========================================

def test_get_all_tasks(test_db_session, setup_employees):
    """Test la récupération de toutes les tâches."""
    # Arrange : Créer 2 tâches
    author = setup_employees["author"]
    recipient = setup_employees["recipient"]
    
    t1 = models.Task(title="T1", content="C1", author_id=author.id, recipient_id=recipient.id)
    t2 = models.Task(title="T2", content="C2", author_id=author.id, recipient_id=recipient.id)
    test_db_session.add_all([t1, t2])
    test_db_session.commit()

    # Act
    tasks = task_service.get_all_tasks(test_db_session)

    # Assert
    assert len(tasks) == 2


def test_get_task_by_id_success(test_db_session, setup_employees):
    """Test récupération par ID."""
    author = setup_employees["author"]
    recipient = setup_employees["recipient"]
    
    # Insérer manuellement
    db_task = models.Task(title="FindMe", content="Hidden", author_id=author.id, recipient_id=recipient.id)
    test_db_session.add(db_task)
    test_db_session.commit()
    
    # Récupérer via le service
    fetched_task = task_service.get_task_by_id(str(db_task.id), test_db_session)
    
    assert fetched_task.title == "FindMe"
    assert str(fetched_task.id) == str(db_task.id)


def test_get_task_by_id_not_found(test_db_session):
    """Test erreur si ID inconnu."""
    # Note: on utilise bien un string pour l'ID pour éviter l'erreur Postgres 'integer vs varchar'
    fake_id = "99999" 
    
    with pytest.raises(TaskNotFound):
        task_service.get_task_by_id(fake_id, test_db_session)


def test_get_tasks_by_author_id_success(test_db_session, setup_employees):
    """Test récupérer les tâches d'un auteur spécifique."""
    author = setup_employees["author"]
    recipient = setup_employees["recipient"]
    
    # Tâche écrite par l'auteur
    t1 = models.Task(title="My Task", content="C", author_id=author.id, recipient_id=recipient.id)
    # Tâche écrite par quelqu'un d'autre (le recipient devient auteur ici pour l'exemple)
    t2 = models.Task(title="Other Task", content="C", author_id=recipient.id, recipient_id=author.id)
    
    test_db_session.add_all([t1, t2])
    test_db_session.commit()

    # On demande les tâches écrites par 'author' (devrait en trouver 1 seule : t1)
    tasks = task_service.get_tasks_by_author_id(str(author.id), test_db_session)
    
    assert len(tasks) == 1
    assert tasks[0].title == "My Task"


def test_get_tasks_by_author_no_tasks_raises_exception(test_db_session, setup_employees):
    """
    Test le cas spécifique de votre code : 
    Si l'auteur existe mais n'a pas de tâches, votre code lève TaskNotFound.
    """
    author = setup_employees["author"] # Il existe, mais on n'a créé aucune tâche
    
    with pytest.raises(TaskNotFound):
        task_service.get_tasks_by_author_id(str(author.id), test_db_session)


def test_get_tasks_by_recipient_id_success(test_db_session, setup_employees):
    """Test récupérer les tâches assignées à un destinataire."""
    author = setup_employees["author"]
    recipient = setup_employees["recipient"]
    
    # Créer une tâche pour ce destinataire
    t1 = models.Task(title="For You", content="Work", author_id=author.id, recipient_id=recipient.id)
    test_db_session.add(t1)
    test_db_session.commit()

    tasks = task_service.get_tasks_by_recipient_id(str(recipient.id), test_db_session)
    
    assert len(tasks) == 1
    assert tasks[0].title == "For You"


def test_get_tasks_by_recipient_no_tasks_raises_exception(test_db_session, setup_employees):
    """Test lève TaskNotFound si le destinataire n'a pas de tâches."""
    recipient = setup_employees["recipient"]
    
    with pytest.raises(TaskNotFound):
        task_service.get_tasks_by_recipient_id(str(recipient.id), test_db_session)




# ==========================================
# TESTS UPDATE
# ==========================================

def test_update_task_by_author_success(test_db_session, setup_employees):
    """L'auteur modifie sa propre tâche."""
    # 1. Arrange
    author = setup_employees["author"]
    recipient = setup_employees["recipient"]
    
    task = models.Task(title="Old Title", content="Old Content", author_id=author.id, recipient_id=recipient.id)
    test_db_session.add(task)
    test_db_session.commit()
    test_db_session.refresh(task) # Important pour avoir l'ID

    # Données de mise à jour (via le Serializer)
    update_data = serializers.TaskCreate(
        title="New Title", 
        content="New Content", 
        author_id=str(author.id), 
        recipient_id=str(recipient.id)
    )

    # 2. Act
    updated_task = task_service.update_task_by_author_id(
        task_id=str(task.id), 
        author_id=str(author.id), 
        task_update=update_data, 
        db=test_db_session
    )

    # 3. Assert
    assert updated_task.title == "New Title"
    assert updated_task.content == "New Content"


def test_update_task_wrong_author_raises_exception(test_db_session, setup_employees):
    """Un autre employé essaie de modifier la tâche de l'auteur."""
    author = setup_employees["author"]
    recipient = setup_employees["recipient"] # Le recipient va essayer de modifier
    
    task = models.Task(title="My Task", content="...", author_id=author.id, recipient_id=recipient.id)
    test_db_session.add(task)
    test_db_session.commit()

    update_data = serializers.TaskCreate(
        title="Hacked Title", 
        content="...", 
        author_id=str(author.id), 
        recipient_id=str(recipient.id)
    )

    # Le recipient essaie de modifier la tâche de l'auteur
    with pytest.raises(WrongAuthor):
        task_service.update_task_by_author_id(
            task_id=str(task.id), 
            author_id=str(recipient.id), # <--- ID incorrect ici
            task_update=update_data, 
            db=test_db_session
        )



# ==========================================
# TESTS DELETE (Single)
# ==========================================

def test_delete_task_simple(test_db_session, setup_employees):
    """Test de la suppression simple (souvent admin)."""
    author = setup_employees["author"]
    recipient = setup_employees["recipient"]
    
    task = models.Task(title="DelMe", content="...", author_id=author.id, recipient_id=recipient.id)
    test_db_session.add(task)
    test_db_session.commit()
    
    deleted_task = task_service.delete_task(str(task.id), test_db_session)
    
    assert deleted_task.id == task.id
    # Vérifier qu'elle n'est plus en base
    assert test_db_session.query(models.Task).filter_by(id=task.id).first() is None


def test_delete_task_by_author_success(test_db_session, setup_employees):
    """L'auteur supprime sa propre tâche."""
    author = setup_employees["author"]
    recipient = setup_employees["recipient"]
    
    task = models.Task(title="DelMeAuthor", content="...", author_id=author.id, recipient_id=recipient.id)
    test_db_session.add(task)
    test_db_session.commit()

    task_service.delete_task_by_author(str(task.id), test_db_session, str(author.id))
    
    assert test_db_session.query(models.Task).filter_by(id=task.id).first() is None


def test_delete_task_by_author_wrong_author(test_db_session, setup_employees):
    """Quelqu'un d'autre essaie de supprimer la tâche."""
    author = setup_employees["author"]
    recipient = setup_employees["recipient"]
    
    task = models.Task(title="DontTouch", content="...", author_id=author.id, recipient_id=recipient.id)
    test_db_session.add(task)
    test_db_session.commit()

    with pytest.raises(WrongAuthor):
        task_service.delete_task_by_author(str(task.id), test_db_session, str(recipient.id)) # Mauvais ID


# ==========================================
# TESTS DELETE ALL (Chief Only)
# ==========================================

def test_delete_all_tasks_success_chief(test_db_session):
    """Le chef supprime toutes les tâches."""
    # 1. Créer un Chef et des tâches
    chief = models.Employee(name="Chief", password="pass", role="Chief_of_resto")
    server = models.Employee(name="Srv", password="pass", role="Server")
    test_db_session.add_all([chief, server])
    test_db_session.commit()
    
    t1 = models.Task(title="T1", content="C", author_id=server.id, recipient_id=server.id)
    t2 = models.Task(title="T2", content="C", author_id=server.id, recipient_id=server.id)
    test_db_session.add_all([t1, t2])
    test_db_session.commit()

    # 2. Act
    deleted_records = task_service.delete_all_tasks(str(chief.id), test_db_session)

    # 3. Assert
    assert len(deleted_records) == 2
    assert test_db_session.query(models.Task).count() == 0


def test_delete_all_tasks_failure_not_chief(test_db_session, setup_employees):
    """Un simple serveur ne peut pas tout supprimer."""
    author = setup_employees["author"] # Rôle = "Server"
    
    # Créer une tâche pour vérifier qu'elle n'est pas supprimée
    t1 = models.Task(title="Safe", content="C", author_id=author.id, recipient_id=author.id)
    test_db_session.add(t1)
    test_db_session.commit()

    with pytest.raises(IncorrectRole):
        task_service.delete_all_tasks(str(author.id), test_db_session)
        
    # Vérifier que la tâche est toujours là
    assert test_db_session.query(models.Task).count() == 1
import pytest
from main import app
import models
from routers import utils
import serializers
# Import nécessaire même si pas utilisé dans les routes publiques, 
# au cas où tu sécurises plus tard.
from routers.task import security 

# ==========================================
# FIXTURE : Données de base
# ==========================================
@pytest.fixture
def setup_task_data(test_db_session):
    """
    Crée un scénario complet :
    - 1 Chef
    - 1 Auteur
    - 1 Destinataire
    """
    chief = models.Employee(name="Chief_Boss", password="pass", role="Chief_of_resto")
    author = models.Employee(name="Writer_Tom", password="pass", role="Server")
    recipient = models.Employee(name="Reader_Jerry", password="pass", role="Cook")
    
    test_db_session.add_all([chief, author, recipient])
    test_db_session.commit()
    
    return {
        "chief": chief,
        "author": author,
        "recipient": recipient
    }

# ==========================================
# 1. POST (CREATE)
# ==========================================

def test_create_task_route_success(client, test_db_session, setup_task_data):
    """Teste la création d'une tâche (Cas nominal 200 OK)."""
    author = setup_task_data["author"]
    recipient = setup_task_data["recipient"]

    payload = {
        "title": "Clean the kitchen",
        "content": "Before midnight",
        "author_id": str(author.id),
        "recipient_id": str(recipient.id)
    }
    
    response = client.post("/tasks/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Clean the kitchen"
    assert data["author_id"] == str(author.id)


def test_create_task_employee_not_found(client, test_db_session, setup_task_data):
    """Teste l'erreur 404 si l'auteur ou le destinataire n'existe pas."""
    recipient = setup_task_data["recipient"]
    
    payload = {
        "title": "Ghost Task",
        "content": "...",
        "author_id": "00000000-0000-0000-0000-000000000000", # ID inconnu
        "recipient_id": str(recipient.id)
    }
    
    response = client.post("/tasks/", json=payload)
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"


def test_create_task_already_exists(client, test_db_session, setup_task_data):
    """Teste l'erreur 409 Conflict si la tâche existe déjà."""
    author = setup_task_data["author"]
    recipient = setup_task_data["recipient"]
    
    payload = {
        "title": "Duplicate",
        "content": "Content",
        "author_id": str(author.id),
        "recipient_id": str(recipient.id)
    }
    
    # 1. Première création : Succès
    response1 = client.post("/tasks/", json=payload)
    assert response1.status_code == 200

    # 2. Deuxième création identique : Erreur 409
    response2 = client.post("/tasks/", json=payload)
    assert response2.status_code == 409
    assert response2.json()["detail"] == "Task already exists"


# ==========================================
# 2. GET ALL
# ==========================================

def test_get_all_tasks_route(client, test_db_session, setup_task_data):
    """Teste la récupération de la liste."""
    author = setup_task_data["author"]
    recipient = setup_task_data["recipient"]
    
    # On ajoute manuellement une tâche en base
    task = models.Task(title="T1", content="C1", author_id=author.id, recipient_id=recipient.id)
    test_db_session.add(task)
    test_db_session.commit()

    response = client.get("/tasks/")
    
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "T1"


# ==========================================
# 3. GET BY ID
# ==========================================

def test_get_task_by_id_success(client, test_db_session, setup_task_data):
    """Teste récupération par ID."""
    author = setup_task_data["author"]
    recipient = setup_task_data["recipient"]
    task = models.Task(title="FindMe", content="Hidden", author_id=author.id, recipient_id=recipient.id)
    test_db_session.add(task)
    test_db_session.commit()

    response = client.get(f"/tasks/{task.id}")
    
    assert response.status_code == 200
    assert response.json()["title"] == "FindMe"


def test_get_task_by_id_not_found(client,test_db_session):
    """Teste erreur 404 sur ID inconnu."""
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/tasks/{fake_uuid}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Tasks not found"


# ==========================================
# 4. GET BY AUTHOR / RECIPIENT
# ==========================================

def test_get_task_by_author_success(client, test_db_session, setup_task_data):
    """Teste récupération par Auteur."""
    author = setup_task_data["author"]
    recipient = setup_task_data["recipient"]
    task = models.Task(title="MyWork", content="...", author_id=author.id, recipient_id=recipient.id)
    test_db_session.add(task)
    test_db_session.commit()

    response = client.get(f"/tasks/taskauthor/{author.id}")
    
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "MyWork"


def test_get_task_by_author_no_tasks(client, test_db_session, setup_task_data):
    """Teste erreur 404 si l'auteur n'a pas écrit de tâches."""
    author = setup_task_data["author"] # Existe mais pas de tâches
    
    response = client.get(f"/tasks/taskauthor/{author.id}")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Has no written Tasks"


def test_get_task_by_recipient_success(client, test_db_session, setup_task_data):
    """Teste récupération par Destinataire."""
    author = setup_task_data["author"]
    recipient = setup_task_data["recipient"]
    task = models.Task(title="ForYou", content="...", author_id=author.id, recipient_id=recipient.id)
    test_db_session.add(task)
    test_db_session.commit()

    response = client.get(f"/tasks/taskrecipient/{recipient.id}")
    
    assert response.status_code == 200
    assert response.json()[0]["title"] == "ForYou"


# ==========================================
# 5. DELETE SINGLE TASK
# ==========================================

def test_delete_task_by_id_success(client, test_db_session, setup_task_data):
    """Teste la suppression d'une tâche par son ID."""
    author = setup_task_data["author"]
    recipient = setup_task_data["recipient"]
    
    # 1. Créer la tâche
    task = models.Task(title="Delete Me", content="...", author_id=author.id, recipient_id=recipient.id)
    test_db_session.add(task)
    test_db_session.commit()

    # 2. Appel API (Route publique selon ton code)
    response = client.delete(f"/tasks/deltask/{task.id}")
    
    assert response.status_code == 200
    assert response.json()["title"] == "Delete Me"
    
    # 3. Vérifier qu'elle est bien supprimée en DB
    assert test_db_session.query(models.Task).filter_by(id=task.id).first() is None


def test_delete_task_not_found(client,test_db_session):
    """Teste erreur 404 si ID inconnu."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"/tasks/deltask/{fake_id}")
    assert response.status_code == 404


# ==========================================
# 6. DELETE ALL TASKS (Secured)
# ==========================================

def test_delete_all_tasks_chief_success(client, test_db_session, setup_task_data):
    """Le chef supprime toutes les tâches."""
    chief = setup_task_data["chief"]
    author = setup_task_data["author"]
    recipient = setup_task_data["recipient"]
    
    # Créer une tâche
    task = models.Task(title="T1", content="C1", author_id=author.id, recipient_id=recipient.id)
    test_db_session.add(task)
    test_db_session.commit()

    # OVERRIDES : Chef connecté
    app.dependency_overrides[utils.get_employee_id] = lambda: str(chief.id)
    app.dependency_overrides[security] = lambda: "fake"

    try:
        response = client.delete(f"/tasks/deletealltask/{chief.id}")
        
        assert response.status_code == 200
        # Vérification DB
        assert test_db_session.query(models.Task).count() == 0
    finally:
        app.dependency_overrides = {}


def test_delete_all_tasks_incorrect_role(client, test_db_session, setup_task_data):
    """Un simple serveur ne peut pas tout supprimer."""
    server = setup_task_data["author"] # Rôle Server
    
    # OVERRIDES : Serveur connecté
    app.dependency_overrides[utils.get_employee_id] = lambda: str(server.id)
    app.dependency_overrides[security] = lambda: "fake"

    try:
        response = client.delete(f"/tasks/deletealltask/{server.id}")
        
        assert response.status_code == 404
        assert "Incorrect Role" in response.json()["detail"]
    finally:
        app.dependency_overrides = {}


# ==========================================
# 7. UPDATE TASK (Secured)
# ==========================================

def test_update_task_author_success(client, test_db_session, setup_task_data):
    """L'auteur met à jour sa tâche."""
    author = setup_task_data["author"]
    recipient = setup_task_data["recipient"]
    
    task = models.Task(title="Old", content="Old", author_id=author.id, recipient_id=recipient.id)
    test_db_session.add(task)
    test_db_session.commit()

    # OVERRIDES : Auteur connecté
    app.dependency_overrides[utils.get_employee_id] = lambda: str(author.id)
    app.dependency_overrides[security] = lambda: "fake"

    try:
        payload = {
            "title": "New Title",
            "content": "New Content",
            "author_id": str(author.id),
            "recipient_id": str(recipient.id)
        }
        
        # la route n'a pas {task_id} dans le chemin, 
        # il faut donc le passer en Query Param (?task_id=...)
        url = f"/tasks/update_task_by_author_id?task_id={task.id}"
        
        response = client.put(url, json=payload)
        
        assert response.status_code == 200
        assert response.json()["title"] == "New Title"
    finally:
        app.dependency_overrides = {}


def test_update_task_wrong_author(client, test_db_session, setup_task_data):
    """Le destinataire tente de modifier (Doit échouer)."""
    author = setup_task_data["author"]
    recipient = setup_task_data["recipient"]
    
    task = models.Task(title="Old", content="Old", author_id=author.id, recipient_id=recipient.id)
    test_db_session.add(task)
    test_db_session.commit()

    # OVERRIDES : Destinataire connecté (Mauvais auteur)
    app.dependency_overrides[utils.get_employee_id] = lambda: str(recipient.id)
    app.dependency_overrides[security] = lambda: "fake"

    try:
        payload = {
            "title": "Hacked",
            "content": "...",
            "author_id": str(author.id),
            "recipient_id": str(recipient.id)
        }
        
        url = f"/tasks/update_task_by_author_id?task_id={task.id}"
        response = client.put(url, json=payload)
        
        # Le codde renvoie 404 pour WrongAuthor
        assert response.status_code == 404
        assert "Only author can delete" in response.json()["detail"] 
    finally:
        app.dependency_overrides = {}

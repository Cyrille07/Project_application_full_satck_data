from datetime import datetime, timedelta
import pytest
import jwt
import os
from models import Employee, Task


from main import app
from routers import utils
from models import Employee
from services_crud.auth import hash_password
from routers.employee import security  
from fastapi.security import HTTPAuthorizationCredentials


# ==========================================
# 1. Tests des routes Publiques (Create / Get)
# ==========================================

def test_create_employee_route_success(client, test_db_session):
    """Teste la création d'un employé via la route POST."""
    payload = {
        "name": "NewUser",
        "password": "password123",
        "role": "Server"
    }
    
    response = client.post("/employees/", json=payload)
    
    assert response.status_code == 200 # Note: Idéalement 201, mais ton code renvoie 200 par défaut
    data = response.json()
    assert data["name"] == "NewUser"
    assert "id" in data
    assert "password" not in data # Le serializer Output ne doit pas renvoyer le mdp


def test_create_employee_route_incorrect_role(client, test_db_session):
    """Teste que l'API renvoie 401 si le rôle est invalide."""
    payload = {
        "name": "BadRoleUser",
        "password": "password123",
        "role": "SuperHero"
    }
    
    response = client.post("/employees/", json=payload)
    
    assert response.status_code == 401
    assert "Role not defined" in response.json()["detail"]


def test_get_employee_by_id_route(client, test_db_session):
    """Teste la récupération d'un employé."""
    # 1. Setup: Créer un employé en DB
    emp = Employee(name="GetMe", password="hash", role="Cook")
    test_db_session.add(emp)
    test_db_session.commit()
    
    # 2. Test
    response = client.get(f"/employees/{emp.id}")
    
    assert response.status_code == 200
    assert response.json()["name"] == "GetMe"


def test_get_employee_not_found(client,test_db_session):
    non_existent_id = "D999KEUUID"
    response = client.get(f"/employees/{non_existent_id}")
    assert response.status_code == 404


# ==========================================
# 2. Tests des routes Protégées (Update / Delete All)
# ==========================================

def test_update_myself_success(client, test_db_session):
    """
    Teste la mise à jour de soi-même.
    Utilise dependency_override pour simuler un utilisateur connecté.
    """
    # 1. Setup : Créer l'utilisateur qui va se connecter
    user = Employee(name="OriginalName", password=hash_password("pass"), role="Server")
    test_db_session.add(user)
    test_db_session.commit()
    
    # 2. OVERRIDE : On force l'API à croire que c'est cet utilisateur qui appelle
    app.dependency_overrides[utils.get_employee_id] = lambda: str(user.id)
    
    try:
        payload = {
            "name": "UpdatedName",
            "password": "newpass",
            "role": "Cashier"
        }
        
        # Note: Pas besoin de header Authorization grâce à l'override !
        response = client.put("/employees/updateme", json=payload)
        
        assert response.status_code == 200
        assert response.json()["name"] == "UpdatedName"
        
        # Vérif en DB
        test_db_session.refresh(user)
        assert user.role == "Cashier"
        
    finally:
        # TRES IMPORTANT : Nettoyer l'override après le test
        app.dependency_overrides = {}


def test_delete_all_employees_success_chief(client, test_db_session):
    """
    Teste que le chef peut tout supprimer.
    """
    # 1. Setup : Création des données (Chef et Employé)
    chief = Employee(name="TheBoss", password="pass", role="Chief_of_resto")
    emp1 = Employee(name="Emp1", password="pass", role="Server")
    test_db_session.add_all([chief, emp1])
    test_db_session.commit()
    
    # ==============================================================================
    # 2. LES SURCHARGES (OVERRIDES)
    # ==============================================================================
    
    # A. Surcharge de l'ID 
    app.dependency_overrides[utils.get_employee_id] = lambda: str(chief.id)
    
    # B. Surcharge de la Sécurité 
    # On dit à l'app : "Voici les identifiants de sécurité, considère qu'ils sont valides."
    # FastAPI a besoin d'un objet HTTPAuthorizationCredentials avec un scheme "Bearer".
    app.dependency_overrides[security] = lambda: HTTPAuthorizationCredentials(scheme="Bearer", credentials="fake_token_value")

    try:
        # 3. Action : Appel de la route
        # FastAPI va utiliser vos overrides au lieu de vérifier les vrais headers
        response = client.delete(f"/employees/delete_all/{chief.id}")
        
        # 4. Vérification
        assert response.status_code == 200
        assert "Deleted" in response.json()["message"]
        
    finally:
        # 5. Nettoyage (TRES IMPORTANT)
        # On remet l'application à zéro pour ne pas impacter les autres tests
        app.dependency_overrides = {}


def test_delete_all_employees_mismatch_id(client, test_db_session):
    """
    Teste l'erreur si l'ID dans l'URL ne correspond pas à l'ID du token.
    """
    # Setup
    chief = Employee(name="TheBoss", password="pass", role="Chief_of_resto")
    other = Employee(name="Hacker", password="pass", role="Server")
    test_db_session.add_all([chief, other])
    test_db_session.commit()
    
    # --- OVERRIDES ---
    # 1. On simule que c'est le Hacker qui est connecté
    app.dependency_overrides[utils.get_employee_id] = lambda: str(other.id)
    
    # 2. (Surcharge de la sécurité)
    app.dependency_overrides[security] = lambda: HTTPAuthorizationCredentials(scheme="Bearer", credentials="fake")

    try:
        # Action : Le hacker essaie de supprimer en utilisant l'ID du chef dans l'URL
        response = client.delete(f"/employees/delete_all/{chief.id}")
        
        # Assert
        assert response.status_code == 403
        assert "mismatch" in response.json()["detail"]

    finally:
        app.dependency_overrides = {}


def test_delete_all_employees_wrong_role(client, test_db_session):
    """
    Teste qu'un serveur ne peut pas supprimer tout le monde même avec le bon ID.
    """
    # Setup
    server = Employee(name="NotChief", password="pass", role="Server")
    test_db_session.add(server)
    test_db_session.commit()
    
    # --- OVERRIDES ---
    # 1. On simule le serveur connecté
    app.dependency_overrides[utils.get_employee_id] = lambda: str(server.id)
    
    # 2. (Surcharge de la sécurité)
    app.dependency_overrides[security] = lambda: HTTPAuthorizationCredentials(scheme="Bearer", credentials="fake")

    try:
        # Action
        response = client.delete(f"/employees/delete_all/{server.id}")
        
        # Assert
        assert response.status_code == 403
        assert "Only the Chief" in response.json()["detail"]
        
    finally:
        app.dependency_overrides = {}
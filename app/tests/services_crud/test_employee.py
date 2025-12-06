
""" Test unitaire de employee coté database et pas route
    Test logique métier  """

from datetime import datetime, timedelta
import pytest
import jwt
import os
from models import Employee, Task
import serializers
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from services_crud.employee import  create_employee, get_employee_by_id, update_employee, delete_all_employees, delete_employee_by_id
from exceptions.employee import EmployeeNotFound, IncorrectRole

from unittest import mock 


# Utiliser un mock pour simuler le hachage du mot de passe
# pour ne pas dépendre du service d'auth réel dans ce test unitaire
@pytest.fixture(autouse=True)
def mock_hash_password():
    with mock.patch("services_crud.employee.hash_password", side_effect=lambda p: f"hashed_{p}") as mock_hash:
        yield mock_hash


#------------Tests de la fonction create_employee------------

def test_create_employee_success(test_db_session):
    """Teste la création réussie d'un employé."""  
    #Arrange
    employee_data = serializers.EmployeeCreate(name="John_Doe", password="securepass", role="Server")  
    #Act
    new_employee = create_employee(db=test_db_session, employee=employee_data)
    #Assert
    assert new_employee.id is not None
    assert new_employee.name == "John_Doe"
    assert new_employee.role == "Server"
    assert new_employee.password == "hashed_securepass" # Vérifie le mock

    # Vérifiez que l'employé est bien en base
    fetched_employee = test_db_session.query(Employee).filter_by(id=new_employee.id).first()
    assert fetched_employee.name == "John_Doe"
    

def test_create_employee_duplicate_name_raises_exception(test_db_session):
    """Teste la levée d'une HTTPException (401) si le nom existe déjà."""

    employee_data_1 = serializers.EmployeeCreate(name="John_Doe", password="pass1", role="Cook")
    create_employee(db=test_db_session, employee=employee_data_1)    
    employee_data_2 = serializers.EmployeeCreate(name="John_Doe", password="pass2", role="Server")    
    #Exécution et Assertion : On s'attend à une HTTPException
    with pytest.raises(HTTPException) as excinfo:
        create_employee(db=test_db_session, employee=employee_data_2)
        
    assert excinfo.value.status_code == 401


def test_create_employee_incorrect_role_raises_exception(test_db_session):
    """Teste la levée de l'exception IncorrectRole si le rôle n'est pas autorisé."""   
    employee_data = serializers.EmployeeCreate(name="John_Doe", password="pass", role="Juggler") # Rôle non autorisé
    # On s'attend à ce que l'exception IncorrectRole soit levée
    with pytest.raises(IncorrectRole):
        create_employee(db=test_db_session, employee=employee_data)



# ------------- Tests de la fonction get_employee_by_id ----------
def test_get_employee_by_id_success(test_db_session):
    """Teste la récupération réussie d'un employé par son ID.""" 
    # 1. Préparer : Insérer un employé directement en DB
    db_employee = Employee(name="John_Doe", password="hash", role="Chief_of_resto")
    test_db_session.add(db_employee)
    test_db_session.commit()
    test_db_session.refresh(db_employee)   
    # 2. Exécution
    fetched_employee = get_employee_by_id(employee_id=db_employee.id, db=test_db_session)
    # 3. Assertion
    assert fetched_employee.name == "John_Doe"
    assert fetched_employee.id == db_employee.id


def test_get_employee_by_id_not_found_raises_exception(test_db_session):
    """Teste la levée de l'exception EmployeeNotFound si l'ID n'existe pas."""  
    non_existent_id = "999"
    # On s'attend à ce que l'exception métier EmployeeNotFound soit levée
    with pytest.raises(EmployeeNotFound):
        get_employee_by_id(employee_id=non_existent_id, db=test_db_session)





# ------------  Tests de la fonction update_employee------------ 

def test_update_employee_success(test_db_session):
    """Teste la mise à jour réussie (changement de nom et de role)."""
    # 1. Arrange: Créer un employé initial
    emp = Employee(name="OldName", password="oldpass", role="Server")
    test_db_session.add(emp)
    test_db_session.commit()
    update_data = serializers.EmployeeCreate(name="NewName", password="newpass", role="Cashier")

    # 2. Act
    updated_emp = update_employee(employee_id=emp.id, db=test_db_session, employee_update=update_data)

    # 3. Assert
    assert updated_emp.name == "NewName"
    assert updated_emp.role == "Cashier"
    assert updated_emp.password == "hashed_newpass" # Grâce au mock du hash


def test_update_employee_duplicate_name(test_db_session):
    """Teste qu'on ne peut pas prendre le nom d'un autre employé existant."""
    # 1. Arrange: Deux employés
    emp1 = Employee(name="Alice", password="p", role="Server")
    emp2 = Employee(name="Bob", password="p", role="Server")
    test_db_session.add_all([emp1, emp2])
    test_db_session.commit()

    # 2. Act: On essaie de renommer Bob en Alice
    update_data = serializers.EmployeeCreate(name="Alice", password="p", role="Server")

    # 3. Assert
    with pytest.raises(HTTPException) as excinfo:
        update_employee(emp2.id, test_db_session, update_data)
    
    assert excinfo.value.status_code == 401
    assert "User with this name already exist" in excinfo.value.detail


def test_update_employee_incorrect_role(test_db_session):
    
    """Teste le blocage si le nouveau rôle n'est pas valide."""
    emp = Employee(name="Carol", password="p", role="Server")
    test_db_session.add(emp)
    test_db_session.commit()

    update_data = serializers.EmployeeCreate(name="Carol", password="p", role="Astronaut")

    with pytest.raises(IncorrectRole):
        update_employee(emp.id, test_db_session, update_data)





# ------------  Tests de la fonction delete_employee_by_id---------------

def test_delete_employee_success(test_db_session):
    """Teste la suppression d'un employé sans tâches."""
    emp = Employee(name="ToBeDeleted", password="p", role="Server")
    test_db_session.add(emp)
    test_db_session.commit() # L'employé a un ID
    emp_id = emp.id

    # Les listes tasks_written/received sont vides par défaut lors de la création
    deleted_emp = delete_employee_by_id(emp_id, test_db_session)

    assert deleted_emp.id == emp_id
    
    # Vérifier qu'il n'est plus en base
    assert test_db_session.query(Employee).filter_by(id=emp_id).first() is None


def test_delete_employee_with_tasks_fails(test_db_session, mocker):
    """
    Teste l'interdiction de supprimer un employé qui a des tâches écrites.
    Utilise 'mocker' pour simuler la présence de tâches sans avoir besoin de la table Task.
    """
    # 1. Arrange
    emp = Employee(name="BusyWorker", password="p", role="Server")
    test_db_session.add(emp)
    test_db_session.commit()

    # 2. Mocking : On intercepte get_employee_by_id pour renvoyer un objet modifié
    # On crée un faux objet qui ressemble à l'employé mais avec une liste de tâches non vide
    mock_employee = mocker.Mock(wraps=emp) 
    mock_employee.tasks_written = ["Task1"] # On simule une tâche
    mock_employee.tasks_received = []
    
    # On dit à python : quand 'get_employee_by_id' est appelé dans ce module,
    # renvoie mon 'mock_employee' au lieu de faire la requête SQL réelle.
    mocker.patch("services_crud.employee.get_employee_by_id", return_value=mock_employee)

    # 3. Act & Assert
    with pytest.raises(HTTPException) as excinfo:
        delete_employee_by_id(emp.id, test_db_session)
    
    assert excinfo.value.status_code == 403
    assert "impossible to delete" in excinfo.value.detail






# ------------  Tests de la fonction delete_all_employees------------ 

def test_delete_all_employees_success(test_db_session):
    """Le chef supprime tout le monde sauf lui-même."""
    # 1. Arrange
    chief = Employee(name="LeChef", password="p", role="Chief_of_resto")
    server1 = Employee(name="Serv1", password="p", role="Server")
    server2 = Employee(name="Serv2", password="p", role="Server")
    
    test_db_session.add_all([chief, server1, server2])
    test_db_session.commit()

    # 2. Act
    delete_all_employees(chief.id, test_db_session)

    # 3. Assert
    remaining_employees = test_db_session.query(Employee).all()
    assert len(remaining_employees) == 1
    assert remaining_employees[0].id == chief.id
    assert remaining_employees[0].role == "Chief_of_resto"


def test_delete_all_employees_unauthorized(test_db_session):
    """Un simple serveur ne peut pas supprimer tout le monde."""
    server = Employee(name="Hacker", password="p", role="Server")
    target = Employee(name="Victim", password="p", role="Server")
    test_db_session.add_all([server, target])
    test_db_session.commit()

    with pytest.raises(IncorrectRole):
        delete_all_employees(server.id, test_db_session)
        
    # Vérification que personne n'a été supprimé
    assert test_db_session.query(Employee).count() == 2
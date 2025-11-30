"""
Tests pour le router d'authentification
"""

from unittest.mock import patch

from exceptions.employee import EmployeeNotFound, IncorrectRole, IncorrectPassword


def test_get_access_token_success(client):
    """
    Test de génération de token avec succès

    Scénario: Utilisateur valide avec credentials corrects
    Résultat attendu: Token généré avec status 200
    """
    # Arrange
    employee_credentials = {"name": "testemployee", "password": "testpassword", "role": "Cashier"}
    mock_token = "mock_jwt_token_abc123"

    # Mock generate_access_token pour retourner un token
    with patch(
        "routers.auth.generate_access_token", return_value=mock_token
    ) as mock_generate:
        # Act
        response = client.post("/auth/token", json=employee_credentials)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["access_token"] == mock_token
        mock_generate.assert_called_once()


def test_get_access_token_employee_not_found(client):
    """
    Test de génération de token avec utilisateur inexistant

    Scénario: Utilisateur n'existe pas dans la base de données
    Résultat attendu: Erreur 404 avec message approprié
    """
    # Arrange
    employee_credentials = {"name": "Wrongtestemployee", "password": "testpassword", "role": "Cashier"}

    # Mock generate_access_token pour lever EmployeeNotFound
    with patch(
        "routers.auth.generate_access_token", side_effect=EmployeeNotFound("User not found")
    ) as mock_generate:
        response = client.post("/auth/token", json=employee_credentials)
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}
        mock_generate.assert_called_once()


def test_get_access_token_incorrect_password(client):
    """
    Test de génération de token avec mot de passe incorrect

    Scénario: Utilisateur existe mais mot de passe incorrect
    Résultat attendu: Erreur 400 avec message approprié
    """
    # Arrange
    employee_credentials = {"name": "testemployee", "password": "Wrongtestpassword", "role": "Cashier"}

    # Mock generate_access_token pour lever IncorrectPassword
    with patch(
        "routers.auth.generate_access_token",
        side_effect=IncorrectPassword("Incorrect password"),
    ) as mock_generate:
        # Act
        response = client.post("/auth/token", json=employee_credentials)

        # Assert
        assert response.status_code == 400
        assert response.json() == {"detail": "Incorrect password"}
        mock_generate.assert_called_once()


def test_get_access_token_incorrect_role(client):
    """
    Test de génération de token avec le role incorect

    Scénario: Utilisateur existe mais role incorrect
    Résultat attendu: Erreur 400 avec message approprié
    """
    # Arrange
    employee_credentials = {"name": "testemployee", "password": "testpassword", "role": "WrongRole"}

    # Mock generate_access_token pour lever IncorrectRole
    with patch(
        "routers.auth.generate_access_token",
        side_effect=IncorrectRole("Incorrect Role"),
    ) as mock_generate:
        # Act
        response = client.post("/auth/token", json=employee_credentials)

        # Assert
        assert response.status_code == 400
        assert response.json() == {"detail": "Incorrect Role"}
        mock_generate.assert_called_once()



def test_get_access_token_missing_name(client):
    """
    Test de génération de token sans name

    Scénario: Requête sans name dans le body
    Résultat attendu: Erreur 422 (validation error)
    """
    # Arrange
    invalid_employee_credentials = {"password": "testpassword", "role": "Cashier"}

    # Act
    response = client.post("/auth/token", json=invalid_employee_credentials)

    # Assert
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_get_access_token_missing_password(client):
    """
    Test de génération de token sans password

    Scénario: Requête sans password dans le body
    Résultat attendu: Erreur 422 (validation error)
    """
    # Arrange
    invalid_employee_credentials = {"name": "tet_employee_name", "role": "Cashier"}

    # Act
    response = client.post("/auth/token", json=invalid_employee_credentials)

    # Assert
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_get_access_token_missing_role(client):
    """
    Test de génération de token sans role

    Scénario: Requête sans role dans le body
    Résultat attendu: Erreur 422 (validation error)
    """
    # Arrange
    invalid_employee_credentials = {"name": "tet_employee_name", "password": "test_password"}

    # Act
    response = client.post("/auth/token", json=invalid_employee_credentials)

    # Assert
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_get_access_token_empty_credentials(client):
    """
    Test de génération de token avec credentials vides

    Scénario: Username et password sont des chaînes vides
    Résultat attendu: Selon la logique métier (400 ou 404)
    """
    # Arrange
    empty_employee_credentials = {"name": "", "password": "", "role":""}

    # Mock pour simuler l'échec avec EmployeeNotFound
    with patch(
        "routers.auth.generate_access_token", side_effect=EmployeeNotFound("Employee Not Found")
    ) as mock_generate:
        response = client.post("/auth/token", json=empty_employee_credentials)
        assert response.status_code == 404
        assert response.json() == {"detail": "Employee Not Found"}
        mock_generate.assert_called_once()


def test_get_access_token_with_special_characters(client):
    """
    Test de génération de token avec caractères spéciaux

    Scénario: Username et password contiennent des caractères spéciaux
    Résultat attendu: Traitement normal, succès si valide
    """
    # Arrange
    special_credentials = {"name": "testemplo@!&#yee", "password": "testpassword@!&#*%", "role": "Cashier"}
    mock_token = "mock_token_with_special_chars"

    # Mock generate_access_token
    with patch(
        "routers.auth.generate_access_token", return_value=mock_token
    ) as mock_generate:
        response = client.post("/auth/token", json=special_credentials)
        assert response.status_code == 200
        assert response.json()["access_token"] == mock_token
        mock_generate.assert_called_once()


def test_get_access_token_verifies_db_session_passed(client):
    """
    Test que la session de base de données est bien passée

    Scénario: Vérifier que generate_access_token reçoit la session DB
    Résultat attendu: Session DB dans les arguments d'appel
    """
    # Arrange
    employee_credentials = {"name": "testemployee", "password": "testpassword", "role": "Cashier"}

    # Mock generate_access_token
    with patch(
        "routers.auth.generate_access_token", return_value="test_token"
    ) as mock_generate:
        response = client.post("/auth/token", json=employee_credentials)
        assert response.status_code == 200
        assert response.json()["access_token"] == "test_token"
        mock_generate.assert_called_once()

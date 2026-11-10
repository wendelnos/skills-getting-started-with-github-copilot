from copy import deepcopy

from fastapi.testclient import TestClient

from src import app as app_module


BASE_ACTIVITIES = {
    "Clube de Xadrez": {
        "description": "Aprenda estratégias e participe de torneios de xadrez",
        "schedule": "Sextas-feiras, 15h30 - 17h",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
    },
    "Aula de Programação": {
        "description": "Aprenda os fundamentos da programação e desenvolva projetos de software",
        "schedule": "Terças e quintas-feiras, 15h30 - 16h30",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
    },
    "Aula de Educação Física": {
        "description": "Atividades de educação física e esportes",
        "schedule": "Segundas, quartas e sextas-feiras, 14h - 15h",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
    },
    "Time de Basquete": {
        "description": "Pratique habilidades de basquete e dispute partidas em equipe",
        "schedule": "Terças e quintas-feiras, 16h - 17h30",
        "max_participants": 15,
        "participants": [],
    },
    "Clube de Futebol": {
        "description": "Desenvolva suas habilidades no futebol e jogue partidas amistosas",
        "schedule": "Segundas e quartas-feiras, 15h30 - 17h",
        "max_participants": 22,
        "participants": [],
    },
    "Clube de Teatro": {
        "description": "Atue, ensaie e produza peças teatrais da escola",
        "schedule": "Quartas-feiras, 15h30 - 17h",
        "max_participants": 20,
        "participants": [],
    },
    "Clube de Arte": {
        "description": "Explore o desenho, a pintura e outras artes visuais",
        "schedule": "Sextas-feiras, 15h30 - 17h",
        "max_participants": 18,
        "participants": [],
    },
    "Clube de Debate": {
        "description": "Pratique oratória, argumentação e pensamento crítico",
        "schedule": "Terças-feiras, 15h30 - 16h30",
        "max_participants": 16,
        "participants": [],
    },
    "Clube de Ciências": {
        "description": "Explore ideias científicas por meio de experimentos e projetos",
        "schedule": "Quintas-feiras, 15h30 - 16h30",
        "max_participants": 16,
        "participants": [],
    },
}

client = TestClient(app_module.app)


def reset_activities():
    app_module.activities.clear()
    app_module.activities.update(deepcopy(BASE_ACTIVITIES))


def test_get_activities_returns_all_activity_details():
    # Arrange
    reset_activities()

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Clube de Xadrez" in payload
    assert payload["Clube de Xadrez"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_for_activity_adds_student():
    # Arrange
    reset_activities()
    email = "newstudent@mergington.edu"

    # Act
    response = client.post("/activities/Clube de Xadrez/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Clube de Xadrez"}
    assert email in app_module.activities["Clube de Xadrez"]["participants"]


def test_signup_for_duplicate_student_returns_400():
    # Arrange
    reset_activities()
    email = "michael@mergington.edu"

    # Act
    response = client.post("/activities/Clube de Xadrez/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_for_unknown_activity_returns_404():
    # Arrange
    reset_activities()

    # Act
    response = client.post("/activities/Atividade Inexistente/signup", params={"email": "student@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_remove_participant_removes_student():
    # Arrange
    reset_activities()
    email = "daniel@mergington.edu"

    # Act
    response = client.delete(f"/activities/Clube de Xadrez/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from Clube de Xadrez"}
    assert email not in app_module.activities["Clube de Xadrez"]["participants"]


def test_remove_missing_participant_returns_404():
    # Arrange
    reset_activities()

    # Act
    response = client.delete("/activities/Clube de Xadrez/participants/ghost@mergington.edu")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found"}

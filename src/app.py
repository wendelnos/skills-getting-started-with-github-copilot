"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Clube de Xadrez": {
        "description": "Aprenda estratégias e participe de torneios de xadrez",
        "schedule": "Sextas-feiras, 15h30 - 17h",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Aula de Programação": {
        "description": "Aprenda os fundamentos da programação e desenvolva projetos de software",
        "schedule": "Terças e quintas-feiras, 15h30 - 16h30",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Aula de Educação Física": {
        "description": "Atividades de educação física e esportes",
        "schedule": "Segundas, quartas e sextas-feiras, 14h - 15h",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Time de Basquete": {
        "description": "Pratique habilidades de basquete e dispute partidas em equipe",
        "schedule": "Terças e quintas-feiras, 16h - 17h30",
        "max_participants": 15,
        "participants": []
    },
    "Clube de Futebol": {
        "description": "Desenvolva suas habilidades no futebol e jogue partidas amistosas",
        "schedule": "Segundas e quartas-feiras, 15h30 - 17h",
        "max_participants": 22,
        "participants": []
    },
    "Clube de Teatro": {
        "description": "Atue, ensaie e produza peças teatrais da escola",
        "schedule": "Quartas-feiras, 15h30 - 17h",
        "max_participants": 20,
        "participants": []
    },
    "Clube de Arte": {
        "description": "Explore o desenho, a pintura e outras artes visuais",
        "schedule": "Sextas-feiras, 15h30 - 17h",
        "max_participants": 18,
        "participants": []
    },
    "Clube de Debate": {
        "description": "Pratique oratória, argumentação e pensamento crítico",
        "schedule": "Terças-feiras, 15h30 - 16h30",
        "max_participants": 16,
        "participants": []
    },
    "Clube de Ciências": {
        "description": "Explore ideias científicas por meio de experimentos e projetos",
        "schedule": "Quintas-feiras, 15h30 - 16h30",
        "max_participants": 16,
        "participants": []
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities(response: Response):
    response.headers["Cache-Control"] = "no-store"
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants/{email}")
def remove_participant(activity_name: str, email: str):
    """Remove a student from an activity."""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    participants = activities[activity_name]["participants"]
    if email not in participants:
        raise HTTPException(status_code=404, detail="Participant not found")

    participants.remove(email)
    return {"message": f"Removed {email} from {activity_name}"}

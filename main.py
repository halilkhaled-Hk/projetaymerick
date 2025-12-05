import json
import uuid
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

# --- Modèles Pydantic ---


class ProjectSubmission(BaseModel):
    """Modèle pour la soumission initiale d'un projet."""

    studentName: str = Field(..., example="Alice Dupont")
    course: str = Field(..., example="Versionning et Gestion de Projet")
    githubUrl: str = Field(..., example="https://github.com/user/repo")


class Project(ProjectSubmission):
    """Modèle complet d'un projet, incluant l'ID et la note."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    grade: Optional[int] = Field(None, ge=0, le=20)


# --- Logique de gestion du fichier DB ---

DB_FILE = "db.json"


def load_db() -> List[Project]:
    """Charge les données depuis le fichier JSON."""
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Valider les données chargées avec le modèle Pydantic
            return [Project(**item) for item in data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        # Si le fichier est vide ou mal formé, retourner une liste vide
        return []


def save_db(projects: List[Project]):
    """Sauvegarde les données dans le fichier JSON."""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        # Convertir les modèles Pydantic en dictionnaires pour la sauvegarde
        json.dump([p.model_dump() for p in projects], f, indent=4)


# --- Initialisation de l'API ---

app = FastAPI(title="ProjetAPI ", version="0.1.0")

# Charger la base de données au démarrage
projects_db = load_db()


@app.get("/")
def read_root():
    return {"message"}


# --- Endpoint POST /projects ---


@app.post("/projects", response_model=Project, status_code=201)
def create_project(submission: ProjectSubmission):
    """Soumettre un nouveau projet."""
    global projects_db

    # Créer un nouvel objet Project avec un ID unique
    new_project = Project(**submission.model_dump())

    # Ajouter à la base de données en mémoire
    projects_db.append(new_project)

    # Sauvegarder sur le disque
    save_db(projects_db)

    return new_project

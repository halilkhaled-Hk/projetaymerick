from fastapi import FastAPI

app = FastAPI(
    title="ProjetAPI - Gestion des Soumissions de Projets Étudiants",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de gestion des soumissions de projets."}

# Le reste des endpoints sera ajouté dans les phases suivantes.

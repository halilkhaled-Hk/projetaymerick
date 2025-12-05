from fastapi import FastAPI

app = FastAPI(title="ProjetAPI ", version="0.1.0")


@app.get("/")
def read_root():
    return {"message": "Bienvenue "}


# Le reste des endpoints sera ajouté dans les phases suivantes.

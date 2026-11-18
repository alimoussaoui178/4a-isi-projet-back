from fastapi import APIRouter, FastAPI

app = FastAPI(
    title="Pol-eat-heck API",
    description="API du projet Pol-eat-heck (contrat back ↔ front)",
    version="0.1.0",
)

# Toutes les routes de l'API sont sous /api (voir le contrat).
# La racine / sera réservée au front, servi plus tard en fichiers statiques.
api = APIRouter(prefix="/api")


@api.get("/health", summary="Vérifier que l'API répond")
def health():
    return {"status": "ok"}


# Les routers (auth, users, products, menus, closing_days, orders)
# seront ajoutés ici à l'étape suivante avec api.include_router(...).

app.include_router(api)

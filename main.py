from fastapi import APIRouter, FastAPI

from routers import auth, closing_days, menus, orders, products, users

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


# Partie Yazi : utilisateurs et commandes
api.include_router(auth.router)
api.include_router(users.router)
api.include_router(orders.router)

# Partie Ali : catalogue (products, menus, closing_days)
api.include_router(products.router)
api.include_router(menus.router)
api.include_router(closing_days.router)

app.include_router(api)

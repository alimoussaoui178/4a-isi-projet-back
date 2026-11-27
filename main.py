import os
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routers import auth, closing_days, menus, orders, products, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Au démarrage du serveur : crée les tables manquantes dans polieatheck.db
    init_db()
    yield


app = FastAPI(
    title="Pol-eat-heck API",
    description="API du projet Pol-eat-heck (contrat back ↔ front)",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS (pour le développement) : autorise le front lancé sur un AUTRE serveur
# (ex. Live Server de VS Code sur le port 5500) à appeler l'API avec fetch.
# Sans ça, le navigateur bloque les réponses venant d'une autre origine.
# En production le front est servi par FastAPI sur la même origine : pas besoin de CORS.
# Liste des origines autorisées, séparées par des virgules, dans POLIEATHECK_CORS_ORIGINS.
CORS_ORIGINS = os.getenv(
    "POLIEATHECK_CORS_ORIGINS",
    "http://localhost:5500,http://127.0.0.1:5500",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in CORS_ORIGINS if origin.strip()],
    allow_methods=["*"],  # GET, POST, PATCH, DELETE...
    allow_headers=["*"],  # dont Authorization (le token) et Content-Type
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

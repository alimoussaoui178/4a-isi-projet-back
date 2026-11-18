"""Routes d'authentification (contrat : section « Authentification et compte »).

Palier 1 : routes déclarées mais vides.
"""

from fastapi import APIRouter

router = APIRouter(tags=["Authentification"])


@router.post("/auth/register", status_code=201, summary="Créer un compte (mot de passe généré)")
def register():
    # Palier 2 : renvoyer {"id", "username", "password"} en dur
    # Palier 3 : 409 si le nom est pris, générer + hasher le mot de passe
    pass


@router.post("/auth/login", summary="Se connecter et recevoir un token")
def login():
    # Palier 2 : renvoyer {"access_token", "token_type": "bearer", "user": User}
    # Palier 3 : 401 si identifiants faux, 403 si compte bloqué
    pass

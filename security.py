"""Sécurité : qui est connecté, et a-t-il le droit ?

PALIER 1 : VERSION BIDON.
Les deux dépendances ci-dessous renvoient toujours un faux utilisateur admin,
sans vérifier le token. Ça permet à tout le monde (Ali compris) de déclarer
dès maintenant les routes protégées avec Depends(...).
Au palier 3, on remplacera l'intérieur des fonctions (vérification du JWT,
compte bloqué, rôle) SANS changer leur nom ni leur utilisation.
"""

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# Lit le header "Authorization: Bearer <token>".
# auto_error=False : au palier 1, on accepte les requêtes sans token.
# Effet bonus : /docs affiche un bouton "Authorize" pour coller un token.
bearer_scheme = HTTPBearer(auto_error=False)

# Faux utilisateur au format "User" du contrat
FAKE_USER = {
    "id": 1,
    "username": "admin",
    "role": "admin",
    "is_blocked": False,
    "created_at": "2026-11-18T09:30:00",
}


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict:
    """Niveau d'accès "User" : token valide et compte non bloqué.

    Palier 3 : décoder le JWT, charger l'utilisateur,
    401 si token absent ou invalide, 403 si compte bloqué.
    """
    return FAKE_USER


def require_admin(user: dict = Depends(get_current_user)) -> dict:
    """Niveau d'accès "Admin" : token valide et rôle admin.

    Palier 3 : 403 si user["role"] != "admin".
    """
    return user

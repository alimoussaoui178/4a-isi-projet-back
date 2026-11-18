"""Routes du compte connecté et administration des utilisateurs.

Palier 1 : routes déclarées mais vides.
Les dépendances (get_current_user, require_admin) sont déjà en place :
elles sont bidon pour l'instant (voir security.py).
"""

from fastapi import APIRouter, Depends

from security import get_current_user, require_admin

router = APIRouter(tags=["Utilisateurs"])


# --- Compte de l'utilisateur connecté (accès User) ---

@router.get("/users/me", summary="Voir mon compte")
def read_me(user: dict = Depends(get_current_user)):
    pass


@router.patch("/users/me/password", status_code=204, summary="Changer mon mot de passe")
def change_password(user: dict = Depends(get_current_user)):
    # Palier 3 : 401 si l'ancien mot de passe est faux
    pass


# --- Administration (accès Admin) ---

@router.get("/users", summary="Lister tous les comptes (admin)")
def list_users(admin: dict = Depends(require_admin)):
    pass


@router.patch("/users/{user_id}/block", summary="Bloquer / débloquer un compte (admin)")
def block_user(user_id: int, admin: dict = Depends(require_admin)):
    # Corps : {"blocked": true|false} — 400 si l'admin se bloque lui-même
    pass

from fastapi import APIRouter, Depends

from models import User
from schemas.user import UserOut
from security import get_current_user, require_admin

router = APIRouter(tags=["Utilisateurs"])


@router.get("/users/me", response_model=UserOut, summary="Voir mon compte")
def read_me(user: User = Depends(get_current_user)):
    return user


@router.patch("/users/me/password", status_code=204, summary="Changer mon mot de passe")
def change_password(user: User = Depends(get_current_user)):
    pass


@router.get("/users", summary="Lister tous les comptes (admin)")
def list_users(admin: User = Depends(require_admin)):
    pass


@router.patch("/users/{user_id}/block", summary="Bloquer / débloquer un compte (admin)")
def block_user(user_id: int, admin: User = Depends(require_admin)):
    pass

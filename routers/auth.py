import secrets

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import User
from schemas.user import LoginIn, LoginOut, RegisterIn, RegisterOut
from security import create_access_token, hash_password, verify_password

router = APIRouter(tags=["Authentification"])


@router.post(
    "/auth/register",
    status_code=201,
    response_model=RegisterOut,
    summary="Créer un compte (mot de passe généré)",
)
def register(body: RegisterIn, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.username == body.username)).first()
    if existing is not None:
        raise HTTPException(status_code=409, detail="Ce nom d'utilisateur est déjà pris")

    password = secrets.token_urlsafe(9)
    user = User(username=body.username, password_hash=hash_password(password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return RegisterOut(id=user.id, username=user.username, password=password)


@router.post("/auth/login", response_model=LoginOut, summary="Se connecter et recevoir un token")
def login(body: LoginIn, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == body.username)).first()
    if user is None or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    if user.is_blocked:
        raise HTTPException(status_code=403, detail="Compte bloqué")

    return LoginOut(access_token=create_access_token(user), user=user.model_dump())

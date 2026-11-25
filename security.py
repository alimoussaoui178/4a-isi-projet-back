import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pwdlib import PasswordHash
from sqlmodel import Session

from database import get_session
from models import User

SECRET_KEY = os.getenv("POLIEATHECK_SECRET", "cle-de-dev-a-changer-en-production")
ALGORITHM = "HS256"
TOKEN_DURATION = timedelta(hours=24)

password_hasher = PasswordHash.recommended()
bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_hasher.verify(password, password_hash)


def create_access_token(user: User) -> str:
    expiration = datetime.now(timezone.utc) + TOKEN_DURATION
    payload = {"sub": str(user.id), "exp": expiration}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    session: Session = Depends(get_session),
) -> User:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Connexion requise")

    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")

    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")
    if user.is_blocked:
        raise HTTPException(status_code=403, detail="Compte bloqué")
    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Réservé aux administrateurs")
    return user

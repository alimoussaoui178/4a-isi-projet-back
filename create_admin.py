import sys

from sqlmodel import Session, select

from database import engine, init_db
from models import User
from security import hash_password


def main():
    if len(sys.argv) != 3:
        print("Utilisation : python create_admin.py <username> <password>")
        sys.exit(1)

    username, password = sys.argv[1], sys.argv[2]
    if len(password) < 8:
        print("Erreur : le mot de passe doit faire au moins 8 caractères.")
        sys.exit(1)

    init_db()
    with Session(engine) as session:
        existing = session.exec(select(User).where(User.username == username)).first()
        if existing is not None:
            print(f"Erreur : le nom « {username} » est déjà pris.")
            sys.exit(1)

        admin = User(username=username, password_hash=hash_password(password), role="admin")
        session.add(admin)
        session.commit()

    print(f"Admin « {username} » créé.")


if __name__ == "__main__":
    main()

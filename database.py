"""Connexion à la base SQLite.

- engine      : la connexion au fichier polieatheck.db
- get_session : dépendance FastAPI qui ouvre une session par requête
- init_db     : crée les tables si elles n'existent pas encore
"""

import os

from sqlalchemy import event
from sqlmodel import Session, SQLModel, create_engine

import models  # noqa: F401  (enregistre les 8 tables dans SQLModel.metadata)

# Chemin du fichier .db : variable d'environnement, sinon polieatheck.db à côté du code.
# Le fichier n'est pas versionné (*.db dans le .gitignore).
DATABASE_PATH = os.getenv("POLIEATHECK_DB", "polieatheck.db")

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}",
    # FastAPI peut traiter une requête dans un autre thread que celui
    # qui a ouvert la connexion : SQLite le refuse par défaut.
    connect_args={"check_same_thread": False},
)


@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    """SQLite désactive les clés étrangères par défaut : on les active
    à CHAQUE nouvelle connexion, sinon ON DELETE CASCADE et les FK sont ignorés."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.close()


def init_db() -> None:
    """Crée les tables manquantes (ne touche pas aux tables déjà créées
    par le schema.sql du dépôt db)."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dépendance FastAPI : une session par requête, fermée automatiquement.

    Utilisation dans une route : session: Session = Depends(get_session)
    """
    with Session(engine) as session:
        yield session

"""Schémas Pydantic des produits : le format JSON échangé avec le front.

Ce ne sont PAS les tables (elles sont dans models/) : ici on décrit ce que
l'API reçoit et renvoie. FastAPI s'en sert pour valider les données
(422 automatique si un champ manque ou a un mauvais type) et pour /docs.
"""

from pydantic import BaseModel, Field, field_validator


class ProductCreate(BaseModel):
    """Corps de POST /api/products."""

    name: str = Field(min_length=1)
    description: str | None = None
    price_cents: int = Field(ge=0)  # prix en centimes : 450 = 4,50 €
    stock: int = Field(default=0, ge=0)
    is_available: bool = True


class ProductUpdate(BaseModel):
    """Corps de PATCH /api/products/{id} : tous les champs sont facultatifs.

    Le front n'envoie que ce qu'il veut changer, ex. {"stock": 15}.
    """

    name: str | None = Field(default=None, min_length=1)
    description: str | None = None
    price_cents: int | None = Field(default=None, ge=0)
    stock: int | None = Field(default=None, ge=0)
    is_available: bool | None = None

    @field_validator("name", "price_cents", "stock", "is_available")
    @classmethod
    def refuser_null(cls, value):
        """Refuse un null ENVOYÉ explicitement pour une colonne NOT NULL.

        Sans ça, {"name": null} passait la validation puis SQLite le refusait :
        erreur 500. Maintenant c'est une erreur 422 claire.
        Un champ simplement absent n'est pas concerné : Pydantic ne lance pas
        ce validateur sur les valeurs par défaut, seulement sur ce qui est envoyé.
        (description peut rester null : sa colonne l'accepte.)
        """
        if value is None:
            raise ValueError("ce champ ne peut pas être null")
        return value


class ProductOut(BaseModel):
    """Objet « Product » du contrat, renvoyé par toutes les routes produits."""

    id: int
    name: str
    description: str | None
    price_cents: int
    stock: int
    is_available: bool

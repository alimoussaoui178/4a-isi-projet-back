"""Schémas Pydantic des menus : le format JSON échangé avec le front."""

from datetime import date

from pydantic import BaseModel, Field, model_validator

# Jours de la semaine : 0 = lundi ... 6 = dimanche (comme date.weekday() en Python).
# Point encore ouvert dans le contrat : si l'équipe choisit 0 = dimanche,
# seule la fonction menu_est_servi() de models/rules.py est à adapter.
Weekday = int


class Availability(BaseModel):
    """Disponibilité d'un menu.

    - start_date et end_date à null : menu permanent
    - start_date == end_date        : menu d'un seul jour
    - weekdays                      : jours servis (0 = lundi, 6 = dimanche)
    """

    start_date: date | None = None
    end_date: date | None = None
    weekdays: list[Weekday] = Field(default_factory=lambda: [0, 1, 2, 3, 4, 5, 6])

    @model_validator(mode="after")
    def check_coherence(self):
        # Même règle que le CHECK (end_date >= start_date) de la table menus
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date doit être après start_date")
        # Même règle que le CHECK (weekday BETWEEN 0 AND 6) de menu_weekdays
        if any(d < 0 or d > 6 for d in self.weekdays):
            raise ValueError("weekdays : chaque jour doit être entre 0 et 6")
        # Pas de doublon (clé primaire (menu_id, weekday)), et liste triée
        self.weekdays = sorted(set(self.weekdays))
        return self


class MenuProduct(BaseModel):
    """Produit d'un menu, tel qu'il apparaît dans Menu.products."""

    id: int
    name: str


class MenuCreate(BaseModel):
    """Corps de POST /api/menus."""

    name: str = Field(min_length=1)
    description: str | None = None
    price_cents: int = Field(ge=0)
    product_ids: list[int] = Field(min_length=1)
    availability: Availability = Field(default_factory=Availability)


class MenuOut(BaseModel):
    """Objet « Menu » du contrat."""

    id: int
    name: str
    description: str | None
    price_cents: int
    products: list[MenuProduct]
    availability: Availability

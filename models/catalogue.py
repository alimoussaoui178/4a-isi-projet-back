"""Tables du catalogue : products, menus, menu_products, menu_weekdays, closing_days.

Mêmes noms de tables et de colonnes que le schema.sql du dépôt 4a-isi-projet-db.
Les CHECK du contrat sont recopiés dans __table_args__ pour que
SQLModel.metadata.create_all() crée exactement les mêmes tables.

Correspondance des types (SQLite n'a ni booléen ni date) :
- bool  -> INTEGER 0 / 1
- date  -> TEXT 'YYYY-MM-DD' (se compare correctement comme du texte)
"""

import datetime as dt

from sqlalchemy import CheckConstraint
from sqlmodel import Field, Relationship, SQLModel


class MenuProduct(SQLModel, table=True):
    """Table de liaison : quels produits composent quel menu.

    Clé primaire composée (menu_id, product_id).
    Si on supprime un menu, ses lignes ici partent avec (ON DELETE CASCADE).
    """

    __tablename__ = "menu_products"

    menu_id: int = Field(foreign_key="menus.id", primary_key=True, ondelete="CASCADE")
    product_id: int = Field(foreign_key="products.id", primary_key=True)


class Product(SQLModel, table=True):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("price_cents >= 0", name="ck_products_price"),
        CheckConstraint("stock >= 0", name="ck_products_stock"),
    )

    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = None
    price_cents: int
    stock: int = 0
    is_available: bool = True


class MenuWeekday(SQLModel, table=True):
    """Un jour de la semaine où un menu est servi (0 = lundi ... 6 = dimanche)."""

    __tablename__ = "menu_weekdays"
    __table_args__ = (CheckConstraint("weekday BETWEEN 0 AND 6", name="ck_menu_weekdays_day"),)

    menu_id: int = Field(foreign_key="menus.id", primary_key=True, ondelete="CASCADE")
    weekday: int = Field(primary_key=True)


class Menu(SQLModel, table=True):
    __tablename__ = "menus"
    __table_args__ = (
        CheckConstraint("price_cents >= 0", name="ck_menus_price"),
        CheckConstraint("end_date >= start_date", name="ck_menus_dates"),
    )

    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = None
    price_cents: int
    start_date: dt.date | None = None  # NULL = pas de date de début
    end_date: dt.date | None = None  # NULL = pas de date de fin

    # Relations : pas des colonnes, mais des raccourcis Python vers les autres tables.
    # menu.products lit menu_products ; menu.weekdays lit menu_weekdays.
    products: list[Product] = Relationship(link_model=MenuProduct)
    weekdays: list[MenuWeekday] = Relationship(cascade_delete=True)


class ClosingDay(SQLModel, table=True):
    """Jour de fermeture. Pas de clé étrangère : le back la consulte avant une commande."""

    __tablename__ = "closing_days"

    date: dt.date = Field(primary_key=True)  # dt.date : évite le conflit avec le nom du champ
    reason: str | None = None

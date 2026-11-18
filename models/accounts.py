"""Tables des comptes et des commandes : users, orders, order_items.

Ces modèles sont utilisés par les routes de Yazi (auth, users, orders).
Mêmes noms de tables et de colonnes que le schema.sql du dépôt 4a-isi-projet-db.
"""

from datetime import date, datetime

from sqlalchemy import CheckConstraint
from sqlmodel import Field, SQLModel


def now_iso() -> str:
    """Horodatage au format du contrat : 'YYYY-MM-DDTHH:MM:SS'."""
    return datetime.now().isoformat(timespec="seconds")


class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = (CheckConstraint("role IN ('user', 'admin')", name="ck_users_role"),)

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    password_hash: str  # jamais renvoyé par l'API
    role: str = "user"
    is_blocked: bool = False
    created_at: str = Field(default_factory=now_iso)


class Order(SQLModel, table=True):
    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'picked_up', 'no_show', 'cancelled')",
            name="ck_orders_status",
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    pickup_date: date
    status: str = "pending"
    created_at: str = Field(default_factory=now_iso)


class OrderItem(SQLModel, table=True):
    """Une ligne de commande : pointe SOIT vers un produit, SOIT vers un menu."""

    __tablename__ = "order_items"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_order_items_quantity"),
        # Exactement une des deux colonnes est remplie, jamais les deux ni aucune
        CheckConstraint("(product_id IS NULL) <> (menu_id IS NULL)", name="ck_order_items_kind"),
    )

    id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", ondelete="CASCADE")
    product_id: int | None = Field(default=None, foreign_key="products.id")
    menu_id: int | None = Field(default=None, foreign_key="menus.id")
    quantity: int
    unit_price_cents: int  # prix copié au moment de la commande

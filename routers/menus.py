"""Routes des menus (contrat : section « Menus »).

Palier 4 : lecture et écriture dans la vraie base
(tables menus, menu_products, menu_weekdays).
L'admin peut créer, supprimer et régler la disponibilité d'un menu,
mais pas le modifier : le seul PATCH porte sur availability.
"""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from database import get_session
from models import Menu, MenuWeekday, Product, User
from regles import est_jour_ferme, menu_est_servi
from schemas.menu import Availability, MenuCreate, MenuOut
from security import require_admin

router = APIRouter(tags=["Menus"])


def menu_to_out(menu: Menu) -> MenuOut:
    """Convertit les lignes de la base vers l'objet « Menu » du contrat.

    Base : colonnes start_date / end_date + lignes de menu_products et menu_weekdays.
    API  : products = [{"id", "name"}] et availability = {start_date, end_date, weekdays}.
    """
    return MenuOut(
        id=menu.id,
        name=menu.name,
        description=menu.description,
        price_cents=menu.price_cents,
        products=[{"id": p.id, "name": p.name} for p in menu.products],
        availability=Availability(
            start_date=menu.start_date,
            end_date=menu.end_date,
            weekdays=[w.weekday for w in menu.weekdays],
        ),
    )


def get_menu_or_404(menu_id: int, session: Session) -> Menu:
    menu = session.get(Menu, menu_id)
    if menu is None:
        raise HTTPException(status_code=404, detail="Menu introuvable")
    return menu


def apply_availability(menu: Menu, availability: Availability) -> None:
    """Recopie la disponibilité de l'API dans les colonnes et la table menu_weekdays."""
    menu.start_date = availability.start_date
    menu.end_date = availability.end_date
    # On remplace toute la liste : SQLAlchemy supprime les anciennes lignes
    # de menu_weekdays et insère les nouvelles au commit.
    menu.weekdays = [MenuWeekday(weekday=d) for d in availability.weekdays]


# --- Lecture (accès Public) ---

@router.get("/menus", response_model=list[MenuOut], summary="Lister les menus")
def list_menus(date: date | None = None, session: Session = Depends(get_session)):
    menus = session.exec(select(Menu).order_by(Menu.name)).all()
    if date is not None:
        # ?date=2026-11-24 : seulement les menus servis ce jour-là,
        # et aucun si le restaurant est fermé
        if est_jour_ferme(date, session):
            return []
        menus = [m for m in menus if menu_est_servi(m, date)]
    return [menu_to_out(m) for m in menus]


@router.get("/menus/{menu_id}", response_model=MenuOut, summary="Voir un menu")
def read_menu(menu_id: int, session: Session = Depends(get_session)):
    return menu_to_out(get_menu_or_404(menu_id, session))


# --- Administration (accès Admin) ---

@router.post("/menus", status_code=201, response_model=MenuOut, summary="Créer un menu (admin)")
def create_menu(
    body: MenuCreate,
    admin: User = Depends(require_admin),
    session: Session = Depends(get_session),
):
    # 400 si un des product_ids n'existe pas
    products = []
    for product_id in dict.fromkeys(body.product_ids):  # dict.fromkeys : retire les doublons
        product = session.get(Product, product_id)
        if product is None:
            raise HTTPException(status_code=400, detail=f"Le produit {product_id} n'existe pas")
        products.append(product)

    menu = Menu(name=body.name, description=body.description, price_cents=body.price_cents)
    menu.products = products  # remplit menu_products au commit
    apply_availability(menu, body.availability)
    session.add(menu)
    session.commit()
    session.refresh(menu)
    return menu_to_out(menu)


@router.patch("/menus/{menu_id}/availability", response_model=MenuOut,
              summary="Changer la disponibilité d'un menu (admin)")
def update_menu_availability(
    menu_id: int,
    body: Availability,
    admin: User = Depends(require_admin),
    session: Session = Depends(get_session),
):
    menu = get_menu_or_404(menu_id, session)
    apply_availability(menu, body)
    session.add(menu)
    session.commit()
    session.refresh(menu)
    return menu_to_out(menu)


@router.delete("/menus/{menu_id}", status_code=204, summary="Supprimer un menu (admin)")
def delete_menu(
    menu_id: int,
    admin: User = Depends(require_admin),
    session: Session = Depends(get_session),
):
    menu = get_menu_or_404(menu_id, session)
    # menu_products et menu_weekdays partent avec (ON DELETE CASCADE)
    session.delete(menu)
    try:
        session.commit()
    except IntegrityError:
        # order_items référence ce menu : la clé étrangère bloque la suppression.
        session.rollback()
        raise HTTPException(status_code=409, detail="Menu déjà commandé : suppression impossible")

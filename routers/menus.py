"""Routes des menus (contrat : section « Menus »).

Palier 2 : données fictives écrites en dur, au format exact du contrat.
L'admin peut créer, supprimer et régler la disponibilité d'un menu,
mais pas le modifier : le seul PATCH porte sur availability.
"""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException

from schemas.menu import Availability, MenuCreate, MenuOut
from security import require_admin

router = APIRouter(tags=["Menus"])

FAKE_MENUS = [
    {
        "id": 5, "name": "Menu midi", "description": "Sandwich + boisson", "price_cents": 750,
        "products": [{"id": 3, "name": "Sandwich poulet"}, {"id": 8, "name": "Eau 50 cl"}],
        "availability": {"start_date": "2026-11-23", "end_date": "2026-11-29",
                         "weekdays": [0, 1, 2, 3, 4]},
    },
    {
        "id": 6, "name": "Menu salade", "description": "Salade + boisson", "price_cents": 700,
        "products": [{"id": 9, "name": "Salade César"}, {"id": 8, "name": "Eau 50 cl"}],
        "availability": {"start_date": None, "end_date": None, "weekdays": [0, 1, 2, 3, 4]},
    },
]


def find_fake(menu_id: int) -> dict:
    for m in FAKE_MENUS:
        if m["id"] == menu_id:
            return m
    raise HTTPException(status_code=404, detail="Menu introuvable")


# --- Lecture (accès Public) ---

@router.get("/menus", response_model=list[MenuOut], summary="Lister les menus")
def list_menus(date: date | None = None):
    # Palier 2 : le filtre ?date= est ignoré, il sera réel au palier 4
    return FAKE_MENUS


@router.get("/menus/{menu_id}", response_model=MenuOut, summary="Voir un menu")
def read_menu(menu_id: int):
    return find_fake(menu_id)


# --- Administration (accès Admin) ---

@router.post("/menus", status_code=201, response_model=MenuOut, summary="Créer un menu (admin)")
def create_menu(body: MenuCreate, admin: dict = Depends(require_admin)):
    return {
        "id": 99,
        "name": body.name,
        "description": body.description,
        "price_cents": body.price_cents,
        "products": [{"id": pid, "name": f"Produit {pid}"} for pid in body.product_ids],
        "availability": body.availability,
    }


@router.patch("/menus/{menu_id}/availability", response_model=MenuOut,
              summary="Changer la disponibilité d'un menu (admin)")
def update_menu_availability(menu_id: int, body: Availability, admin: dict = Depends(require_admin)):
    return {**find_fake(menu_id), "availability": body}


@router.delete("/menus/{menu_id}", status_code=204, summary="Supprimer un menu (admin)")
def delete_menu(menu_id: int, admin: dict = Depends(require_admin)):
    find_fake(menu_id)

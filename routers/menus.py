"""Routes des menus (contrat : section « Menus »).

Palier 1 : routes déclarées mais vides.
L'admin peut créer, supprimer et régler la disponibilité d'un menu,
mais pas le modifier : le seul PATCH porte sur availability.
"""

from datetime import date

from fastapi import APIRouter, Depends

from security import require_admin

router = APIRouter(tags=["Menus"])


# --- Lecture (accès Public) ---

@router.get("/menus", summary="Lister les menus")
def list_menus(date: date | None = None):
    # ?date=2026-11-24 : seulement les menus servis ce jour-là
    # (liste vide si c'est un jour de fermeture)
    pass


@router.get("/menus/{menu_id}", summary="Voir un menu")
def read_menu(menu_id: int):
    # 404 si le menu n'existe pas
    pass


# --- Administration (accès Admin) ---

@router.post("/menus", status_code=201, summary="Créer un menu (admin)")
def create_menu(admin: dict = Depends(require_admin)):
    # 400 si un des product_ids n'existe pas
    pass


@router.patch("/menus/{menu_id}/availability", summary="Changer la disponibilité d'un menu (admin)")
def update_menu_availability(menu_id: int, admin: dict = Depends(require_admin)):
    # Corps : {"start_date", "end_date", "weekdays"}
    pass


@router.delete("/menus/{menu_id}", status_code=204, summary="Supprimer un menu (admin)")
def delete_menu(menu_id: int, admin: dict = Depends(require_admin)):
    pass

"""Routes des commandes (contrat : section « Commandes »).

Palier 1 : routes déclarées mais vides.
"""

from datetime import date

from fastapi import APIRouter, Depends

from security import get_current_user, require_admin

router = APIRouter(tags=["Commandes"])


# --- Côté utilisateur ---

@router.post("/orders", status_code=201, summary="Passer une commande")
def create_order(user: dict = Depends(get_current_user)):
    # Palier 4 : les 5 vérifications du contrat, dans l'ordre
    # (date future, pas fermé, menus servis / produits dispo, stock suffisant)
    pass


@router.get("/users/me/orders", summary="Mes commandes")
def my_orders(user: dict = Depends(get_current_user)):
    pass


@router.get("/orders/{order_id}", summary="Voir une commande (la sienne, ou admin)")
def read_order(order_id: int, user: dict = Depends(get_current_user)):
    # 404 (et pas 403) si la commande appartient à quelqu'un d'autre
    pass


@router.delete("/orders/{order_id}", status_code=204, summary="Annuler ma commande (optionnel)")
def cancel_order(order_id: int, user: dict = Depends(get_current_user)):
    pass


# --- Côté admin ---

@router.get("/orders", summary="Commandes d'un jour de retrait (admin)")
def orders_by_date(date: date, admin: dict = Depends(require_admin)):
    # ?date=2026-11-24 — FastAPI vérifie tout seul le format (422 sinon)
    pass


@router.patch("/orders/{order_id}/status", summary="Changer le statut d'une commande (admin)")
def update_order_status(order_id: int, admin: dict = Depends(require_admin)):
    # Corps : {"status": "picked_up" | "no_show"}
    pass

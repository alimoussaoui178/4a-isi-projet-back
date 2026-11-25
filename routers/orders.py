from datetime import date

from fastapi import APIRouter, Depends

from models import User
from security import get_current_user, require_admin

router = APIRouter(tags=["Commandes"])


@router.post("/orders", status_code=201, summary="Passer une commande")
def create_order(user: User = Depends(get_current_user)):
    pass


@router.get("/users/me/orders", summary="Mes commandes")
def my_orders(user: User = Depends(get_current_user)):
    pass


@router.get("/orders/{order_id}", summary="Voir une commande (la sienne, ou admin)")
def read_order(order_id: int, user: User = Depends(get_current_user)):
    pass


@router.delete("/orders/{order_id}", status_code=204, summary="Annuler ma commande (optionnel)")
def cancel_order(order_id: int, user: User = Depends(get_current_user)):
    pass


@router.get("/orders", summary="Commandes d'un jour de retrait (admin)")
def orders_by_date(date: date, admin: User = Depends(require_admin)):
    pass


@router.patch("/orders/{order_id}/status", summary="Changer le statut d'une commande (admin)")
def update_order_status(order_id: int, admin: User = Depends(require_admin)):
    pass

"""Routes des produits (contrat : section « Produits »).

Palier 2 : données fictives écrites en dur, au format exact du contrat.
Lecture publique, modification réservée à l'admin.
"""

from fastapi import APIRouter, Depends, HTTPException

from schemas.product import ProductCreate, ProductOut, ProductUpdate
from security import require_admin

router = APIRouter(tags=["Produits"])

FAKE_PRODUCTS = [
    {"id": 3, "name": "Sandwich poulet", "description": "Pain complet, poulet, crudités",
     "price_cents": 450, "stock": 20, "is_available": True},
    {"id": 8, "name": "Eau 50 cl", "description": None,
     "price_cents": 100, "stock": 50, "is_available": True},
    {"id": 9, "name": "Salade César", "description": "Poulet, parmesan, croûtons",
     "price_cents": 550, "stock": 0, "is_available": True},
]


def find_fake(product_id: int) -> dict:
    for p in FAKE_PRODUCTS:
        if p["id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail="Produit introuvable")


# --- Lecture (accès Public) ---

@router.get("/products", response_model=list[ProductOut], summary="Lister les produits")
def list_products(available: bool = False):
    # ?available=true : seulement les produits disponibles ET en stock
    if available:
        return [p for p in FAKE_PRODUCTS if p["is_available"] and p["stock"] > 0]
    return FAKE_PRODUCTS


@router.get("/products/{product_id}", response_model=ProductOut, summary="Voir un produit")
def read_product(product_id: int):
    return find_fake(product_id)


# --- Administration (accès Admin) ---

@router.post("/products", status_code=201, response_model=ProductOut, summary="Créer un produit (admin)")
def create_product(body: ProductCreate, admin: dict = Depends(require_admin)):
    return {"id": 99, **body.model_dump()}


@router.patch("/products/{product_id}", response_model=ProductOut, summary="Modifier un produit (admin)")
def update_product(product_id: int, body: ProductUpdate, admin: dict = Depends(require_admin)):
    # exclude_unset : on ne garde que les champs réellement envoyés par le front
    return {**find_fake(product_id), **body.model_dump(exclude_unset=True)}


@router.delete("/products/{product_id}", status_code=204, summary="Supprimer un produit (admin)")
def delete_product(product_id: int, admin: dict = Depends(require_admin)):
    find_fake(product_id)

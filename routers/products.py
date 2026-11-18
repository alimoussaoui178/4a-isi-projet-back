"""Routes des produits (contrat : section « Produits »).

Palier 1 : routes déclarées mais vides.
Lecture publique, modification réservée à l'admin.
"""

from fastapi import APIRouter, Depends

from security import require_admin

router = APIRouter(tags=["Produits"])


# --- Lecture (accès Public) ---

@router.get("/products", summary="Lister les produits")
def list_products(available: bool = False):
    # ?available=true : seulement les produits disponibles ET en stock
    pass


@router.get("/products/{product_id}", summary="Voir un produit")
def read_product(product_id: int):
    # 404 si le produit n'existe pas
    pass


# --- Administration (accès Admin) ---

@router.post("/products", status_code=201, summary="Créer un produit (admin)")
def create_product(admin: dict = Depends(require_admin)):
    pass


@router.patch("/products/{product_id}", summary="Modifier un produit (admin)")
def update_product(product_id: int, admin: dict = Depends(require_admin)):
    # Seulement les champs envoyés, ex. {"stock": 15}
    pass


@router.delete("/products/{product_id}", status_code=204, summary="Supprimer un produit (admin)")
def delete_product(product_id: int, admin: dict = Depends(require_admin)):
    pass

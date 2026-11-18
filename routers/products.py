"""Routes des produits (contrat : section « Produits »).

Palier 4 : lecture et écriture dans la vraie base (table products).
Lecture publique, modification réservée à l'admin.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from database import get_session
from models import Product
from schemas.product import ProductCreate, ProductOut, ProductUpdate
from security import require_admin

router = APIRouter(tags=["Produits"])


def get_product_or_404(product_id: int, session: Session) -> Product:
    product = session.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return product


# --- Lecture (accès Public) ---

@router.get("/products", response_model=list[ProductOut], summary="Lister les produits")
def list_products(available: bool = False, session: Session = Depends(get_session)):
    query = select(Product).order_by(Product.name)
    if available:
        # ?available=true : seulement les produits disponibles ET en stock
        query = query.where(Product.is_available == True, Product.stock > 0)  # noqa: E712
    return session.exec(query).all()


@router.get("/products/{product_id}", response_model=ProductOut, summary="Voir un produit")
def read_product(product_id: int, session: Session = Depends(get_session)):
    return get_product_or_404(product_id, session)


# --- Administration (accès Admin) ---

@router.post("/products", status_code=201, response_model=ProductOut, summary="Créer un produit (admin)")
def create_product(
    body: ProductCreate,
    admin: dict = Depends(require_admin),
    session: Session = Depends(get_session),
):
    product = Product(**body.model_dump())
    session.add(product)
    session.commit()
    session.refresh(product)  # récupère l'id généré par SQLite
    return product


@router.patch("/products/{product_id}", response_model=ProductOut, summary="Modifier un produit (admin)")
def update_product(
    product_id: int,
    body: ProductUpdate,
    admin: dict = Depends(require_admin),
    session: Session = Depends(get_session),
):
    product = get_product_or_404(product_id, session)
    # exclude_unset : on ne change que les champs réellement envoyés par le front
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@router.delete("/products/{product_id}", status_code=204, summary="Supprimer un produit (admin)")
def delete_product(
    product_id: int,
    admin: dict = Depends(require_admin),
    session: Session = Depends(get_session),
):
    product = get_product_or_404(product_id, session)
    session.delete(product)
    try:
        session.commit()
    except IntegrityError:
        # Les clés étrangères de menu_products / order_items bloquent la suppression.
        # Point ouvert du contrat (archivage ?) : en attendant, on refuse proprement.
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Produit utilisé dans un menu ou une commande : rendez-le indisponible plutôt",
        )

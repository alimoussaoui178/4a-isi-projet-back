"""Routes des jours de fermeture (contrat : section « Jours de fermeture »).

Palier 1 : routes déclarées mais vides.
Lecture publique (le front grise ces jours dans son calendrier).
"""

from datetime import date

from fastapi import APIRouter, Depends

from security import require_admin

router = APIRouter(tags=["Jours de fermeture"])


@router.get("/closing-days", summary="Jours de fermeture d'une période")
def list_closing_days(start: date, end: date):
    # ?start=2026-11-01&end=2026-11-30
    pass


@router.post("/closing-days", status_code=201, summary="Ajouter un jour de fermeture (admin)")
def create_closing_day(admin: dict = Depends(require_admin)):
    # 409 si la date est déjà fermée, 400 si elle est déjà passée
    pass


@router.delete("/closing-days/{day}", status_code=204, summary="Rouvrir un jour (admin)")
def delete_closing_day(day: date, admin: dict = Depends(require_admin)):
    pass

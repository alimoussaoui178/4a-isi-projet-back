"""Routes des jours de fermeture (contrat : section « Jours de fermeture »).

Palier 2 : données fictives écrites en dur, au format exact du contrat.
Lecture publique (le front grise ces jours dans son calendrier).
"""

from datetime import date

from fastapi import APIRouter, Depends

from schemas.closing_day import ClosingDayCreate, ClosingDayOut
from security import require_admin

router = APIRouter(tags=["Jours de fermeture"])

FAKE_CLOSING_DAYS = [
    {"date": "2026-11-11", "reason": "Armistice"},
    {"date": "2026-12-25", "reason": "Noël"},
]


@router.get("/closing-days", response_model=list[ClosingDayOut], summary="Jours de fermeture d'une période")
def list_closing_days(start: date, end: date):
    # ?start=2026-11-01&end=2026-11-30 (dates incluses)
    # Les dates au format YYYY-MM-DD se comparent correctement comme du texte
    return [d for d in FAKE_CLOSING_DAYS if start.isoformat() <= d["date"] <= end.isoformat()]


@router.post("/closing-days", status_code=201, response_model=ClosingDayOut,
             summary="Ajouter un jour de fermeture (admin)")
def create_closing_day(body: ClosingDayCreate, admin: dict = Depends(require_admin)):
    return body


@router.delete("/closing-days/{day}", status_code=204, summary="Rouvrir un jour (admin)")
def delete_closing_day(day: date, admin: dict = Depends(require_admin)):
    pass

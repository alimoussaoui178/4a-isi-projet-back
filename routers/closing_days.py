"""Routes des jours de fermeture (contrat : section « Jours de fermeture »).

Palier 4 : lecture et écriture dans la vraie base (table closing_days).
Lecture publique (le front grise ces jours dans son calendrier).
"""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import ClosingDay
from schemas.closing_day import ClosingDayCreate, ClosingDayOut
from security import require_admin

router = APIRouter(tags=["Jours de fermeture"])


@router.get("/closing-days", response_model=list[ClosingDayOut], summary="Jours de fermeture d'une période")
def list_closing_days(start: date, end: date, session: Session = Depends(get_session)):
    # ?start=2026-11-01&end=2026-11-30 (dates incluses)
    query = (
        select(ClosingDay)
        .where(ClosingDay.date >= start, ClosingDay.date <= end)
        .order_by(ClosingDay.date)
    )
    return session.exec(query).all()


@router.post("/closing-days", status_code=201, response_model=ClosingDayOut,
             summary="Ajouter un jour de fermeture (admin)")
def create_closing_day(
    body: ClosingDayCreate,
    admin: dict = Depends(require_admin),
    session: Session = Depends(get_session),
):
    if body.date < date.today():
        raise HTTPException(status_code=400, detail="Cette date est déjà passée")
    if session.get(ClosingDay, body.date) is not None:
        raise HTTPException(status_code=409, detail="Ce jour est déjà fermé")
    closing_day = ClosingDay(date=body.date, reason=body.reason)
    session.add(closing_day)
    session.commit()
    session.refresh(closing_day)
    return closing_day


@router.delete("/closing-days/{day}", status_code=204, summary="Rouvrir un jour (admin)")
def delete_closing_day(
    day: date,
    admin: dict = Depends(require_admin),
    session: Session = Depends(get_session),
):
    closing_day = session.get(ClosingDay, day)
    if closing_day is None:
        raise HTTPException(status_code=404, detail="Ce jour n'est pas fermé")
    session.delete(closing_day)
    session.commit()

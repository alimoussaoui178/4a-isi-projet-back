"""Schémas Pydantic des jours de fermeture."""

import datetime as dt

from pydantic import BaseModel


class ClosingDayCreate(BaseModel):
    """Corps de POST /api/closing-days."""

    date: dt.date  # dt.date : évite le conflit entre le champ « date » et le type « date »
    reason: str | None = None


class ClosingDayOut(BaseModel):
    """Objet « ClosingDay » du contrat : {"date": "2026-12-25", "reason": "Noël"}."""

    date: dt.date  # dt.date : évite le conflit entre le champ « date » et le type « date »
    reason: str | None

"""Règles métier du catalogue, réutilisées pour valider les commandes.

- est_jour_ferme(day, session) : le restaurant est-il fermé ce jour-là ?
- menu_est_servi(menu, day)    : ce menu est-il servi ce jour-là ?
"""

from datetime import date

from sqlmodel import Session

from models import ClosingDay, Menu


def est_jour_ferme(day: date, session: Session) -> bool:
    """Vrai si `day` est dans la table closing_days."""
    return session.get(ClosingDay, day) is not None


def menu_est_servi(menu: Menu, day: date) -> bool:
    """Vrai si le menu est servi le jour `day`.

    Trois conditions :
    1. day >= start_date (si start_date est renseignée)
    2. day <= end_date   (si end_date est renseignée)
    3. le jour de la semaine de `day` est dans menu.weekdays

    Ne regarde PAS les jours de fermeture : c'est est_jour_ferme() qui s'en charge.
    """
    if menu.start_date is not None and day < menu.start_date:
        return False
    if menu.end_date is not None and day > menu.end_date:
        return False
    # Convention : 0 = lundi ... 6 = dimanche, comme date.weekday() en Python.
    # Si l'équipe choisit 0 = dimanche : remplacer par (day.weekday() + 1) % 7
    jours_servis = {w.weekday for w in menu.weekdays}
    return day.weekday() in jours_servis

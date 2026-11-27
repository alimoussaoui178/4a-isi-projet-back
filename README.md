# 4a-isi-projet-back

Back-end du projet **Pol-eat-heck** : une API REST qui permet de consulter des produits et des menus de la semaine, et de les réserver à l'avance. Le paiement se fait sur place, il n'est pas géré par l'application.

Stack : Python 3.11, [FastAPI](https://fastapi.tiangolo.com/), [SQLModel](https://sqlmodel.tiangolo.com/), SQLite, pwdlib (Argon2) et PyJWT.

## Collaborateurs

- [alimoussaoui178](https://github.com/alimoussaoui178)
- [shawskyy](https://github.com/shawskyy)
- [simosaj](https://github.com/simosaj)
- [mouaad009](https://github.com/mouaad009)
- [esirem-chassel](https://github.com/esirem-chassel) (enseignant)

## Autres dépôts

- [4a-isi-projet-db](https://github.com/alimoussaoui178/4a-isi-projet-db) : schéma de la base et données de test
- [4a-isi-projet-front](https://github.com/alimoussaoui178/4a-isi-projet-front) : interface web en HTML, CSS et JavaScript
- [4a-isi-projet-back](https://github.com/alimoussaoui178/4a-isi-projet-back) : ce dépôt

## Installation

À faire une seule fois, après le clone :

```bash
git clone https://github.com/alimoussaoui178/4a-isi-projet-back.git
cd 4a-isi-projet-back
python -m venv .venv
```

Activer le venv, à faire à chaque nouveau terminal :

| Système | Commande |
|---|---|
| Windows (PowerShell) | `Set-ExecutionPolicy -Scope Process RemoteSigned` puis `.\.venv\Scripts\Activate.ps1` |
| Windows (Git Bash) | `source .venv/Scripts/activate` |
| Linux, macOS, Raspberry | `source .venv/bin/activate` |

Installer les dépendances, avec le venv actif :

```bash
pip install -r requirements.txt
```

## Lancement

```bash
fastapi dev
```

- API : http://localhost:8000/api
- Documentation interactive (Swagger) : http://localhost:8000/docs
- Test rapide : http://localhost:8000/api/health doit renvoyer `{"status": "ok"}`

`fastapi dev` recharge le serveur à chaque modification de fichier. En production, on utilise `fastapi run` à la place.

## Base de données

La base est un seul fichier SQLite, `polieatheck.db`. Il n'est pas versionné (`*.db` est dans le `.gitignore`) : chacun a sa propre base sur sa machine.

**Création** : les 8 tables sont créées automatiquement au démarrage du serveur, par `init_db()` dans `database.py`, qui appelle `SQLModel.metadata.create_all()`. Cette fonction ne crée que les tables manquantes : elle ne touche ni aux tables ni aux données existantes.

**Repartir de zéro** : arrêter le serveur, supprimer `polieatheck.db`, puis relancer `fastapi dev`.

Les clés étrangères sont activées à chaque connexion (`PRAGMA foreign_keys = ON`).

> Le choix entre `create_all()` côté back et le `schema.sql` du dépôt db est encore à trancher avec l'équipe db. Pour l'instant, c'est le back qui crée les tables.

## Créer un compte administrateur

Un admin ne peut être créé **qu'en ligne de commande**, sur la machine du serveur. Il n'existe ni route ni page pour ça. Avec le venv actif :

```bash
python create_admin.py <nom> <mot_de_passe>
```

Remplace `<nom>` et `<mot_de_passe>` par tes valeurs, **sans les chevrons**. Le mot de passe doit faire au moins 8 caractères.

Pour utiliser les routes admin dans `/docs` :

1. `POST /api/auth/login` avec ce nom et ce mot de passe.
2. Copier la valeur de `access_token` dans la réponse.
3. Cliquer sur **Authorize** en haut de la page et coller le token.

Sans token, une route admin répond 401. Avec le token d'un simple utilisateur, elle répond 403.

## Variables d'environnement

Toutes ont une valeur par défaut, pour que `fastapi dev` marche sans rien configurer.

| Variable | Rôle | Valeur par défaut |
|---|---|---|
| `POLIEATHECK_DB` | Chemin du fichier SQLite | `polieatheck.db` |
| `POLIEATHECK_SECRET` | Clé de signature des tokens JWT | une clé de développement : **à changer en production** |
| `POLIEATHECK_CORS_ORIGINS` | Origines autorisées à appeler l'API depuis un autre serveur, séparées par des virgules | `http://localhost:5500,http://127.0.0.1:5500` (Live Server) |
| `POLIEATHECK_FRONT_DIR` | Dossier du front servi sur `/` | à venir |

La vraie clé secrète ne doit **jamais** être commitée. Exemple en PowerShell :

```powershell
$env:POLIEATHECK_SECRET = "une-longue-cle-aleatoire"
fastapi dev
```

## Organisation du code

```
main.py            point d'entrée : crée l'app, le CORS, et branche les routers sous /api
database.py        connexion SQLite, get_session, init_db
models/            les 8 tables SQLModel (mêmes noms que le dépôt db)
schemas/           le format JSON de l'API (ce que le front envoie et reçoit)
routers/           les routes, une famille par fichier
regles.py          règles métier : jour de fermeture, menu servi tel jour
security.py        hash des mots de passe, token JWT, get_current_user, require_admin
create_admin.py    script en ligne de commande pour créer un admin
```

Une requête passe par `main.py`, puis par le router concerné. Le router valide le JSON avec un schéma, vérifie les droits avec `security.py`, lit ou écrit la base via `database.py` et `models/`, puis renvoie la réponse au format du schéma.

## Routes

Toutes les routes sont sous `/api` et échangent du JSON. Le détail des corps et des réponses est dans le document « Contrat d'API (back ↔ front) » et dans `/docs`.

| Famille | Routes | Accès |
|---|---|---|
| Authentification | `POST /auth/register`, `POST /auth/login` | Public |
| Compte | `GET /users/me`, `PATCH /users/me/password` | User |
| Utilisateurs | `GET /users`, `PATCH /users/{id}/block` | Admin |
| Produits | `GET /products`, `GET /products/{id}` | Public |
| | `POST /products`, `PATCH /products/{id}`, `DELETE /products/{id}` | Admin |
| Menus | `GET /menus` (et `?date=`), `GET /menus/{id}` | Public |
| | `POST /menus`, `PATCH /menus/{id}/availability`, `DELETE /menus/{id}` | Admin |
| Jours de fermeture | `GET /closing-days?start=&end=` | Public |
| | `POST /closing-days`, `DELETE /closing-days/{date}` | Admin |
| Commandes | `POST /orders`, `GET /users/me/orders`, `GET /orders/{id}`, `DELETE /orders/{id}` | User |
| | `GET /orders?date=`, `PATCH /orders/{id}/status` | Admin |

## Conventions

- Prix en **centimes** (`450` = 4,50 €).
- Dates au format `YYYY-MM-DD`, horodatages au format `YYYY-MM-DDTHH:MM:SS`.
- Jours de la semaine : `0` = lundi … `6` = dimanche.
- Erreurs au format `{"detail": "message"}`.

## Travailler sur le projet

Une tâche = une branche = une pull request vers `main` :

```bash
git checkout main
git pull
git checkout -b <prenom>/<sujet>
# coder, tester dans /docs
git add <fichiers>
git commit -m "message clair"
git push -u origin <prenom>/<sujet>
```

Ensuite, ouvrir la pull request sur GitHub. On ne pousse jamais directement sur `main`.

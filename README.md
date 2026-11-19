# tp2_cicd

API FastAPI + PostgreSQL 16, lancée avec Docker Compose.

## Prérequis

- Docker Desktop
- Un fichier `.env` à la racine avec :

```env
POSTGRES_PASSWORD=motdepasse
POSTGRES_DB=shop
```

## Lancer

```powershell
docker compose up --build
```

L'API est disponible sur http://localhost:8000.

Pour repartir d'une base vide (rejoue `init.sql`) :

```powershell
docker compose down -v
docker compose up --build
```

## Endpoints

| Méthode | Route       | Description                          |
|---------|-------------|--------------------------------------|
| GET     | `/health`   | Statut de l'API                      |
| GET     | `/products` | Liste des produits                   |
| PUT     | `/products/{id}/stock` | Déclare le stock d'un produit (`{"user_id": 1, "quantity": 10}`) |
| GET     | `/products/{id}/stock?user_id=1` | Consulte le stock d'un producteur |
| POST    | `/orders`   | Crée une commande et décrémente le stock (`{"user_id": 1, "items": [{"product_id": 1, "quantity": 2}]}`) |

Exemple :

```powershell
curl http://localhost:8000/products
curl -X POST http://localhost:8000/orders -H "Content-Type: application/json" -d "{\"user_id\":1,\"items\":[{\"product_id\":1,\"quantity\":2}]}"
```

## Structure

- `app/main.py` : toute l'API FastAPI, découpée en sections (modèles, santé, produits, stock, commandes)
- `tests/` : tests automatiques (`python -m pytest`)
- `init.sql` : création des tables, utilisateurs et 1 200 produits de test
- `docker-compose.yml` : services `db` et `api`
- `requirements.txt` : dépendances Python

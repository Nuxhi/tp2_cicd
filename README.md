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
| POST    | `/orders`   | Crée une commande `{"product_id", "quantity"}` |

Exemple :

```powershell
curl http://localhost:8000/products
curl -X POST http://localhost:8000/orders -H "Content-Type: application/json" -d "{\"product_id\":1,\"quantity\":2}"
```

## Structure

- `app/main.py` : routes FastAPI
- `init.sql` : création des tables `products` et `orders` + données de test
- `docker-compose.yml` : services `db` et `api`
- `requirements.txt` : dépendances Python

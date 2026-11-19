import os

# main.py lit DATABASE_URL à l'import ; les tests n'ouvrent jamais de vraie connexion.
os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost:5432/test")

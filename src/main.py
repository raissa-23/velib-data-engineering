import os
from dotenv import load_dotenv

# Charge les variables du fichier .env
load_dotenv()

# Récupère les variables d'environnement
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "velib_db")
db_user = os.getenv("DB_USER", "postgres")

print("=" * 50)
print("🚀 Vélib Data Engineering Project")
print("=" * 50)
print(f"✅ Database Host: {db_host}")
print(f"✅ Database Port: {db_port}")
print(f"✅ Database Name: {db_name}")
print(f"✅ Database User: {db_user}")
print("=" * 50)
print("Application démarrée avec succès!")
print("=" * 50)

import os
from dotenv import load_dotenv
from db_handler import DatabaseHandler
from data_ingestion import DataIngestion
from etl_pipeline import ETLPipeline

load_dotenv()

print("\n" + "=" * 60)
print("🚀 VÉLIB DATA ENGINEERING PROJECT")
print("=" * 60)

# Initialiser la base de données
print("\n📦 Step 1: Testing Database Connection...")
print("-" * 60)
db = DatabaseHandler()
db.test_connection()
db.get_tables()

# Récupérer et insérer les données des APIs
print("\n🌐 Step 2: Fetching and Inserting Data from APIs...")
print("-" * 60)
ingestion = DataIngestion(db)
ingestion.fetch_and_insert_all()

# Exécuter le pipeline ETL
print("\n🔄 Step 3: Running ETL Pipeline...")
print("-" * 60)
etl = ETLPipeline(db)
etl.run_full_pipeline()

print("\n" + "=" * 60)
print("✅ All steps completed!")
print("=" * 60 + "\n")

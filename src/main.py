import os
from dotenv import load_dotenv
from db_handler import DatabaseHandler
from api_handler import test_apis

load_dotenv()

print("\n" + "=" * 60)
print("🚀 VÉLIB DATA ENGINEERING PROJECT")
print("=" * 60)

# Test 1 : Connexion à la base de données
print("\n📦 Step 1: Testing Database Connection...")
print("-" * 60)
db = DatabaseHandler()
db.test_connection()
db.get_tables()

# Test 2 : Test des APIs
print("\n🌐 Step 2: Testing APIs...")
print("-" * 60)
velib_data, weather_data = test_apis()

# Affiche les résultats
print("\n📊 Results:")
print("-" * 60)
if velib_data:
    print(f"✅ Vélib: {len(velib_data)} stations retrieved")
else:
    print("❌ Vélib: No data")

if weather_data:
    print(f"✅ Weather: Temperature {weather_data.get('temperature_2m')}°C")
else:
    print("❌ Weather: No data")

print("=" * 60)
print("✅ All tests completed!")
print("=" * 60 + "\n")

import requests
import json
from datetime import datetime

# API URLs
VELIB_API_URL = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-emplacement-des-stations-et-donnees-temps-reel&rows=1000"
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

# Coordonnées de Paris
PARIS_LATITUDE = 48.8566
PARIS_LONGITUDE = 2.3522

def fetch_velib_data():
    """
    Récupère les données du Vélib via l'API Open Data Paris
    """
    try:
        response = requests.get(VELIB_API_URL)
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Vélib data fetched: {len(data['records'])} stations found")
        return data['records']
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching Vélib data: {e}")
        return None

def fetch_weather_data():
    """
    Récupère les données météo via l'API Open Meteo
    """
    params = {
        "latitude": PARIS_LATITUDE,
        "longitude": PARIS_LONGITUDE,
        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,precipitation",
        "timezone": "Europe/Paris"
    }
    
    try:
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Weather data fetched at {data['current']['time']}")
        return data['current']
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching weather data: {e}")
        return None

def test_apis():
    """
    Fonction de test pour vérifier que les APIs fonctionnent
    """
    print("=" * 50)
    print("🧪 Testing APIs...")
    print("=" * 50)
    
    # Test Vélib
    velib_data = fetch_velib_data()
    
    # Test Météo
    weather_data = fetch_weather_data()
    
    print("=" * 50)
    print("✅ API tests completed!")
    print("=" * 50)
    
    return velib_data, weather_data

if __name__ == "__main__":
    test_apis()

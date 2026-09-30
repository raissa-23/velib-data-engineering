from db_handler import DatabaseHandler
from api_handler import fetch_weather_data, fetch_velib_data
from sqlalchemy import text
from datetime import datetime

class DataIngestion:
    """Récupère les données des APIs et les insère dans PostgreSQL"""
    
    def __init__(self, db_handler):
        self.db = db_handler
    
    def insert_weather(self, weather_data):
        """Insère les données météo dans PostgreSQL"""
        try:
            if not weather_data:
                return False
            
            with self.db.engine.connect() as conn:
                query = text("""
                    INSERT INTO weather (timestamp, temperature, humidity, wind_speed, precipitation, weather_code)
                    VALUES (:timestamp, :temperature, :humidity, :wind_speed, :precipitation, :weather_code)
                    ON CONFLICT DO NOTHING
                """)
                
                conn.execute(query, {
                    'timestamp': datetime.now(),
                    'temperature': weather_data.get('temperature_2m', 0),
                    'humidity': weather_data.get('relative_humidity_2m', 0),
                    'wind_speed': weather_data.get('wind_speed_10m', 0),
                    'precipitation': weather_data.get('precipitation', 0),
                    'weather_code': weather_data.get('weather_code', 0)
                })
                conn.commit()
                print("✅ Weather data inserted")
                return True
        except Exception as e:
            print(f"❌ Error inserting weather data: {e}")
            return False
    
    def insert_velib(self, velib_stations):
        """Insère les données Vélib dans PostgreSQL"""
        try:
            if not velib_stations:
                return False
            
            with self.db.engine.connect() as conn:
                # Insérer les stations d'abord
                for station in velib_stations[:5]:  # Limiter à 5 stations pour tester
                    station_data = station.get('fields', {})
                    
                    insert_station = text("""
                        INSERT INTO stations (station_id, station_name, latitude, longitude, capacity)
                        VALUES (:station_id, :name, :lat, :lon, :capacity)
                        ON CONFLICT DO NOTHING
                    """)
                    
                    conn.execute(insert_station, {
                        'station_id': station_data.get('code_postal', 1),
                        'name': station_data.get('name', 'Unknown'),
                        'lat': float(station_data.get('lat', 0)) if station_data.get('lat') else 0,
                        'lon': float(station_data.get('lon', 0)) if station_data.get('lon') else 0,
                        'capacity': station_data.get('capacity', 30)
                    })
                    
                    # Insérer le statut
                    insert_status = text("""
                        INSERT INTO velib_status (station_id, available_bikes, available_slots, timestamp)
                        VALUES (:station_id, :bikes, :slots, :timestamp)
                    """)
                    
                    conn.execute(insert_status, {
                        'station_id': station_data.get('code_postal', 1),
                        'bikes': station_data.get('available_bikes', 0),
                        'slots': station_data.get('available_ebikes', 0),
                        'timestamp': datetime.now()
                    })
                
                conn.commit()
                print("✅ Velib data inserted")
                return True
        except Exception as e:
            print(f"❌ Error inserting velib data: {e}")
            return False
    
    def fetch_and_insert_all(self):
        """Récupère et insère toutes les données"""
        print("🔄 Fetching and inserting data...")
        
        # Météo
        weather = fetch_weather_data()
        if weather:
            self.insert_weather(weather)
        
        # Vélib
        velib = fetch_velib_data()
        if velib:
            self.insert_velib(velib)
        
        print("✅ Data ingestion complete!")

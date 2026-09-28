from sqlalchemy import text
from datetime import datetime, timedelta
import pandas as pd

class ETLPipeline:
    """
    Pipeline ETL : Bronze → Silver → Gold
    """
    
    def __init__(self, db_handler):
        """
        Initialise le pipeline avec une connexion DB
        """
        self.db = db_handler
    
    # ===== BRONZE → SILVER =====
    
    def bronze_to_silver(self):
        """
        Transforme les données brutes (Bronze) en données nettoyées (Silver)
        """
        try:
            with self.db.engine.connect() as conn:
                # Requête pour combiner Vélib + Météo et nettoyer
                query = text("""
                    INSERT INTO velib_weather_silver 
                    (timestamp, station_id, station_name, latitude, longitude,
                     available_bikes, available_slots, capacity,
                     temperature, humidity, wind_speed, precipitation)
                    SELECT 
                        COALESCE(vs.timestamp, w.timestamp) as timestamp,
                        vs.station_id,
                        s.station_name,
                        s.latitude,
                        s.longitude,
                        COALESCE(vs.available_bikes, 0) as available_bikes,
                        COALESCE(vs.available_slots, 0) as available_slots,
                        s.capacity,
                        COALESCE(w.temperature, 0) as temperature,
                        COALESCE(w.humidity, 0) as humidity,
                        COALESCE(w.wind_speed, 0) as wind_speed,
                        COALESCE(w.precipitation, 0) as precipitation
                    FROM velib_status vs
                    FULL OUTER JOIN weather w 
                        ON DATE_TRUNC('hour', vs.timestamp) = DATE_TRUNC('hour', w.timestamp)
                    LEFT JOIN stations s ON vs.station_id = s.station_id
                    WHERE vs.timestamp > NOW() - INTERVAL '24 hours'
                    ON CONFLICT DO NOTHING
                """)
                conn.execute(query)
                conn.commit()
                print("✅ Bronze → Silver: Transformation completed")
                return True
        except Exception as e:
            print(f"❌ Bronze → Silver error: {e}")
            return False
    
    # ===== SILVER → GOLD (Hourly) =====
    
    def silver_to_gold_hourly(self):
        """
        Agrège les données Silver par heure
        """
        try:
            with self.db.engine.connect() as conn:
                query = text("""
                    INSERT INTO velib_weather_gold_hourly
                    (hour, avg_available_bikes, avg_humidity, avg_temperature,
                     avg_wind_speed, total_precipitation, station_count)
                    SELECT
                        DATE_TRUNC('hour', timestamp) as hour,
                        AVG(available_bikes) as avg_available_bikes,
                        AVG(humidity) as avg_humidity,
                        AVG(temperature) as avg_temperature,
                        AVG(wind_speed) as avg_wind_speed,
                        SUM(precipitation) as total_precipitation,
                        COUNT(DISTINCT station_id) as station_count
                    FROM velib_weather_silver
                    WHERE timestamp > NOW() - INTERVAL '24 hours'
                    GROUP BY DATE_TRUNC('hour', timestamp)
                    ON CONFLICT (hour) DO UPDATE SET
                        avg_available_bikes = EXCLUDED.avg_available_bikes,
                        avg_humidity = EXCLUDED.avg_humidity,
                        avg_temperature = EXCLUDED.avg_temperature,
                        avg_wind_speed = EXCLUDED.avg_wind_speed,
                        total_precipitation = EXCLUDED.total_precipitation,
                        station_count = EXCLUDED.station_count
                """)
                conn.execute(query)
                conn.commit()
                print("✅ Silver → Gold (Hourly): Aggregation completed")
                return True
        except Exception as e:
            print(f"❌ Silver → Gold (Hourly) error: {e}")
            return False
    
    # ===== SILVER → GOLD (Daily) =====
    
    def silver_to_gold_daily(self):
        """
        Agrège les données Silver par jour et station
        """
        try:
            with self.db.engine.connect() as conn:
                query = text("""
                    INSERT INTO velib_weather_gold_daily
                    (day, station_id, station_name, avg_available_bikes,
                     avg_humidity, avg_temperature, avg_wind_speed, total_precipitation)
                    SELECT
                        DATE(timestamp) as day,
                        station_id,
                        station_name,
                        AVG(available_bikes) as avg_available_bikes,
                        AVG(humidity) as avg_humidity,
                        AVG(temperature) as avg_temperature,
                        AVG(wind_speed) as avg_wind_speed,
                        SUM(precipitation) as total_precipitation
                    FROM velib_weather_silver
                    WHERE timestamp > NOW() - INTERVAL '7 days'
                    GROUP BY DATE(timestamp), station_id, station_name
                    ON CONFLICT (day, station_id) DO UPDATE SET
                        avg_available_bikes = EXCLUDED.avg_available_bikes,
                        avg_humidity = EXCLUDED.avg_humidity,
                        avg_temperature = EXCLUDED.avg_temperature,
                        avg_wind_speed = EXCLUDED.avg_wind_speed,
                        total_precipitation = EXCLUDED.total_precipitation
                """)
                conn.execute(query)
                conn.commit()
                print("✅ Silver → Gold (Daily): Aggregation completed")
                return True
        except Exception as e:
            print(f"❌ Silver → Gold (Daily) error: {e}")
            return False
    
    def run_full_pipeline(self):
        """
        Exécute le pipeline complet : Bronze → Silver → Gold
        """
        print("=" * 60)
        print("🔄 ETL PIPELINE")
        print("=" * 60)
        
        self.bronze_to_silver()
        self.silver_to_gold_hourly()
        self.silver_to_gold_daily()
        
        print("=" * 60)
        print("✅ Pipeline completed!")
        print("=" * 60)

from flask import Flask, render_template, jsonify
from db_handler import DatabaseHandler
from sqlalchemy import text
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialiser la base de données
db = DatabaseHandler()

@app.route('/')
def index():
    """Page d'accueil du Dashboard"""
    return render_template('index.html')

@app.route('/api/weather')
def get_weather():
    """API pour récupérer les données météo"""
    try:
        with db.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT timestamp, temperature, humidity, wind_speed, precipitation
                FROM weather
                ORDER BY timestamp DESC
                LIMIT 24
            """))
            data = [dict(row._mapping) for row in result]
            return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/velib-status')
def get_velib_status():
    """API pour récupérer le statut du Vélib"""
    try:
        with db.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT station_id, available_bikes, available_slots, timestamp
                FROM velib_status
                ORDER BY timestamp DESC
                LIMIT 24
            """))
            data = [dict(row._mapping) for row in result]
            return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """API pour récupérer les statistiques"""
    try:
        with db.engine.connect() as conn:
            # Statistiques météo
            weather_stats = conn.execute(text("""
                SELECT 
                    AVG(temperature) as avg_temp,
                    AVG(humidity) as avg_humidity,
                    AVG(wind_speed) as avg_wind
                FROM weather
                WHERE timestamp > NOW() - INTERVAL '24 hours'
            """)).fetchone()
            
            # Statistiques Vélib
            velib_stats = conn.execute(text("""
                SELECT 
                    COUNT(DISTINCT station_id) as total_stations,
                    AVG(available_bikes) as avg_bikes,
                    SUM(available_slots) as total_slots
                FROM velib_status
                WHERE timestamp > NOW() - INTERVAL '24 hours'
            """)).fetchone()
            
            return jsonify({
                'weather': dict(weather_stats._mapping) if weather_stats else {},
                'velib': dict(velib_stats._mapping) if velib_stats else {}
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

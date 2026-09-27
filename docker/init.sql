-- Création des tables pour le projet Vélib

-- Table 1: Stations Vélib
CREATE TABLE IF NOT EXISTS stations (
    station_id INT PRIMARY KEY,
    station_name VARCHAR(255) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    capacity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: Statut des stations (mises à jour régulières)
CREATE TABLE IF NOT EXISTS velib_status (
    id SERIAL PRIMARY KEY,
    station_id INT NOT NULL,
    available_bikes INT NOT NULL,
    available_slots INT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    FOREIGN KEY (station_id) REFERENCES stations(station_id)
);

-- Table 3: Données météo
CREATE TABLE IF NOT EXISTS weather (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL UNIQUE,
    temperature DECIMAL(5, 2) NOT NULL,
    humidity INT NOT NULL,
    wind_speed DECIMAL(5, 2) NOT NULL,
    precipitation DECIMAL(5, 2),
    weather_code INT
);

-- Table 4: Données agrégées (Bronze/Silver/Gold)
CREATE TABLE IF NOT EXISTS velib_weather_aggregated (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    station_id INT NOT NULL,
    available_bikes INT NOT NULL,
    temperature DECIMAL(5, 2) NOT NULL,
    humidity INT NOT NULL,
    wind_speed DECIMAL(5, 2) NOT NULL,
    precipitation DECIMAL(5, 2),
    FOREIGN KEY (station_id) REFERENCES stations(station_id)
);

-- Index pour optimiser les requêtes
CREATE INDEX idx_velib_status_timestamp ON velib_status(timestamp);
CREATE INDEX idx_weather_timestamp ON weather(timestamp);
CREATE INDEX idx_aggregated_timestamp ON velib_weather_aggregated(timestamp);

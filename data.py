import sqlite3
import random
import pandas as pd

# Connect to the database
conn = sqlite3.connect('farmers_data.db')
cursor = conn.cursor()

# Step 1: Create tables if they don't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS Soil (
    SoilID INTEGER PRIMARY KEY AUTOINCREMENT,
    SoilType TEXT,
    PH REAL,
    Nutrients TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Weather (
    WeatherID INTEGER PRIMARY KEY AUTOINCREMENT,
    Location TEXT,
    Temperature REAL,
    Humidity REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Crops (
    CropID INTEGER PRIMARY KEY,
    CropName TEXT,
    SoilType TEXT,
    Season TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Pests (
    PestID INTEGER PRIMARY KEY,
    CropAffected TEXT,
    PestName TEXT,
    ControlMeasures TEXT,
    SeverityLevel TEXT,
    PreventiveMeasures TEXT
)
""")

# Step 2: Generate synthetic data for Soil
soil_types = ["Loamy", "Clay", "Sandy", "Silty", "Peaty", "Chalky", "Saline"]
pH_levels = [5.5, 6.0, 6.5, 7.0, 7.5, 8.0]
nutrients = ["High", "Medium", "Low"]

soil_data = []
for i in range(1000):
    soil_type = random.choice(soil_types)
    ph = random.choice(pH_levels)
    nutrient = random.choice(nutrients)
    soil_data.append((soil_type, ph, nutrient))

# Insert soil data
cursor.executemany("""
INSERT INTO Soil (SoilType, PH, Nutrients) VALUES (?, ?, ?)
""", soil_data)

# Step 3: Generate synthetic data for Weather
locations = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore", "Hyderabad", "Pune", "Jaipur", "Lucknow", "Ahmedabad"]
temperatures = [random.uniform(20, 35) for _ in range(1000)]
humidities = [random.uniform(40, 80) for _ in range(1000)]

weather_data = []
for i in range(1000):
    location = random.choice(locations)
    temperature = temperatures[i]
    humidity = humidities[i]
    weather_data.append((location, temperature, humidity))

# Insert weather data
cursor.executemany("""
INSERT INTO Weather (Location, Temperature, Humidity) VALUES (?, ?, ?)
""", weather_data)

# Step 4: Generate synthetic data for Crops
crops_data = [
    (1, "Wheat", "Loamy", "Winter"),
    (2, "Rice", "Clay", "Rainy"),
    (3, "Maize", "Sandy", "Summer"),
    (4, "Sugarcane", "Silty", "Spring")
]

# Insert crops data
cursor.executemany("""
INSERT INTO Crops (CropID, CropName, SoilType, Season) VALUES (?, ?, ?, ?)
""", crops_data)

# Step 5: Generate pest control data
pests_data = [
    (1, "Wheat", "Wheat Aphids", "1. Spray neem-based insecticides\n2. Use ladybugs as natural predators\n3. Apply systemic insecticides if severe", "Medium", "1. Crop rotation\n2. Regular monitoring\n3. Maintain field hygiene"),
    (2, "Wheat", "Powdery Mildew", "1. Apply fungicides\n2. Increase air circulation\n3. Remove infected plants", "High", "1. Use resistant varieties\n2. Proper spacing\n3. Avoid overhead irrigation"),
    (3, "Rice", "Rice Blast", "1. Apply fungicides\n2. Adjust water management\n3. Remove infected plants", "High", "1. Use resistant varieties\n2. Balanced fertilization\n3. Proper water management"),
    (4, "Rice", "Stem Borers", "1. Use pheromone traps\n2. Apply appropriate insecticides\n3. Time insecticide application", "Medium", "1. Early planting\n2. Remove egg masses\n3. Regular monitoring"),
    (5, "Maize", "Fall Armyworm", "1. Apply biological controls\n2. Use recommended insecticides\n3. Early intervention", "High", "1. Early planting\n2. Regular scouting\n3. Natural enemy conservation"),
    (6, "Maize", "Corn Earworm", "1. Release beneficial insects\n2. Apply Bt-based products\n3. Time insecticide sprays", "Medium", "1. Plant resistant varieties\n2. Early planting\n3. Monitor adult moths"),
    (7, "Sugarcane", "Sugarcane Borers", "1. Release parasitoids\n2. Apply appropriate insecticides\n3. Remove dead hearts", "High", "1. Use clean planting material\n2. Regular monitoring\n3. Proper field sanitation"),
    (8, "Sugarcane", "Red Rot", "1. Remove infected plants\n2. Improve drainage\n3. Apply fungicides", "Medium", "1. Use disease-free setts\n2. Crop rotation\n3. Proper field drainage")
]

# Insert pest control data
cursor.executemany("""
INSERT INTO Pests (PestID, CropAffected, PestName, ControlMeasures, SeverityLevel, PreventiveMeasures) 
VALUES (?, ?, ?, ?, ?, ?)
""", pests_data)

# Commit changes
conn.commit()

# Verify the data
print("Data Samples:")
tables = ['Soil', 'Weather', 'Crops', 'Pests']
for table in tables:
    print(f"\n{table} Data Sample:")
    sample = pd.read_sql_query(f"SELECT * FROM {table} LIMIT 5", conn)
    print(sample)

# Close the connection
conn.close()

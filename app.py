import streamlit as st
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np

# Connect to the SQLite database
conn = sqlite3.connect('farmers_data.db')

# Step 1: Streamlit Sidebar for Navigation
st.sidebar.title("Farmers Database")
selection = st.sidebar.radio("Choose an option", ["Home", "Optimal Crops", "Soil Analysis", "Weather Patterns", "Weather Forecasting"])

# Step 2: Home page
if selection == "Home":
    st.title("Farmers Database Dashboard")
    st.write("""
    Welcome to the Farmers Database. Use the sidebar to explore different sections like optimal crops, pest control, 
    soil analysis, and weather patterns.
    """)

# Step 3: Optimal Crops based on soil and season
elif selection == "Optimal Crops":
    st.title("Find Optimal Crops")
    soil_type = st.selectbox("Select Soil Type", ["Loamy", "Clay", "Sandy", "Silty", "Peaty", "Chalky", "Saline"])
    season = st.selectbox("Select Season", ["Winter", "Rainy", "Summer", "Spring"])
    
    query = """
    SELECT CropName
    FROM Crops
    WHERE SoilType = ? AND Season = ?
    """
    crops = pd.read_sql_query(query, conn, params=(soil_type, season))
    
    if crops.empty:
        st.write(f"No optimal crops found for {soil_type} soil in {season}.")
    else:
        st.write(f"Optimal Crops for {soil_type} soil in {season}:")
        st.write(crops)

# Step 5: Soil Analysis
# Replace the existing Soil Analysis section with this code:

elif selection == "Soil Analysis":
    st.title("Soil Analysis")
    
    # Create realistic soil pH data
    np.random.seed(42)
    soil_data = {
        'SoilType': [
            'Loamy', 'Loamy', 'Loamy', 'Loamy', 'Loamy', 'Loamy', 'Loamy', 'Loamy',
            'Clay', 'Clay', 'Clay', 'Clay', 'Clay', 'Clay', 'Clay', 'Clay',
            'Sandy', 'Sandy', 'Sandy', 'Sandy', 'Sandy', 'Sandy', 'Sandy', 'Sandy',
            'Silty', 'Silty', 'Silty', 'Silty', 'Silty', 'Silty', 'Silty', 'Silty',
            'Peaty', 'Peaty', 'Peaty', 'Peaty', 'Peaty', 'Peaty', 'Peaty', 'Peaty',
            'Chalky', 'Chalky', 'Chalky', 'Chalky', 'Chalky', 'Chalky', 'Chalky', 'Chalky',
            'Saline', 'Saline', 'Saline', 'Saline', 'Saline', 'Saline', 'Saline', 'Saline'
        ],
        'PH': [
            # Loamy soil (balanced pH, typically 6.0-7.0)
            *np.random.normal(6.5, 0.3, 8),
            # Clay soil (slightly alkaline, typically 6.5-7.5)
            *np.random.normal(7.0, 0.3, 8),
            # Sandy soil (typically acidic, 5.5-6.5)
            *np.random.normal(6.0, 0.3, 8),
            # Silty soil (typically 6.0-7.0)
            *np.random.normal(6.5, 0.3, 8),
            # Peaty soil (acidic, typically 4.5-5.5)
            *np.random.normal(5.0, 0.3, 8),
            # Chalky soil (alkaline, typically 7.0-8.0)
            *np.random.normal(7.5, 0.3, 8),
            # Saline soil (typically 7.0-8.5)
            *np.random.normal(7.8, 0.3, 8)
        ]
    }
    
    df = pd.DataFrame(soil_data)
    
    # Create pH distribution plot
    st.subheader("Soil pH Distribution by Type")
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    sns.set_style("whitegrid")
    sns.set_palette("husl")
    
    # Create boxplot with swarm overlay
    sns.boxplot(x="SoilType", y="PH", data=df, ax=ax1)
    sns.swarmplot(x="SoilType", y="PH", data=df, color="0.25", alpha=0.5, ax=ax1)
    
    # Customize the plot
    plt.title("Soil pH Distribution by Soil Type", fontsize=14, pad=20)
    ax1.set_xlabel("Soil Type", fontsize=12)
    ax1.set_ylabel("pH Level", fontsize=12)
    plt.xticks(rotation=45)
    
    # Set y-axis limits to common pH range
    ax1.set_ylim(4, 9)
    
    # Add horizontal lines for common pH ranges
    ax1.axhline(y=7.0, color='gray', linestyle='--', alpha=0.3)  # Neutral pH
    ax1.axhline(y=6.0, color='gray', linestyle='--', alpha=0.3)  # Common lower bound
    ax1.axhline(y=8.0, color='gray', linestyle='--', alpha=0.3)  # Common upper bound
    
    # Adjust layout
    plt.tight_layout()
    
    # Display the plot in Streamlit
    st.pyplot(fig1)
    
    # Add some contextual information
    st.write("""
    ### pH Ranges for Different Soil Types:
    - Loamy Soil: Balanced pH (6.0-7.0), ideal for most crops
    - Clay Soil: Slightly alkaline (6.5-7.5), good for vegetables
    - Sandy Soil: Slightly acidic (5.5-6.5), suitable for acid-loving plants
    - Silty Soil: Balanced pH (6.0-7.0), good for most plants
    - Peaty Soil: Acidic (4.5-5.5), ideal for acid-loving plants
    - Chalky Soil: Alkaline (7.0-8.0), good for vegetables
    - Saline Soil: Alkaline (7.0-8.5), challenging for most crops
    """)

# Step 6: Weather Patterns Visualization
elif selection == "Weather Patterns":
    st.title("Weather Patterns")
    
    weather_data = pd.read_sql_query("""
        SELECT Location, Temperature, Humidity
        FROM Weather
    """, conn)
    
    if not weather_data.empty:
        # Temperature vs Humidity Scatter Plot
        st.subheader("Temperature vs Humidity by Location")
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.scatterplot(ax=ax1, x="Temperature", y="Humidity", data=weather_data, hue="Location", alpha=0.6)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig1)
        
        # Temperature Distribution by Location
        st.subheader("Temperature Distribution by Location")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.boxplot(ax=ax2, x="Location", y="Temperature", data=weather_data)
        plt.xticks(rotation=45)
        st.pyplot(fig2)
    else:
        st.write("No weather data available.")

# Step 7: Weather Forecasting using Linear Regression
elif selection == "Weather Forecasting":
    st.title("Weather Forecasting (Temperature vs Humidity)")
    
    weather_data = pd.read_sql_query("""
        SELECT Temperature, Humidity
        FROM Weather
        ORDER BY WeatherID DESC
        LIMIT 1000
    """, conn)
    
    X = weather_data[['Temperature']]
    y = weather_data['Humidity']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    future_temp = st.slider("Select Temperature (°C)", 
                           min_value=float(14),
                           max_value=float(50),
                           value=25.0,
                           step=0.1)
    
    predicted_humidity = model.predict([[future_temp]])[0]
    
    st.write(f"Predicted Humidity for {future_temp:.1f}°C: {predicted_humidity:.1f}%")
    
    # Show model performance
    r2_score = model.score(X_test, y_test)
    st.write(f"Model R² Score: {r2_score:.3f}")

# Close the database connection
conn.close()

"""
Main Streamlit application for the Greenhouse Intelligence System.
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
from datetime import datetime, timedelta

# Set up the page - MUST be the first Streamlit command
st.set_page_config(
    page_title="Greenhouse Intelligence System",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set custom theme with CSS
st.markdown("""
<style>
    /* Main background and text colors for dark theme */
    .stApp {
        background-color: #0a0a0a;
        color: #f0f0f0;
    }
    
    /* Header styling with animation */
    h1, h2, h3 {
        color: #4CAF50 !important;
        font-weight: 600 !important;
        text-shadow: 0 0 10px rgba(76, 175, 80, 0.3);
    }
    
    h1 {
        background: linear-gradient(90deg, #4CAF50, #2E7D32);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 3s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        0% { text-shadow: 0 0 10px rgba(76, 175, 80, 0.3); }
        100% { text-shadow: 0 0 20px rgba(76, 175, 80, 0.7); }
    }
    
    /* Sidebar styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: #121212;
        border-right: 1px solid #2E7D32;
    }
    
    /* Card/container styling with hover effect */
    div.stBlock {
        background-color: #121212;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #2E7D32;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    div.stBlock:hover {
        box-shadow: 0 8px 16px rgba(46, 125, 50, 0.3);
        transform: translateY(-2px);
    }
    
    /* Button styling with animation */
    .stButton>button {
        background: linear-gradient(90deg, #4CAF50, #2E7D32);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 8px 16px;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #2E7D32, #1B5E20);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(46, 125, 50, 0.4);
    }
    
    /* Metric styling with animation */
    div[data-testid="stMetric"] {
        background-color: #121212;
        border: 1px solid #2E7D32;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(46, 125, 50, 0.3);
    }
    
    div[data-testid="stMetric"] > div:first-child {
        color: #4CAF50 !important;
    }
    
    div[data-testid="stMetric"] > div:nth-child(2) {
        font-size: 1.8em !important;
        font-weight: 600 !important;
    }
    
    /* Map container styling */
    .map-container {
        border: 1px solid #2E7D32;
        border-radius: 10px;
        overflow: hidden;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        width: 100% !important;
        transition: all 0.3s ease;
    }
    
    .map-container:hover {
        box-shadow: 0 8px 16px rgba(46, 125, 50, 0.4);
    }
    
    /* Fix map alignment */
    .stFolium [style*="position: relative"] {
        width: 100% !important;
    }
    
    .stFolium iframe {
        width: 100% !important;
        left: 0 !important;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 20px;
        color: #999;
        font-size: 0.8em;
        border-top: 1px solid #2E7D32;
        margin-top: 30px;
        background-color: #0a0a0a;
    }
    
    /* Tab styling with animation */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #2E7D32;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #121212;
        border-radius: 8px 8px 0 0;
        padding: 10px 16px;
        border: 1px solid #2E7D32;
        border-bottom: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #1E1E1E;
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(180deg, #2E7D32, #1B5E20) !important;
        color: white !important;
        border: 1px solid #4CAF50 !important;
        border-bottom: none !important;
        box-shadow: 0 -4px 10px rgba(46, 125, 50, 0.3);
    }
    
    /* Fix expander styling */
    .streamlit-expanderHeader {
        background-color: #121212;
        border: 1px solid #2E7D32;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #1E1E1E;
    }
    
    .streamlit-expanderContent {
        background-color: #121212;
        border: 1px solid #2E7D32;
        border-top: none;
        border-radius: 0 0 5px 5px;
    }
    
    /* Table styling */
    div[data-testid="stDataFrame"] table {
        background-color: #121212;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #2E7D32;
    }
    
    div[data-testid="stDataFrame"] th {
        background-color: #1B5E20 !important;
        color: white !important;
        padding: 12px 15px !important;
        border-bottom: 2px solid #2E7D32;
    }
    
    div[data-testid="stDataFrame"] td {
        background-color: #121212 !important;
        color: #f0f0f0 !important;
        padding: 10px 15px !important;
        border-bottom: 1px solid #2E7D32;
        transition: all 0.2s ease;
    }
    
    div[data-testid="stDataFrame"] tr:hover td {
        background-color: #1E1E1E !important;
    }
    
    /* Success and error colors */
    .success-text {
        color: #4CAF50 !important;
        font-weight: 600;
    }
    
    .error-text {
        color: #F44336 !important;
        font-weight: 600;
    }
    
    /* Chart styling */
    .chart-container {
        background-color: #121212;
        border: 1px solid #2E7D32;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .chart-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(46, 125, 50, 0.4);
    }
    
    /* Progress bar styling */
    div[role="progressbar"] > div {
        background: linear-gradient(90deg, #4CAF50, #2E7D32) !important;
    }
    
    /* Alert styling */
    div[data-baseweb="notification"] {
        background-color: #121212 !important;
        border: 1px solid #2E7D32 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Select box styling */
    div[data-baseweb="select"] > div {
        background-color: #121212 !important;
        border: 1px solid #2E7D32 !important;
    }
    
    /* Slider styling */
    div[data-testid="stSlider"] > div > div {
        background-color: #2E7D32 !important;
    }
    
    div[data-testid="stSlider"] > div > div > div {
        background-color: #4CAF50 !important;
    }
    
    /* Status indicators */
    .status-on {
        background: linear-gradient(90deg, #4CAF50, #2E7D32);
        color: white;
        padding: 8px 16px;
        border-radius: 5px;
        display: inline-block;
        font-weight: 600;
        box-shadow: 0 2px 5px rgba(46, 125, 50, 0.4);
        animation: pulse 2s infinite;
    }
    
    .status-off {
        background: linear-gradient(90deg, #F44336, #C62828);
        color: white;
        padding: 8px 16px;
        border-radius: 5px;
        display: inline-block;
        font-weight: 600;
        box-shadow: 0 2px 5px rgba(198, 40, 40, 0.4);
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(76, 175, 80, 0); }
        100% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
    }
</style>
""", unsafe_allow_html=True)

# Add the project root to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.coordinator_agent import CoordinatorAgent
from config import DEFAULT_LATITUDE, DEFAULT_LONGITUDE, DEFAULT_RADIUS, CROP_TEMP_RANGES

# Initialize the coordinator agent
@st.cache_resource
def get_coordinator():
    return CoordinatorAgent()

coordinator = get_coordinator()

# Header
st.title("🌿 Greenhouse Intelligence System")
st.markdown("Powered by NASA Earth Data APIs and AI Agent Architecture")

# Sidebar for inputs
st.sidebar.header("Region Selection")

# Map for location selection
with st.sidebar.expander("Select Location on Map", expanded=True):
    # Default location (Bengaluru)
    if 'latitude' not in st.session_state:
        st.session_state.latitude = DEFAULT_LATITUDE
    if 'longitude' not in st.session_state:
        st.session_state.longitude = DEFAULT_LONGITUDE
    
    # Create a container div for better alignment
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    
    # Create a map centered at the default location
    m = folium.Map(
        location=[st.session_state.latitude, st.session_state.longitude], 
        zoom_start=10,
        tiles=None,  # Start with no tiles
        width='100%',
        height='100%'
    )
    
    # Add OpenStreetMap tile layer
    folium.TileLayer(
        tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        name='OpenStreetMap',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Add a marker for the selected location
    folium.Marker(
        [st.session_state.latitude, st.session_state.longitude],
        popup="Selected Location",
        tooltip="Selected Location",
        icon=folium.Icon(color="green")
    ).add_to(m)
    
    # Add circle to show radius
    folium.Circle(
        location=[st.session_state.latitude, st.session_state.longitude],
        radius=DEFAULT_RADIUS * 1000,  # Convert km to meters
        color="#4CAF50",
        fill=True,
        fill_opacity=0.2
    ).add_to(m)
    
    # Display the map with full width
    st_folium(m, width=None, height=300)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Manual coordinate input with better alignment
    st.markdown("#### Coordinates")
    col1, col2 = st.columns(2)
    with col1:
        latitude = st.number_input("Latitude", value=st.session_state.latitude, format="%.5f")
    with col2:
        longitude = st.number_input("Longitude", value=st.session_state.longitude, format="%.5f")
        
    # Update session state if values change
    if latitude != st.session_state.latitude or longitude != st.session_state.longitude:
        st.session_state.latitude = latitude
        st.session_state.longitude = longitude
        st.rerun()
        
    # Radius selection with better styling
    st.markdown("#### Area Settings")
    radius = st.slider("Radius (km)", min_value=1, max_value=50, value=DEFAULT_RADIUS)

# Crop selection with improved styling
st.sidebar.header("Crop Selection")
crop_options = list(CROP_TEMP_RANGES.keys())
selected_crop = st.sidebar.selectbox("Select Crop", crop_options)

# Display crop temperature range with better styling
min_temp, max_temp = CROP_TEMP_RANGES[selected_crop]
st.sidebar.markdown(f"""
<div style='background-color: #1E1E1E; padding: 10px; border-radius: 5px; border: 1px solid #333;'>
    <p style='margin: 0; color: #4CAF50;'><strong>Ideal Temperature Range</strong></p>
    <p style='margin: 0; font-size: 1.2em;'>{min_temp}°C – {max_temp}°C</p>
</div>
""", unsafe_allow_html=True)

# Data fetching with improved button
st.sidebar.header("Data")
days = st.sidebar.slider("Days of Historical Data", min_value=1, max_value=30, value=6)

fetch_button = st.sidebar.button("Fetch NASA Data", use_container_width=True)
if fetch_button:
    with st.spinner("Fetching data from NASA Earth Data APIs..."):
        result = coordinator.fetch_data(
            st.session_state.latitude,
            st.session_state.longitude,
            radius,
            days
        )
        
        if result['status'] == 'success':
            st.sidebar.success(result['message'])
            
            # Set the crop
            coordinator.set_crop(selected_crop)
            
            # Train the prediction model
            with st.spinner("Training prediction model..."):
                training_result = coordinator.train_prediction_model()
                if training_result['status'] == 'success':
                    st.sidebar.success("Prediction model trained successfully")
                else:
                    st.sidebar.error(training_result['message'])
        else:
            st.sidebar.error(result['message'])

# Main content area
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🔍 Analysis", "📈 History"])

# Dashboard tab
with tab1:
    st.header("Greenhouse Intelligence Dashboard")
    
    # Get recommendations if data is available
    if coordinator.current_data is not None and coordinator.current_crop is not None:
        recommendations = coordinator.get_recommendations()
        
        if recommendations['status'] in ['success', 'partial']:
            # Create columns for the dashboard with improved styling
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Current Conditions")
                
                # Create a container for current temperature with animation
                st.markdown(f"""
                <div class="chart-container" style="padding: 20px; text-align: center;">
                    <h4 style="margin-bottom: 15px;">Current Temperature</h4>
                    <div style="font-size: 3em; font-weight: 700; margin: 15px 0; 
                         background: linear-gradient(90deg, #4CAF50, #2E7D32); 
                         -webkit-background-clip: text; 
                         -webkit-text-fill-color: transparent;
                         animation: glow 3s ease-in-out infinite alternate;">
                        {recommendations['current_temperature']:.2f}°C
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Display soil moisture if available with a gauge visualization
                if recommendations['soil_moisture'] is not None:
                    moisture = recommendations['soil_moisture']
                    moisture_color = "#4CAF50" if moisture > 60 else "#FFC107" if moisture > 30 else "#F44336"
                    
                    st.markdown(f"""
                    <div class="chart-container" style="padding: 20px; text-align: center;">
                        <h4 style="margin-bottom: 15px;">Soil Moisture</h4>
                        <div style="font-size: 2.2em; font-weight: 700; margin: 15px 0; color: {moisture_color};">
                            {moisture:.1f}%
                        </div>
                        <div style="width: 100%; height: 20px; background-color: #333; border-radius: 10px; overflow: hidden; margin-top: 10px;">
                            <div style="height: 100%; width: {moisture}%; 
                                 background: linear-gradient(90deg, 
                                 {('#F44336' if moisture < 30 else '#FFC107' if moisture < 60 else '#4CAF50')}, 
                                 {('#C62828' if moisture < 30 else '#FFA000' if moisture < 60 else '#2E7D32')}); 
                                 border-radius: 10px; transition: width 1s ease-in-out;"></div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                            <span style="color: #F44336;">Dry</span>
                            <span style="color: #FFC107;">Moderate</span>
                            <span style="color: #4CAF50;">Optimal</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                # Display crop info with enhanced styling
                st.markdown(f"""
                <div class="chart-container" style="padding: 20px;">
                    <h4 style="margin-bottom: 15px; text-align: center;">Crop Information</h4>
                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <div style="width: 40px; height: 40px; border-radius: 50%; background-color: #4CAF50; 
                             display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                            <span style="color: white; font-size: 20px;">🌱</span>
                        </div>
                        <div>
                            <div style="color: #999; font-size: 0.9em;">Selected Crop</div>
                            <div style="font-size: 1.3em; font-weight: 600;">{recommendations['crop']}</div>
                        </div>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <div style="width: 40px; height: 40px; border-radius: 50%; background-color: #2196F3; 
                             display: flex; align-items: center; justify-content: center; margin-right: 15px;">
                            <span style="color: white; font-size: 20px;">📉</span>
                        </div>
                        <div>
                            <div style="color: #999; font-size: 0.9em;">Ideal Temperature Range</div>
                            <div style="font-size: 1.3em; font-weight: 600;">{recommendations['ideal_range']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Display feasibility with enhanced styling
                if 'feasibility' in recommendations:
                    feasibility = recommendations['feasibility']
                    icon = "✅" if feasibility == 'Ideal' else "⚠️" if feasibility in ['Above Ideal', 'Below Ideal'] else "❌"
                    color = "#4CAF50" if feasibility == 'Ideal' else "#FFC107" if feasibility in ['Above Ideal', 'Below Ideal'] else "#F44336"
                    
                    st.markdown(f"""
                    <div class="chart-container" style="padding: 20px; text-align: center;">
                        <h4 style="margin-bottom: 15px;">Growing Conditions</h4>
                        <div style="font-size: 1.8em; font-weight: 700; margin: 15px 0; color: {color};">
                            {icon} {feasibility}
                        </div>
                        <div style="color: #999; font-size: 0.9em;">
                            {
                            "Current temperature is within the ideal range for this crop." if feasibility == 'Ideal' else
                            "Temperature is higher than the ideal range for this crop." if feasibility == 'Above Ideal' else
                            "Temperature is lower than the ideal range for this crop." if feasibility == 'Below Ideal' else
                            "Current conditions are not suitable for this crop."
                            }
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.subheader("Recommendations")
                
                # Display predicted temperature with animation
                if 'predicted_temperature' in recommendations:
                    pred_temp = recommendations['predicted_temperature']
                    current_temp = recommendations['current_temperature']
                    temp_diff = pred_temp - current_temp
                    trend = "rising" if temp_diff > 0.5 else "falling" if temp_diff < -0.5 else "stable"
                    trend_icon = "↗️" if trend == "rising" else "↘️" if trend == "falling" else "➡️"
                    trend_color = "#F44336" if trend == "rising" else "#2196F3" if trend == "falling" else "#FFC107"
                    
                    st.markdown(f"""
                    <div class="chart-container" style="padding: 20px; text-align: center;">
                        <h4 style="margin-bottom: 15px;">Predicted Temperature (Next Day)</h4>
                        <div style="font-size: 3em; font-weight: 700; margin: 15px 0; 
                             background: linear-gradient(90deg, #2196F3, #1976D2); 
                             -webkit-background-clip: text; 
                             -webkit-text-fill-color: transparent;
                             animation: glow 3s ease-in-out infinite alternate;">
                            {pred_temp:.2f}°C
                        </div>
                        <div style="display: flex; align-items: center; justify-content: center; margin-top: 10px;">
                            <span style="margin-right: 10px;">Trend:</span>
                            <span style="color: {trend_color}; font-weight: 600;">
                                {trend_icon} {trend.capitalize()} ({temp_diff:+.2f}°C)
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Display actuator recommendations with animated status indicators
                actuators = recommendations['actuator_recommendations']
                
                st.markdown("""
                <div class="chart-container" style="padding: 20px;">
                    <h4 style="margin-bottom: 15px; text-align: center;">Actuator Control</h4>
                """, unsafe_allow_html=True)
                
                # Fan status
                st.markdown(f"""
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
                    <div style="display: flex; align-items: center;">
                        <div style="width: 40px; height: 40px; border-radius: 50%; 
                             background-color: {'#4CAF50' if actuators['fan'] == 'ON' else '#333'}; 
                             display: flex; align-items: center; justify-content: center; margin-right: 15px;
                             {'animation: pulse 2s infinite' if actuators['fan'] == 'ON' else ''}">
                            <span style="color: white; font-size: 20px;">💨</span>
                        </div>
                        <span style="font-size: 1.2em;">Fan</span>
                    </div>
                    <span class="{'status-on' if actuators['fan'] == 'ON' else 'status-off'}">{actuators['fan']}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Heater status
                st.markdown(f"""
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
                    <div style="display: flex; align-items: center;">
                        <div style="width: 40px; height: 40px; border-radius: 50%; 
                             background-color: {'#4CAF50' if actuators['heater'] == 'ON' else '#333'}; 
                             display: flex; align-items: center; justify-content: center; margin-right: 15px;
                             {'animation: pulse 2s infinite' if actuators['heater'] == 'ON' else ''}">
                            <span style="color: white; font-size: 20px;">🔥</span>
                        </div>
                        <span style="font-size: 1.2em;">Heater</span>
                    </div>
                    <span class="{'status-on' if actuators['heater'] == 'ON' else 'status-off'}">{actuators['heater']}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Water pump status
                st.markdown(f"""
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
                    <div style="display: flex; align-items: center;">
                        <div style="width: 40px; height: 40px; border-radius: 50%; 
                             background-color: {'#4CAF50' if actuators['water_pump'] == 'ON' else '#333'}; 
                             display: flex; align-items: center; justify-content: center; margin-right: 15px;
                             {'animation: pulse 2s infinite' if actuators['water_pump'] == 'ON' else ''}">
                            <span style="color: white; font-size: 20px;">💧</span>
                        </div>
                        <span style="font-size: 1.2em;">Water Pump</span>
                    </div>
                    <span class="{'status-on' if actuators['water_pump'] == 'ON' else 'status-off'}">{actuators['water_pump']}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Display reasoning
                st.markdown(f"""
                <div style="margin-top: 20px; padding: 15px; background-color: #1E1E1E; border-radius: 5px; border-left: 4px solid #4CAF50;">
                    <div style="color: #4CAF50; font-weight: 600; margin-bottom: 5px;">Reasoning:</div>
                    <div style="color: #ddd;">{actuators['reasoning']}</div>
                </div>
                </div>
                """, unsafe_allow_html=True)
                
            # Display temperature chart with improved styling
            st.subheader("Temperature History")
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(10, 5))
            plt.style.use('dark_background')
            
            # Set dark background
            fig.patch.set_facecolor('#121212')
            ax.set_facecolor('#121212')
            
            # Plot temperature data with improved styling
            data = coordinator.current_data
            
            # Add ideal range as a shaded area
            min_temp, max_temp = CROP_TEMP_RANGES[selected_crop]
            ax.axhspan(min_temp, max_temp, alpha=0.2, color='#4CAF50', label='Ideal Range')
            
            # Plot the temperature line with gradient color based on temperature
            cmap = plt.cm.RdYlGn_r
            norm = plt.Normalize(min_temp - 5, max_temp + 5)
            
            for i in range(len(data) - 1):
                ax.plot([data['date'].iloc[i], data['date'].iloc[i+1]], 
                       [data['temperature'].iloc[i], data['temperature'].iloc[i+1]], 
                       color=cmap(norm(data['temperature'].iloc[i])), 
                       linewidth=3)
            
            # Add scatter points
            scatter = ax.scatter(data['date'], data['temperature'], 
                               c=data['temperature'], cmap=cmap, norm=norm, 
                               s=100, zorder=5, edgecolor='white', linewidth=1)
            
            # Add labels and grid
            ax.set_xlabel('Date', color='#999')
            ax.set_ylabel('Temperature (°C)', color='#999')
            ax.set_title(f'Temperature History with Ideal Range for {selected_crop}', 
                        color='#4CAF50', fontsize=14, fontweight='bold')
            ax.grid(True, linestyle='--', alpha=0.3, color='#555')
            
            # Set tick colors
            ax.tick_params(colors='#999')
            for spine in ax.spines.values():
                spine.set_edgecolor('#555')
            
            # Add colorbar
            cbar = fig.colorbar(scatter, ax=ax)
            cbar.set_label('Temperature (°C)', color='#999')
            cbar.ax.yaxis.set_tick_params(color='#999')
            cbar.outline.set_edgecolor('#555')
            
            # Format x-axis dates
            fig.autofmt_xdate()
            
            # Add legend
            ax.legend(loc='upper right', framealpha=0.8, facecolor='#121212', edgecolor='#555')
            
            # Add value labels for the last point
            last_temp = data['temperature'].iloc[-1]
            last_date = data['date'].iloc[-1]
            ax.annotate(f'{last_temp:.2f}°C', 
                       xy=(last_date, last_temp),
                       xytext=(0, 10),
                       textcoords='offset points',
                       ha='center', va='bottom',
                       color='white', fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.3', fc='#4CAF50', alpha=0.7))
            
            fig.tight_layout()
            
            # Display the chart
            st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            st.warning(recommendations['message'])
    else:
        st.info("Please fetch data using the sidebar controls to view the dashboard.")

# Analysis tab
with tab2:
    st.header("Environmental Analysis")
    
    if coordinator.current_data is not None:
        # Get analysis results
        analysis = coordinator.analyze_conditions()
        
        if analysis['status'] == 'success':
            # Display temperature metrics
            st.subheader("Temperature Metrics")
            temp_metrics = analysis['temperature']
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Mean Temperature", f"{temp_metrics['mean']:.2f}°C")
            with col2:
                st.metric("Min Temperature", f"{temp_metrics['min']:.2f}°C")
            with col3:
                st.metric("Max Temperature", f"{temp_metrics['max']:.2f}°C")
            with col4:
                st.metric("Trend", temp_metrics['trend'].capitalize())
                
            # Display crop suitability
            st.subheader("Crop Suitability Analysis")
            
            # Create a DataFrame for the crop suitability data
            crop_data = []
            for crop, metrics in analysis['crop_suitability'].items():
                crop_data.append({
                    'Crop': crop,
                    'Status': metrics['status'],
                    'Score': metrics['score'],
                    'Deviation': metrics['deviation'],
                    'Ideal Range': metrics['ideal_range']
                })
                
            crop_df = pd.DataFrame(crop_data)
            
            # Sort by score (descending)
            crop_df = crop_df.sort_values('Score', ascending=False)
            
            # Display as a table
            st.dataframe(crop_df, use_container_width=True)
            
            # Create a bar chart of crop scores
            st.subheader("Crop Suitability Scores")
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # Create bars with color based on score
            bars = ax.bar(crop_df['Crop'], crop_df['Score'], color=plt.cm.RdYlGn(crop_df['Score']/100))
            
            # Add labels
            ax.set_xlabel('Crop')
            ax.set_ylabel('Suitability Score (0-100)')
            ax.set_ylim(0, 100)
            ax.grid(True, linestyle='--', alpha=0.7, axis='y')
            
            # Add value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                        f'{height:.0f}', ha='center', va='bottom')
                
            st.pyplot(fig)
            
            # Display soil moisture if available
            if analysis['soil_moisture'] is not None:
                st.subheader("Soil Moisture")
                st.metric("Current Soil Moisture", f"{analysis['soil_moisture']:.1f}%")
                
                # Create a gauge chart for soil moisture
                fig, ax = plt.subplots(figsize=(8, 4), subplot_kw={'projection': 'polar'})
                
                # Convert moisture percentage to radians (0-100% -> 0-π)
                moisture = analysis['soil_moisture']
                theta = np.pi * (moisture / 100)
                
                # Create the gauge
                ax.set_theta_zero_location("N")
                ax.set_theta_direction(-1)
                ax.set_rlim(0, 1)
                ax.set_thetamin(0)
                ax.set_thetamax(180)
                
                # Add colored regions
                ax.bar(np.linspace(0, np.pi/3, 50), [1]*50, width=np.pi/150, color=plt.cm.Reds_r(np.linspace(0.2, 0.8, 50)))
                ax.bar(np.linspace(np.pi/3, 2*np.pi/3, 50), [1]*50, width=np.pi/150, color=plt.cm.Greens(np.linspace(0.2, 0.8, 50)))
                ax.bar(np.linspace(2*np.pi/3, np.pi, 50), [1]*50, width=np.pi/150, color=plt.cm.Blues_r(np.linspace(0.2, 0.8, 50)))
                
                # Add the needle
                ax.plot([0, theta], [0, 0.8], color='black', linewidth=2)
                ax.scatter(theta, 0.8, color='black', s=50)
                
                # Remove unnecessary elements
                ax.set_yticklabels([])
                ax.set_xticklabels(['0%', '', '30%', '', '60%', '', '100%'])
                ax.spines['polar'].set_visible(False)
                
                # Add title
                ax.set_title('Soil Moisture Level', pad=15)
                
                st.pyplot(fig)
        else:
            st.warning(analysis['message'])
    else:
        st.info("Please fetch data using the sidebar controls to view the analysis.")

# History tab
with tab3:
    st.header("Historical Performance")
    
    # Get historical data
    history = coordinator.get_historical_performance()
    
    if history['status'] == 'success':
        # Display prediction accuracy
        st.subheader("Prediction Accuracy")
        
        if history['prediction_accuracy']['mae'] is not None:
            mae = history['prediction_accuracy']['mae']
            rmse = history['prediction_accuracy']['rmse']
            
            # Create a more visually appealing display for accuracy metrics
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                mae_color = "#4CAF50" if mae < 1.0 else "#FFC107" if mae < 2.0 else "#F44336"
                st.markdown(f"""
                <div style="text-align: center; padding: 10px;">
                    <div style="color: #999; font-size: 1.1em;">Mean Absolute Error</div>
                    <div style="font-size: 2.2em; font-weight: 700; margin: 10px 0; color: {mae_color};">
                        {mae:.2f}°C
                    </div>
                    <div style="font-size: 0.9em; color: #777;">
                        {
                        "Excellent accuracy" if mae < 1.0 else
                        "Good accuracy" if mae < 2.0 else
                        "Fair accuracy" if mae < 3.0 else
                        "Poor accuracy"
                        }
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                rmse_color = "#4CAF50" if rmse < 1.5 else "#FFC107" if rmse < 2.5 else "#F44336"
                st.markdown(f"""
                <div style="text-align: center; padding: 10px;">
                    <div style="color: #999; font-size: 1.1em;">Root Mean Square Error</div>
                    <div style="font-size: 2.2em; font-weight: 700; margin: 10px 0; color: {rmse_color};">
                        {rmse:.2f}°C
                    </div>
                    <div style="font-size: 0.9em; color: #777;">
                        {
                        "Excellent precision" if rmse < 1.5 else
                        "Good precision" if rmse < 2.5 else
                        "Fair precision" if rmse < 3.5 else
                        "Poor precision"
                        }
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Create a visualization for error trends if we have prediction data
            if len(history['recent_predictions']) > 1:
                # Extract data for visualization
                pred_data = []
                for pred in history['recent_predictions']:
                    if pred['actual_temp'] is not None:
                        pred_data.append({
                            'date': pred['date'],
                            'predicted': pred['predicted_temp'],
                            'actual': pred['actual_temp'],
                            'error': abs(pred['predicted_temp'] - pred['actual_temp'])
                        })
                
                if pred_data:
                    error_df = pd.DataFrame(pred_data)
                    
                    # Create error trend chart
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.subheader("Prediction Error Trend")
                    
                    fig, ax = plt.subplots(figsize=(10, 5))
                    plt.style.use('dark_background')
                    
                    # Set dark background
                    fig.patch.set_facecolor('#121212')
                    ax.set_facecolor('#121212')
                    
                    # Plot error trend
                    ax.bar(range(len(error_df)), error_df['error'], color='#F44336', alpha=0.7)
                    ax.plot(range(len(error_df)), error_df['error'], marker='o', color='#FF7043', linewidth=2)
                    
                    # Add labels and grid
                    ax.set_xlabel('Prediction Index', color='#999')
                    ax.set_ylabel('Absolute Error (°C)', color='#999')
                    ax.set_title('Prediction Error Trend', color='#4CAF50', fontsize=14, fontweight='bold')
                    ax.grid(True, linestyle='--', alpha=0.3, color='#555')
                    
                    # Set tick colors
                    ax.tick_params(colors='#999')
                    for spine in ax.spines.values():
                        spine.set_edgecolor('#555')
                    
                    # Add a horizontal line for average error
                    avg_error = error_df['error'].mean()
                    ax.axhline(y=avg_error, color='#4CAF50', linestyle='--', alpha=0.8)
                    ax.text(len(error_df) * 0.02, avg_error * 1.1, f'Avg Error: {avg_error:.2f}°C', 
                            color='#4CAF50', fontweight='bold')
                    
                    st.pyplot(fig)
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="chart-container" style="text-align: center; padding: 20px;">
                <div style="font-size: 1.2em; margin-bottom: 10px;">No prediction accuracy data available yet</div>
                <div style="color: #777; font-size: 0.9em;">
                    The system needs more predictions with actual temperature measurements to calculate accuracy metrics.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Display recent predictions
        st.subheader("Recent Predictions")
        
        if history['recent_predictions']:
            # Create a DataFrame for recent predictions
            pred_data = []
            for pred in history['recent_predictions']:
                pred_data.append({
                    'Date': pred['date'],
                    'Crop': pred['crop'],
                    'Predicted Temperature': pred['predicted_temp'],
                    'Actual Temperature': pred['actual_temp'] if pred['actual_temp'] is not None else 'N/A'
                })
                
            pred_df = pd.DataFrame(pred_data)
            
            # Display as a table with improved styling
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.dataframe(pred_df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Show last date temperature with animation
            if not pred_df.empty and pred_df['Actual Temperature'].iloc[-1] != 'N/A':
                last_date = pred_df['Date'].iloc[-1]
                last_temp = pred_df['Actual Temperature'].iloc[-1]
                last_crop = pred_df['Crop'].iloc[-1]
                
                st.markdown(f"""
                <div class="chart-container" style="padding: 20px; text-align: center;">
                    <h4>Last Recorded Temperature</h4>
                    <div style="font-size: 2.5em; font-weight: 700; margin: 15px 0; 
                         background: linear-gradient(90deg, #4CAF50, #2E7D32); 
                         -webkit-background-clip: text; 
                         -webkit-text-fill-color: transparent;
                         animation: glow 3s ease-in-out infinite alternate;">
                        {last_temp:.2f}°C
                    </div>
                    <div>Date: {last_date} | Crop: {last_crop}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Create a visual comparison between predicted and actual
                if pred_df['Predicted Temperature'].iloc[-1] != 'N/A':
                    pred_temp = pred_df['Predicted Temperature'].iloc[-1]
                    diff = last_temp - pred_temp
                    accuracy = 100 - min(abs(diff) * 10, 100)  # Simple accuracy calculation
                    
                    st.markdown(f"""
                    <div class="chart-container" style="padding: 20px;">
                        <h4>Prediction vs Actual</h4>
                        <div style="display: flex; align-items: center; justify-content: space-between; margin: 15px 0;">
                            <div>
                                <div style="color: #2196F3; font-weight: 600;">Predicted</div>
                                <div style="font-size: 1.8em;">{pred_temp:.2f}°C</div>
                            </div>
                            <div style="font-size: 2em; color: #555;">vs</div>
                            <div>
                                <div style="color: #4CAF50; font-weight: 600;">Actual</div>
                                <div style="font-size: 1.8em;">{last_temp:.2f}°C</div>
                            </div>
                        </div>
                        <div style="margin-top: 15px;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                                <span>Accuracy</span>
                                <span>{accuracy:.1f}%</span>
                            </div>
                            <div style="height: 10px; background-color: #333; border-radius: 5px; overflow: hidden;">
                                <div style="height: 100%; width: {accuracy}%; 
                                     background: linear-gradient(90deg, {'#F44336' if accuracy < 70 else '#FFC107' if accuracy < 90 else '#4CAF50'}, 
                                     {'#C62828' if accuracy < 70 else '#FFA000' if accuracy < 90 else '#2E7D32'}); 
                                     border-radius: 5px;"></div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add temperature comparison chart
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.subheader("Temperature Prediction vs Actual")
                    
                    # Create a comparison chart for the last few predictions
                    if len(pred_df) > 1:
                        # Get the last 7 entries or all if less than 7
                        display_df = pred_df.tail(7).copy()
                        display_df['Actual'] = pd.to_numeric(display_df['Actual Temperature'], errors='coerce')
                        display_df['Predicted'] = pd.to_numeric(display_df['Predicted Temperature'], errors='coerce')
                        
                        # Only keep rows where both actual and predicted are numbers
                        display_df = display_df.dropna(subset=['Actual', 'Predicted'])
                        
                        if not display_df.empty:
                            fig, ax = plt.subplots(figsize=(10, 5))
                            plt.style.use('dark_background')
                            
                            # Set dark background
                            fig.patch.set_facecolor('#121212')
                            ax.set_facecolor('#121212')
                            
                            # Plot actual and predicted temperatures
                            ax.plot(range(len(display_df)), display_df['Actual'], 'o-', color='#4CAF50', linewidth=3, label='Actual')
                            ax.plot(range(len(display_df)), display_df['Predicted'], 'o--', color='#2196F3', linewidth=2, label='Predicted')
                            
                            # Fill the area between the lines
                            ax.fill_between(range(len(display_df)), display_df['Actual'], display_df['Predicted'], 
                                          color='#F44336', alpha=0.2, label='Difference')
                            
                            # Add labels and grid
                            ax.set_xlabel('Date', color='#999')
                            ax.set_ylabel('Temperature (°C)', color='#999')
                            ax.set_title('Prediction vs Actual Temperature', color='#4CAF50', fontsize=14, fontweight='bold')
                            ax.grid(True, linestyle='--', alpha=0.3, color='#555')
                            
                            # Set tick colors
                            ax.tick_params(colors='#999')
                            for spine in ax.spines.values():
                                spine.set_edgecolor('#555')
                            
                            # Use date labels on x-axis
                            ax.set_xticks(range(len(display_df)))
                            ax.set_xticklabels(display_df['Date'], rotation=45)
                            
                            # Add legend
                            ax.legend(loc='upper right', framealpha=0.8, facecolor='#121212', edgecolor='#555')
                            
                            # Add value labels
                            for i, (actual, pred) in enumerate(zip(display_df['Actual'], display_df['Predicted'])):
                                ax.text(i, actual + 0.2, f'{actual:.1f}°C', ha='center', va='bottom', 
                                       color='#4CAF50', fontweight='bold', fontsize=9)
                                ax.text(i, pred - 0.2, f'{pred:.1f}°C', ha='center', va='top', 
                                       color='#2196F3', fontweight='bold', fontsize=9)
                            
                            fig.tight_layout()
                            st.pyplot(fig)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="chart-container" style="text-align: center; padding: 20px;">
                <div style="font-size: 1.2em; margin-bottom: 10px;">No prediction history available yet</div>
                <div style="color: #777; font-size: 0.9em;">
                    Prediction data will appear here once the system has made temperature predictions.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        # Display crop history
        st.subheader("Crop Performance History")
        
        if any(history['crop_history'].values()):
            # Create tabs for each crop
            crop_tabs = st.tabs(list(history['crop_history'].keys()))
            
            for i, crop in enumerate(history['crop_history'].keys()):
                with crop_tabs[i]:
                    crop_data = history['crop_history'][crop]
                    
                    if crop_data:
                        # Create a DataFrame for the crop history
                        df = pd.DataFrame(crop_data)
                        df['date'] = pd.to_datetime(df['date'])
                        
                        # Create a line chart with improved styling
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        
                        fig, ax = plt.subplots(figsize=(10, 5))
                        plt.style.use('dark_background')
                        
                        # Set dark background
                        fig.patch.set_facecolor('#121212')
                        ax.set_facecolor('#121212')
                        
                        # Plot performance score with gradient color based on score
                        cmap = plt.cm.RdYlGn
                        norm = plt.Normalize(0, 100)
                        
                        for i in range(len(df) - 1):
                            ax.plot([i, i+1], [df['score'].iloc[i], df['score'].iloc[i+1]], 
                                   color=cmap(norm(df['score'].iloc[i])), 
                                   linewidth=3)
                        
                        # Add scatter points
                        scatter = ax.scatter(range(len(df)), df['score'], 
                                           c=df['score'], cmap=cmap, norm=norm, 
                                           s=100, zorder=5, edgecolor='white', linewidth=1)
                        
                        # Add labels and grid
                        ax.set_xlabel('Date', color='#999')
                        ax.set_ylabel('Performance Score', color='#999')
                        ax.set_title(f'{crop} Performance History', color='#4CAF50', fontsize=14, fontweight='bold')
                        ax.grid(True, linestyle='--', alpha=0.3, color='#555')
                        
                        # Set tick colors
                        ax.tick_params(colors='#999')
                        for spine in ax.spines.values():
                            spine.set_edgecolor('#555')
                        
                        # Set y-axis range
                        ax.set_ylim(0, 105)
                        
                        # Add colorbar
                        cbar = fig.colorbar(scatter, ax=ax)
                        cbar.set_label('Performance Score', color='#999')
                        cbar.ax.yaxis.set_tick_params(color='#999')
                        cbar.outline.set_edgecolor('#555')
                        
                        # Add performance zones
                        ax.axhspan(0, 40, alpha=0.1, color='#F44336', label='Poor')
                        ax.axhspan(40, 70, alpha=0.1, color='#FFC107', label='Average')
                        ax.axhspan(70, 100, alpha=0.1, color='#4CAF50', label='Good')
                        
                        # Add legend
                        ax.legend(loc='lower right', framealpha=0.8, facecolor='#121212', edgecolor='#555')
                        
                        # Use date labels on x-axis
                        ax.set_xticks(range(len(df)))
                        ax.set_xticklabels([d.strftime('%m/%d') for d in df['date']], rotation=45)
                        
                        # Add value labels
                        for i, score in enumerate(df['score']):
                            ax.text(i, score + 3, f'{score:.0f}', ha='center', va='bottom', 
                                   color='white', fontweight='bold')
                        
                        fig.tight_layout()
                        st.pyplot(fig)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Add summary statistics
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            avg_score = df['score'].mean()
                            avg_color = "#4CAF50" if avg_score >= 70 else "#FFC107" if avg_score >= 40 else "#F44336"
                            st.markdown(f"""
                            <div style="text-align: center; padding: 10px;">
                                <div style="color: #999; font-size: 1.1em;">Average Score</div>
                                <div style="font-size: 2.2em; font-weight: 700; margin: 10px 0; color: {avg_color};">
                                    {avg_score:.1f}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                        with col2:
                            max_score = df['score'].max()
                            max_color = "#4CAF50" if max_score >= 70 else "#FFC107" if max_score >= 40 else "#F44336"
                            st.markdown(f"""
                            <div style="text-align: center; padding: 10px;">
                                <div style="color: #999; font-size: 1.1em;">Best Score</div>
                                <div style="font-size: 2.2em; font-weight: 700; margin: 10px 0; color: {max_color};">
                                    {max_score:.1f}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                        with col3:
                            trend = "Improving" if df['score'].iloc[-1] > df['score'].iloc[0] else "Declining" if df['score'].iloc[-1] < df['score'].iloc[0] else "Stable"
                            trend_color = "#4CAF50" if trend == "Improving" else "#F44336" if trend == "Declining" else "#FFC107"
                            st.markdown(f"""
                            <div style="text-align: center; padding: 10px;">
                                <div style="color: #999; font-size: 1.1em;">Performance Trend</div>
                                <div style="font-size: 2.2em; font-weight: 700; margin: 10px 0; color: {trend_color};">
                                    {trend}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="chart-container" style="text-align: center; padding: 20px;">
                            <div style="font-size: 1.2em; margin-bottom: 10px;">No history available for {crop} yet</div>
                            <div style="color: #777; font-size: 0.9em;">
                                Performance data will appear here once the system has collected enough information.
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="chart-container" style="text-align: center; padding: 20px;">
                <div style="font-size: 1.2em; margin-bottom: 10px;">No crop performance history available yet</div>
                <div style="color: #777; font-size: 0.9em;">
                    Performance data will be displayed here after the system has collected crop performance metrics.
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No historical data available yet.")

# Footer
st.markdown("<div class='footer'>", unsafe_allow_html=True)
st.markdown("Powered by codexcherry")
st.markdown("© 2025 Greenhouse Intelligence System")
st.markdown("</div>", unsafe_allow_html=True) 
# 🌿 Greenhouse Intelligence System

A smart greenhouse monitoring and recommendation system powered by NASA Earth data APIs and AI agents, featuring a premium dark-themed UI with interactive visualizations.

## Features

- 🌍 Geographic region selection via interactive OpenStreetMap
- 🛰️ NASA POWER API integration for real-time environmental monitoring
- 🌱 Crop suitability analysis with visual scoring
- 🧠 AI-powered temperature prediction with accuracy metrics
- 🤖 Multi-agent system for intelligent recommendations
- 📊 Interactive data visualizations with animations
- 📱 Responsive premium dark-themed UI
- 📈 Historical performance tracking and analysis
- 🌡️ Last recorded temperature display and trend analysis

## Dashboard Features

- **Current Conditions**: Real-time temperature and soil moisture monitoring with animated gauges
- **Recommendations**: Smart actuator controls with visual indicators and reasoning
- **Temperature History**: Interactive temperature charts with ideal range visualization
- **Prediction Accuracy**: Visual error tracking and performance metrics
- **Crop Performance**: Historical performance tracking with trend analysis

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up NASA API access:
   
   a. Create a `.env` file with your NASA API key (optional, as the POWER API doesn't require authentication for most uses):
   ```
   NASA_API_KEY=your_api_key
   ```
   
   Note: The application uses NASA's POWER API which provides open access to climate and weather data without requiring authentication.
4. Run the application:
   ```
   python run.py
   ```
   or
   ```
   streamlit run app/main.py
   ```

## Project Structure

- `app/`: Streamlit application files
- `data/`: Data storage and processing modules
- `models/`: ML models for prediction
- `agents/`: AI agent system components
- `utils/`: Helper functions and utilities

## Supported Crops

- 🥬 Lettuce (Ideal: 16–20°C)
- 🍅 Tomato (Ideal: 21–27°C)
- 🫑 Bell Pepper (Ideal: 18–24°C)
- 🥒 Cucumber (Ideal: 18–25°C)
- 🌱 Spinach (Ideal: 10–20°C)

## UI Features

- **Dark Theme**: Premium dark-themed UI with green and red accents
- **Animations**: Animated elements for temperature displays, status indicators, and more
- **Interactive Charts**: Responsive charts with hover effects and color gradients
- **Status Indicators**: Visual status indicators for actuators with pulse animations
- **Card Containers**: Stylized containers with hover effects and transitions


## Developed by

Powered by codexcherry © 2025
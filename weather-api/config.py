"""Weather Dashboard Configuration

Configuration for weather API services, caching, and UI settings.
"""

import os
from typing import Dict, Optional

# Weather API Providers
WEATHER_PROVIDERS = {
    'openweathermap': {
        'base_url': 'https://api.openweathermap.org/data/2.5',
        'free_tier': True,
        'requires_key': True,
        'rate_limit': 60,  # requests per minute
    },
    'weatherapi': {
        'base_url': 'https://api.weatherapi.com/v1',
        'free_tier': True,
        'requires_key': True,
        'rate_limit': 1000,  # requests per day
    },
    'openmeteo': {
        'base_url': 'https://api.open-meteo.com/v1',
        'free_tier': True,
        'requires_key': False,
        'rate_limit': 10000,  # requests per day
    },
    'tomorrow': {
        'base_url': 'https://api.tomorrow.io/v4/timelines',
        'free_tier': False,
        'requires_key': True,
        'rate_limit': 500,  # requests per day free tier
    },
}

# API Keys (from environment)
API_KEYS = {
    'openweathermap': os.getenv('OPENWEATHERMAP_API_KEY', ''),
    'weatherapi': os.getenv('WEATHERAPI_KEY', ''),
    'tomorrow': os.getenv('TOMORROW_IO_API_KEY', ''),
}

# Default Configuration
DEFAULT_CONFIG = {
    'provider': 'openmeteo',  # Use Open-Meteo as default (no API key required)
    'units': 'metric',  # 'metric' or 'imperial'
    'language': 'en',
    'cache_duration': 600,  # seconds (10 minutes)
    'update_interval': 300,  # seconds (5 minutes) for real-time updates
    'timeout': 10,  # seconds
    'retries': 3,
    'retry_delay': 2,  # seconds
}

# Location Presets
PREFERRED_LOCATIONS = [
    {'name': 'Dubai', 'lat': 25.2048, 'lon': 55.2708, 'country': 'AE'},
    {'name': 'New York', 'lat': 40.7128, 'lon': -74.0060, 'country': 'US'},
    {'name': 'London', 'lat': 51.5074, 'lon': -0.1278, 'country': 'UK'},
    {'name': 'Tokyo', 'lat': 35.6762, 'lon': 139.6503, 'country': 'JP'},
    {'name': 'Sydney', 'lat': -33.8688, 'lon': 151.2093, 'country': 'AU'},
    {'name': 'Singapore', 'lat': 1.3521, 'lon': 103.8198, 'country': 'SG'},
]

# Weather Condition Icons/Emojis
WEATHER_ICONS = {
    'clear': '☀️',
    'sunny': '☀️',
    'cloudy': '☁️',
    'overcast': '☁️',
    'rainy': '🌧️',
    'rain': '🌧️',
    'thunderstorm': '⛈️',
    'snow': '❄️',
    'sleet': '🌨️',
    'windy': '💨',
    'foggy': '🌫️',
    'partly_cloudy': '⛅',
    'drizzle': '🌦️',
    'hail': '🧊',
}

# UI Theme
UI_CONFIG = {
    'theme': 'dark',  # 'dark' or 'light'
    'accent_color': '#00d4ff',  # Cyan
    'primary_color': '#1a1a2e',  # Dark blue
    'warning_color': '#ff6b6b',  # Red
    'success_color': '#51cf66',  # Green
    'font_family': 'Arial, sans-serif',
    'refresh_interval': 60,  # seconds
}

# Alert Thresholds
ALERT_THRESHOLDS = {
    'extreme_heat': 40,  # Celsius
    'extreme_cold': -10,  # Celsius
    'high_uv': 11,  # UV Index
    'low_visibility': 1000,  # meters
    'high_wind': 40,  # km/h
    'heavy_rain': 50,  # mm
    'air_quality_poor': 200,  # AQI
}

# Pollution Level Colors
POLLUTION_COLORS = {
    'good': '#51cf66',  # Green
    'fair': '#ffd43b',  # Yellow
    'moderate': '#ff922b',  # Orange
    'poor': '#ff6b6b',  # Red
    'very_poor': '#9c36b5',  # Purple
}

# UV Index Colors
UV_INDEX_COLORS = {
    'low': '#51cf66',
    'moderate': '#ffd43b',
    'high': '#ff922b',
    'very_high': '#ff6b6b',
    'extreme': '#9c36b5',
}

def get_weather_icon(condition: str) -> str:
    """Get emoji icon for weather condition"""
    condition_lower = condition.lower().replace(' ', '_')
    for key, icon in WEATHER_ICONS.items():
        if key in condition_lower:
            return icon
    return '🌤️'  # Default

def get_uv_color(uv_index: float) -> str:
    """Get color for UV index"""
    if uv_index <= 2:
        return UV_INDEX_COLORS['low']
    elif uv_index <= 5:
        return UV_INDEX_COLORS['moderate']
    elif uv_index <= 7:
        return UV_INDEX_COLORS['high']
    elif uv_index <= 10:
        return UV_INDEX_COLORS['very_high']
    else:
        return UV_INDEX_COLORS['extreme']

def get_pollution_color(aqi: float) -> str:
    """Get color for air quality index"""
    if aqi <= 50:
        return POLLUTION_COLORS['good']
    elif aqi <= 100:
        return POLLUTION_COLORS['fair']
    elif aqi <= 150:
        return POLLUTION_COLORS['moderate']
    elif aqi <= 200:
        return POLLUTION_COLORS['poor']
    else:
        return POLLUTION_COLORS['very_poor']

"""Weather Alerts System

Monitors weather conditions and generates alerts based on configured thresholds.
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from config import ALERT_THRESHOLDS
from weather_service import CurrentWeather, DailyForecast, AirQuality

logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = 'info'
    WARNING = 'warning'
    CRITICAL = 'critical'

@dataclass
class WeatherAlert:
    """Weather alert data"""
    type: str
    severity: AlertSeverity
    message: str
    location: str
    timestamp: str
    icon: str
    affected_period: Optional[str] = None

class WeatherAlertSystem:
    """System for generating weather alerts"""
    
    def __init__(self):
        self.logger = logger
        self.active_alerts = []
    
    def check_current_weather_alerts(self, weather: CurrentWeather, 
                                    location_name: str) -> List[WeatherAlert]:
        """Check current weather for alert conditions"""
        alerts = []
        
        # Temperature alerts
        if weather.temperature > ALERT_THRESHOLDS['extreme_heat']:
            alerts.append(WeatherAlert(
                type='extreme_heat',
                severity=AlertSeverity.CRITICAL,
                message=f"🔥 Extreme heat alert: {weather.temperature}°C - Stay hydrated and avoid prolonged sun exposure",
                location=location_name,
                timestamp=datetime.now().isoformat(),
                icon='🔥'
            ))
        
        if weather.temperature < ALERT_THRESHOLDS['extreme_cold']:
            alerts.append(WeatherAlert(
                type='extreme_cold',
                severity=AlertSeverity.CRITICAL,
                message=f"❄️ Extreme cold alert: {weather.temperature}°C - Dress warmly and limit outdoor time",
                location=location_name,
                timestamp=datetime.now().isoformat(),
                icon='❄️'
            ))
        
        # Wind alerts
        if weather.wind_speed > ALERT_THRESHOLDS['high_wind']:
            alerts.append(WeatherAlert(
                type='high_wind',
                severity=AlertSeverity.WARNING,
                message=f"💨 High wind alert: {weather.wind_speed} km/h - Exercise caution outdoors",
                location=location_name,
                timestamp=datetime.now().isoformat(),
                icon='💨'
            ))
        
        # Visibility alerts
        if weather.visibility < ALERT_THRESHOLDS['low_visibility'] / 1000:
            alerts.append(WeatherAlert(
                type='low_visibility',
                severity=AlertSeverity.WARNING,
                message=f"🌫️ Low visibility: {weather.visibility} km - Drive carefully",
                location=location_name,
                timestamp=datetime.now().isoformat(),
                icon='🌫️'
            ))
        
        # Precipitation alerts
        if weather.precipitation > ALERT_THRESHOLDS['heavy_rain']:
            alerts.append(WeatherAlert(
                type='heavy_rain',
                severity=AlertSeverity.WARNING,
                message=f"🌧️ Heavy rain alert: {weather.precipitation} mm - Flooding possible",
                location=location_name,
                timestamp=datetime.now().isoformat(),
                icon='🌧️'
            ))
        
        # UV Index alerts
        if weather.uv_index and weather.uv_index > ALERT_THRESHOLDS['high_uv']:
            alerts.append(WeatherAlert(
                type='high_uv',
                severity=AlertSeverity.WARNING,
                message=f"☀️ High UV Index: {weather.uv_index} - Use sunscreen",
                location=location_name,
                timestamp=datetime.now().isoformat(),
                icon='☀️'
            ))
        
        # Humidity comfort alert
        if weather.humidity > 80 and weather.temperature > 25:
            alerts.append(WeatherAlert(
                type='high_humidity',
                severity=AlertSeverity.INFO,
                message=f"💧 High humidity: {weather.humidity}% - May feel uncomfortably muggy",
                location=location_name,
                timestamp=datetime.now().isoformat(),
                icon='💧'
            ))
        
        return alerts
    
    def check_forecast_alerts(self, forecast: DailyForecast,
                             location_name: str,
                             days_ahead: int = 0) -> List[WeatherAlert]:
        """Check forecast for alert conditions"""
        alerts = []
        
        # Temperature forecast alerts
        if forecast.temp_high > ALERT_THRESHOLDS['extreme_heat']:
            period = f"in {days_ahead} days" if days_ahead > 0 else "tomorrow"
            alerts.append(WeatherAlert(
                type='forecast_extreme_heat',
                severity=AlertSeverity.WARNING if days_ahead > 0 else AlertSeverity.CRITICAL,
                message=f"🔥 Extreme heat forecast {period}: {forecast.temp_high}°C",
                location=location_name,
                timestamp=datetime.now().isoformat(),
                icon='🔥',
                affected_period=forecast.date
            ))
        
        if forecast.temp_low < ALERT_THRESHOLDS['extreme_cold']:
            period = f"in {days_ahead} days" if days_ahead > 0 else "tomorrow"
            alerts.append(WeatherAlert(
                type='forecast_extreme_cold',
                severity=AlertSeverity.WARNING if days_ahead > 0 else AlertSeverity.CRITICAL,
                message=f"❄️ Extreme cold forecast {period}: {forecast.temp_low}°C",
                location=location_name,
                timestamp=datetime.now().isoformat(),
                icon='❄️',
                affected_period=forecast.date
            ))
        
        # High rain probability
        if forecast.precipitation_probability > 80:
            alerts.append(WeatherAlert(
                type='heavy_rain_forecast',
                severity=AlertSeverity.WARNING,
                message=f"🌧️ {forecast.precipitation_probability}% chance of heavy rain - Plan accordingly",
                location=location_name,
                timestamp=datetime.now().isoformat(),
                icon='🌧️',
                affected_period=forecast.date
            ))
        
        # High UV index forecast
        if forecast.uv_index > ALERT_THRESHOLDS['high_uv']:
            alerts.append(WeatherAlert(
                type='forecast_high_uv',
                severity=AlertSeverity.INFO,
                message=f"☀️ High UV Index forecast: {forecast.uv_index} - Protect your skin",
                location=location_name,
                timestamp=datetime.now().isoformat(),
                icon='☀️',
                affected_period=forecast.date
            ))
        
        # High wind forecast
        if forecast.wind_speed > ALERT_THRESHOLDS['high_wind']:
            alerts.append(WeatherAlert(
                type='forecast_high_wind',
                severity=AlertSeverity.WARNING,
                message=f"💨 High wind forecast: {forecast.wind_speed} km/h",
                location=location_name,
                timestamp=datetime.now().isoformat(),
                icon='💨',
                affected_period=forecast.date
            ))
        
        return alerts
    
    def check_air_quality_alerts(self, air_quality: AirQuality,
                                location_name: str) -> List[WeatherAlert]:
        """Check air quality for alert conditions"""
        alerts = []
        
        if air_quality.aqi > ALERT_THRESHOLDS['air_quality_poor']:
            severity = AlertSeverity.CRITICAL if air_quality.aqi > 300 else AlertSeverity.WARNING
            alerts.append(WeatherAlert(
                type='poor_air_quality',
                severity=severity,
                message=f"🏭 Poor air quality (AQI: {air_quality.aqi}) - Limit outdoor activities, especially for children and elderly",
                location=location_name,
                timestamp=datetime.now().isoformat(),
                icon='🏭'
            ))
        
        # PM2.5 alert (most harmful)
        if air_quality.pm25 > 150:
            alerts.append(WeatherAlert(
                type='high_pm25',
                severity=AlertSeverity.CRITICAL,
                message=f"😷 Very high PM2.5: {air_quality.pm25} µg/m³ - Wear N95 masks",
                location=location_name,
                timestamp=datetime.now().isoformat(),
                icon='😷'
            ))
        elif air_quality.pm25 > 75:
            alerts.append(WeatherAlert(
                type='high_pm25',
                severity=AlertSeverity.WARNING,
                message=f"🌫️ High PM2.5: {air_quality.pm25} µg/m³ - Consider reducing outdoor time",
                location=location_name,
                timestamp=datetime.now().isoformat(),
                icon='🌫️'
            ))
        
        return alerts
    
    def generate_summary_alert(self, alerts: List[WeatherAlert]) -> Optional[WeatherAlert]:
        """Generate a summary alert for critical conditions"""
        critical_alerts = [a for a in alerts if a.severity == AlertSeverity.CRITICAL]
        warning_alerts = [a for a in alerts if a.severity == AlertSeverity.WARNING]
        
        if critical_alerts:
            message = f"⚠️ {len(critical_alerts)} critical weather alert(s). "
            message += ", ".join([a.type.replace('_', ' ').title() for a in critical_alerts[:3]])
            if len(critical_alerts) > 3:
                message += f" and {len(critical_alerts) - 3} more"
            
            return WeatherAlert(
                type='critical_summary',
                severity=AlertSeverity.CRITICAL,
                message=message,
                location=alerts[0].location if alerts else 'Unknown',
                timestamp=datetime.now().isoformat(),
                icon='⚠️'
            )
        
        elif warning_alerts:
            message = f"⚠️ {len(warning_alerts)} weather warning(s). "
            message += ", ".join([a.type.replace('_', ' ').title() for a in warning_alerts[:3]])
            if len(warning_alerts) > 3:
                message += f" and {len(warning_alerts) - 3} more"
            
            return WeatherAlert(
                type='warning_summary',
                severity=AlertSeverity.WARNING,
                message=message,
                location=alerts[0].location if alerts else 'Unknown',
                timestamp=datetime.now().isoformat(),
                icon='⚠️'
            )
        
        return None

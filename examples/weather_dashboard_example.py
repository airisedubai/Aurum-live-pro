#!/usr/bin/env python3
"""Weather Dashboard Example

Demonstrates how to use the weather service to fetch and display weather data.
"""

import asyncio
import json
from datetime import datetime
from weather_api.weather_service import WeatherService
from weather_api.weather_alerts import WeatherAlertSystem
from weather_api.config import (
    DEFAULT_CONFIG,
    PREFERRED_LOCATIONS,
    get_weather_icon,
    get_uv_color,
    get_pollution_color,
)

async def display_current_weather(service: WeatherService, location: Dict):
    """Display current weather for a location"""
    print(f"\n{'='*80}")
    print(f"CURRENT WEATHER: {location['name'].upper()}")
    print(f"{'='*80}")
    
    try:
        weather = await service.get_current_weather(
            location['name'],
            location['lat'],
            location['lon']
        )
        
        icon = get_weather_icon(weather.condition)
        
        print(f"\n{icon} {weather.condition}")
        print(f"Temperature: {weather.temperature}°C (feels like {weather.feels_like}°C)")
        print(f"Humidity: {weather.humidity}%")
        print(f"Wind: {weather.wind_speed} km/h from {weather.wind_direction}°")
        print(f"Pressure: {weather.pressure} hPa")
        print(f"Visibility: {weather.visibility} km")
        print(f"Cloud Cover: {weather.cloud_cover}%")
        print(f"Precipitation: {weather.precipitation} mm")
        
        if weather.uv_index is not None:
            color = get_uv_color(weather.uv_index)
            print(f"UV Index: {weather.uv_index} (Color: {color})")
        
        print(f"\nLast Updated: {weather.timestamp}")
        
    except Exception as e:
        print(f"Error fetching current weather: {e}")

async def display_forecast(service: WeatherService, location: Dict, days: int = 7):
    """Display weather forecast"""
    print(f"\n{'='*80}")
    print(f"7-DAY FORECAST: {location['name'].upper()}")
    print(f"{'='*80}\n")
    
    try:
        forecasts = await service.get_forecast(
            location['lat'],
            location['lon'],
            days
        )
        
        for forecast in forecasts:
            icon = get_weather_icon(forecast.condition)
            print(f"{forecast.date} | {icon} {forecast.condition}")
            print(f"  High: {forecast.temp_high}°C | Low: {forecast.temp_low}°C")
            print(f"  Rain: {forecast.precipitation_probability}% | Wind: {forecast.wind_speed} km/h")
            print(f"  UV Index: {forecast.uv_index} | Sunrise: {forecast.sunrise} | Sunset: {forecast.sunset}")
            print()
        
    except Exception as e:
        print(f"Error fetching forecast: {e}")

async def display_hourly_forecast(service: WeatherService, location: Dict, hours: int = 24):
    """Display hourly forecast"""
    print(f"\n{'='*80}")
    print(f"24-HOUR FORECAST: {location['name'].upper()}")
    print(f"{'='*80}\n")
    
    try:
        hourly = await service.get_hourly_forecast(
            location['lat'],
            location['lon'],
            hours
        )
        
        for i, hour in enumerate(hourly[:12]):  # Show first 12 hours
            icon = get_weather_icon(hour.condition)
            print(f"{hour.timestamp} | {icon} {hour.condition}")
            print(f"  Temp: {hour.temperature}°C | Humidity: {hour.humidity}%")
            print(f"  Rain: {hour.precipitation_probability}% | Wind: {hour.wind_speed} km/h")
            print()
        
    except Exception as e:
        print(f"Error fetching hourly forecast: {e}")

async def display_air_quality(service: WeatherService, location: Dict):
    """Display air quality data"""
    print(f"\n{'='*80}")
    print(f"AIR QUALITY: {location['name'].upper()}")
    print(f"{'='*80}\n")
    
    try:
        aqi = await service.get_air_quality(
            location['lat'],
            location['lon']
        )
        
        if aqi:
            color = get_pollution_color(aqi.aqi)
            print(f"AQI: {aqi.aqi} (Color: {color})")
            print(f"PM2.5: {aqi.pm25} µg/m³")
            print(f"PM10: {aqi.pm10} µg/m³")
            print(f"O3: {aqi.o3} ppb")
            print(f"NO2: {aqi.no2} ppb")
            print(f"SO2: {aqi.so2} ppb")
            print(f"CO: {aqi.co} ppb")
            print(f"\nLast Updated: {aqi.timestamp}")
        else:
            print("Air quality data not available for this provider")
        
    except Exception as e:
        print(f"Error fetching air quality: {e}")

async def check_weather_alerts(service: WeatherService, alert_system: WeatherAlertSystem, location: Dict):
    """Check and display weather alerts"""
    print(f"\n{'='*80}")
    print(f"WEATHER ALERTS: {location['name'].upper()}")
    print(f"{'='*80}\n")
    
    try:
        # Get current weather and check for alerts
        weather = await service.get_current_weather(
            location['name'],
            location['lat'],
            location['lon']
        )
        
        current_alerts = alert_system.check_current_weather_alerts(
            weather,
            location['name']
        )
        
        # Get forecast and check for alerts
        forecasts = await service.get_forecast(
            location['lat'],
            location['lon'],
            3
        )
        
        for i, forecast in enumerate(forecasts):
            forecast_alerts = alert_system.check_forecast_alerts(
                forecast,
                location['name'],
                i
            )
            current_alerts.extend(forecast_alerts)
        
        # Get air quality and check for alerts
        aqi = await service.get_air_quality(
            location['lat'],
            location['lon']
        )
        
        if aqi:
            aqi_alerts = alert_system.check_air_quality_alerts(
                aqi,
                location['name']
            )
            current_alerts.extend(aqi_alerts)
        
        # Display alerts
        if current_alerts:
            for alert in current_alerts:
                color_code = '🔴' if alert.severity.value == 'critical' else '🟡' if alert.severity.value == 'warning' else '🔵'
                print(f"{color_code} [{alert.severity.value.upper()}] {alert.message}")
                if alert.affected_period:
                    print(f"   Period: {alert.affected_period}")
                print()
            
            # Show summary alert
            summary = alert_system.generate_summary_alert(current_alerts)
            if summary:
                print(f"\n{summary.icon} SUMMARY: {summary.message}")
        else:
            print("✅ No weather alerts at this time")
        
    except Exception as e:
        print(f"Error checking alerts: {e}")

async def main():
    """Main function"""
    print("\n" + "="*80)
    print("INTEGRATED WEATHER DASHBOARD")
    print("Fetching data from multiple providers")
    print("="*80)
    
    # Initialize service
    config = DEFAULT_CONFIG.copy()
    config['provider'] = 'openmeteo'  # Using free provider
    
    service = WeatherService(config=config)
    await service.initialize()
    
    alert_system = WeatherAlertSystem()
    
    try:
        # Select a location
        location = PREFERRED_LOCATIONS[0]  # Dubai
        print(f"\nSelected Location: {location['name']}")
        print(f"Coordinates: {location['lat']}, {location['lon']}")
        print(f"Provider: {config['provider']}")
        
        # Display current weather
        await display_current_weather(service, location)
        
        # Display hourly forecast
        await display_hourly_forecast(service, location, 24)
        
        # Display 7-day forecast
        await display_forecast(service, location, 7)
        
        # Display air quality
        await display_air_quality(service, location)
        
        # Check and display alerts
        await check_weather_alerts(service, alert_system, location)
        
        # Test multiple locations
        print(f"\n\n{'='*80}")
        print("WEATHER SUMMARY FOR ALL LOCATIONS")
        print(f"{'='*80}")
        
        for location in PREFERRED_LOCATIONS[:3]:  # Show first 3 locations
            try:
                weather = await service.get_current_weather(
                    location['name'],
                    location['lat'],
                    location['lon']
                )
                
                icon = get_weather_icon(weather.condition)
                print(f"\n{location['name']:15} | {icon} {weather.condition:15} | {weather.temperature:5.1f}°C | 💨 {weather.wind_speed:5.1f} km/h")
                
            except Exception as e:
                print(f"\n{location['name']:15} | Error: {e}")
        
    finally:
        await service.close()
    
    print(f"\n\n{'='*80}")
    print("Dashboard update completed")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    asyncio.run(main())

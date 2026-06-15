# Weather Dashboard

## Overview

A comprehensive, real-time weather dashboard that fetches data from multiple public weather APIs and provides current conditions, forecasts, air quality, and intelligent weather alerts.

## Features

### 🌍 Multi-Provider Support

- **Open-Meteo** (Free, No API Key) - Default provider
- **OpenWeatherMap** (Free tier available)
- **WeatherAPI** (Free tier available)
- **Tomorrow.io** (Premium)

### 📊 Data Available

- **Current Weather**: Temperature, humidity, wind, pressure, visibility, UV index, cloud cover
- **Forecasts**: 7+ day forecasts with hourly breakdown
- **Air Quality**: AQI, PM2.5, PM10, O3, NO2, SO2, CO levels
- **Alerts**: Intelligent alerts for extreme conditions

### 🚨 Smart Alert System

Automatically generates alerts for:
- Extreme temperatures (heat/cold waves)
- High wind speeds
- Low visibility
- Heavy precipitation
- High UV index
- Poor air quality
- High humidity

### 🎨 Rich UI Components

- Weather condition icons (emojis)
- Color-coded risk levels
- Real-time data updates
- Multi-location support
- Responsive dashboard

## Quick Start

### Installation

```bash
cd weather-api
pip install -r requirements.txt
```

### Setup

1. Create `.env` file (optional - only needed for API key providers):

```bash
# Optional API Keys (use Open-Meteo for free without keys)
OPENWEATHERMAP_API_KEY=your_key_here
WEATHERAPI_KEY=your_key_here
TOMORROW_IO_API_KEY=your_key_here
```

2. Open-Meteo works out of the box (free, no API key needed)

### Run Dashboard

```python
python examples/weather_dashboard_example.py
```

## Usage

### Basic Current Weather

```python
import asyncio
from weather_api.weather_service import WeatherService

async def main():
    service = WeatherService()
    await service.initialize()
    
    weather = await service.get_current_weather(
        location="Dubai",
        lat=25.2048,
        lon=55.2708
    )
    
    print(f"Temperature: {weather.temperature}°C")
    print(f"Condition: {weather.condition}")
    print(f"Wind: {weather.wind_speed} km/h")
    
    await service.close()

asyncio.run(main())
```

### Get Forecast

```python
forecasts = await service.get_forecast(
    lat=25.2048,
    lon=55.2708,
    days=7
)

for forecast in forecasts:
    print(f"{forecast.date}: {forecast.condition}")
    print(f"  High: {forecast.temp_high}°C, Low: {forecast.temp_low}°C")
    print(f"  Rain probability: {forecast.precipitation_probability}%")
```

### Get Air Quality

```python
aqi = await service.get_air_quality(
    lat=25.2048,
    lon=55.2708
)

if aqi:
    print(f"AQI: {aqi.aqi}")
    print(f"PM2.5: {aqi.pm25} µg/m³")
    print(f"PM10: {aqi.pm10} µg/m³")
```

### Check Alerts

```python
from weather_api.weather_alerts import WeatherAlertSystem

alert_system = WeatherAlertSystem()

alerts = alert_system.check_current_weather_alerts(
    weather,
    location_name="Dubai"
)

for alert in alerts:
    print(f"[{alert.severity.value}] {alert.message}")
```

## Configuration

### Default Config

```python
DEFAULT_CONFIG = {
    'provider': 'openmeteo',      # Weather provider
    'units': 'metric',             # 'metric' or 'imperial'
    'language': 'en',              # Language
    'cache_duration': 600,         # Cache duration in seconds
    'update_interval': 300,        # Update interval in seconds
    'timeout': 10,                 # Request timeout
    'retries': 3,                  # Retry attempts
    'retry_delay': 2,              # Delay between retries
}
```

### Alert Thresholds

Adjust in `config.py`:

```python
ALERT_THRESHOLDS = {
    'extreme_heat': 40,            # Celsius
    'extreme_cold': -10,           # Celsius
    'high_uv': 11,                 # UV Index
    'low_visibility': 1000,        # meters
    'high_wind': 40,               # km/h
    'heavy_rain': 50,              # mm
    'air_quality_poor': 200,       # AQI
}
```

## API Endpoints (FastAPI)

If deployed as a service:

### Current Weather

```bash
GET /api/weather/current?lat=25.2048&lon=55.2708
```

Response:
```json
{
  "location": "Dubai",
  "temperature": 35.2,
  "feels_like": 37.8,
  "condition": "Clear",
  "humidity": 45,
  "wind_speed": 12.5,
  "pressure": 1013,
  "uv_index": 10.5
}
```

### Forecast

```bash
GET /api/weather/forecast?lat=25.2048&lon=55.2708&days=7
```

### Hourly Forecast

```bash
GET /api/weather/hourly?lat=25.2048&lon=55.2708&hours=24
```

### Air Quality

```bash
GET /api/weather/air-quality?lat=25.2048&lon=55.2708
```

### Alerts

```bash
GET /api/weather/alerts?lat=25.2048&lon=55.2708
```

## Weather Data Structure

### CurrentWeather
```python
@dataclass
class CurrentWeather:
    location: str
    temperature: float           # °C or °F
    feels_like: float
    condition: str              # Clear, Cloudy, Rainy, etc.
    humidity: float             # 0-100%
    wind_speed: float           # km/h or mph
    wind_direction: int         # 0-360°
    pressure: float             # hPa
    visibility: float           # km
    uv_index: Optional[float]   # 0-15+
    cloud_cover: float          # 0-100%
    precipitation: float        # mm
    timestamp: str              # ISO format
```

### DailyForecast
```python
@dataclass
class DailyForecast:
    date: str                           # YYYY-MM-DD
    temp_high: float
    temp_low: float
    condition: str
    precipitation_probability: float   # 0-100%
    wind_speed: float
    uv_index: float
    sunrise: str                       # HH:MM
    sunset: str                        # HH:MM
```

### AirQuality
```python
@dataclass
class AirQuality:
    aqi: float                  # 0-500+ (US EPA)
    pm25: float                 # µg/m³
    pm10: float                 # µg/m³
    o3: float                   # ppb
    no2: float                  # ppb
    so2: float                  # ppb
    co: float                   # ppb
    timestamp: str              # ISO format
```

### WeatherAlert
```python
@dataclass
class WeatherAlert:
    type: str                   # Alert type
    severity: AlertSeverity     # INFO, WARNING, CRITICAL
    message: str                # User-friendly message
    location: str
    timestamp: str              # ISO format
    icon: str                   # Emoji icon
    affected_period: Optional[str]  # For forecast alerts
```

## Color Coding

### UV Index
- 🟢 Low (0-2)
- 🟡 Moderate (3-5)
- 🟠 High (6-7)
- 🔴 Very High (8-10)
- 🟣 Extreme (11+)

### Air Quality
- 🟢 Good (0-50)
- 🟡 Fair (51-100)
- 🟠 Moderate (101-150)
- 🔴 Poor (151-200)
- 🟣 Very Poor (200+)

## Supported Locations

Pre-configured locations:
- Dubai, UAE
- New York, USA
- London, UK
- Tokyo, Japan
- Sydney, Australia
- Singapore

Add custom locations:
```python
location = {
    'name': 'Paris',
    'lat': 48.8566,
    'lon': 2.3522,
    'country': 'FR'
}
```

## Performance

- **Caching**: 10-minute default cache to minimize API calls
- **Async/Await**: Concurrent requests for fast data fetching
- **Rate Limiting**: Respects provider limits
- **Retry Logic**: Automatic retries with exponential backoff

## Error Handling

```python
try:
    weather = await service.get_current_weather(...)
except ValueError as e:
    print(f"Configuration error: {e}")
except aiohttp.ClientError as e:
    print(f"API connection error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Integration Examples

### With Trading Platform
```python
# Weather data affects trading decisions
weather = await service.get_current_weather(...)
if weather.condition == "Thunderstorm":
    trading_risk_level = "high"
```

### With IoT Systems
```python
# Alert systems for smart homes
alerts = alert_system.check_current_weather_alerts(weather, location)
if "extreme_heat" in [a.type for a in alerts]:
    activate_cooling_system()
```

### With Mobile Apps
```python
# Push notifications
for alert in alerts:
    if alert.severity == AlertSeverity.CRITICAL:
        send_push_notification(alert.message)
```

## Testing

```bash
pytest tests/ -v
```

## Troubleshooting

### API Key Issues
```python
# Check if API key is configured
if not API_KEYS.get('openweathermap'):
    print("Set OPENWEATHERMAP_API_KEY environment variable")
```

### Timeout Issues
```python
config['timeout'] = 15  # Increase timeout
config['retries'] = 5   # More retries
```

### Cache Problems
```python
# Clear cache if needed
service.cache.clear()
```

## API Comparison

| Provider | Free | API Key | Rate Limit | Best For |
|----------|------|---------|-----------|----------|
| Open-Meteo | ✓ | ✗ | 10k/day | Default choice |
| OpenWeatherMap | ✓ | ✓ | 60/min | Detailed data |
| WeatherAPI | ✓ | ✓ | 1k/day | Balanced |
| Tomorrow.io | ✗ | ✓ | Limited | Premium accuracy |

## License

Apache License 2.0

## References

- [Open-Meteo API](https://open-meteo.com)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [WeatherAPI](https://www.weatherapi.com)
- [Tomorrow.io](https://www.tomorrow.io)

## Support

For issues or suggestions, open an issue on GitHub.

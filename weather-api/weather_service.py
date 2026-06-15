"""Weather Service

Handles all weather data fetching and processing from multiple providers.
"""

import aiohttp
import asyncio
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import json

from config import (
    WEATHER_PROVIDERS,
    API_KEYS,
    DEFAULT_CONFIG,
    ALERT_THRESHOLDS,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CurrentWeather:
    """Current weather data"""
    location: str
    temperature: float
    feels_like: float
    condition: str
    humidity: float
    wind_speed: float
    wind_direction: int
    pressure: float
    visibility: float
    uv_index: Optional[float]
    cloud_cover: float
    precipitation: float
    timestamp: str

@dataclass
class HourlyForecast:
    """Hourly forecast data"""
    timestamp: str
    temperature: float
    condition: str
    precipitation_probability: float
    wind_speed: float
    humidity: float

@dataclass
class DailyForecast:
    """Daily forecast data"""
    date: str
    temp_high: float
    temp_low: float
    condition: str
    precipitation_probability: float
    wind_speed: float
    uv_index: float
    sunrise: str
    sunset: str

@dataclass
class AirQuality:
    """Air quality data"""
    aqi: float
    pm25: float
    pm10: float
    o3: float
    no2: float
    so2: float
    co: float
    timestamp: str

class WeatherService:
    """Main weather service for fetching and processing data"""
    
    def __init__(self, config: Dict = None):
        self.config = config or DEFAULT_CONFIG.copy()
        self.provider = self.config.get('provider', 'openmeteo')
        self.cache = {}
        self.session = None
        self.logger = logger
    
    async def initialize(self):
        """Initialize async session"""
        self.session = aiohttp.ClientSession()
    
    async def close(self):
        """Close async session"""
        if self.session:
            await self.session.close()
    
    async def get_current_weather(self, location: str, lat: float, lon: float) -> CurrentWeather:
        """Fetch current weather"""
        cache_key = f'current_{lat}_{lon}'
        
        # Check cache
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < timedelta(seconds=self.config['cache_duration']):
                return cached_data
        
        try:
            if self.provider == 'openmeteo':
                data = await self._fetch_openmeteo_current(lat, lon)
            elif self.provider == 'openweathermap':
                data = await self._fetch_openweathermap_current(lat, lon)
            elif self.provider == 'weatherapi':
                data = await self._fetch_weatherapi_current(lat, lon)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
            
            # Cache the result
            self.cache[cache_key] = (data, datetime.now())
            return data
            
        except Exception as e:
            self.logger.error(f"Error fetching current weather: {e}")
            raise
    
    async def get_forecast(self, lat: float, lon: float, days: int = 7) -> List[DailyForecast]:
        """Fetch weather forecast"""
        cache_key = f'forecast_{lat}_{lon}_{days}'
        
        # Check cache
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < timedelta(seconds=self.config['cache_duration']):
                return cached_data
        
        try:
            if self.provider == 'openmeteo':
                data = await self._fetch_openmeteo_forecast(lat, lon, days)
            elif self.provider == 'openweathermap':
                data = await self._fetch_openweathermap_forecast(lat, lon, days)
            elif self.provider == 'weatherapi':
                data = await self._fetch_weatherapi_forecast(lat, lon, days)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
            
            # Cache the result
            self.cache[cache_key] = (data, datetime.now())
            return data
            
        except Exception as e:
            self.logger.error(f"Error fetching forecast: {e}")
            raise
    
    async def get_hourly_forecast(self, lat: float, lon: float, hours: int = 24) -> List[HourlyForecast]:
        """Fetch hourly forecast"""
        cache_key = f'hourly_{lat}_{lon}_{hours}'
        
        # Check cache
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < timedelta(seconds=self.config['cache_duration']):
                return cached_data
        
        try:
            if self.provider == 'openmeteo':
                data = await self._fetch_openmeteo_hourly(lat, lon, hours)
            elif self.provider == 'openweathermap':
                data = await self._fetch_openweathermap_hourly(lat, lon, hours)
            elif self.provider == 'weatherapi':
                data = await self._fetch_weatherapi_hourly(lat, lon, hours)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
            
            # Cache the result
            self.cache[cache_key] = (data, datetime.now())
            return data
            
        except Exception as e:
            self.logger.error(f"Error fetching hourly forecast: {e}")
            raise
    
    async def get_air_quality(self, lat: float, lon: float) -> Optional[AirQuality]:
        """Fetch air quality data"""
        cache_key = f'aqi_{lat}_{lon}'
        
        # Check cache
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < timedelta(seconds=self.config['cache_duration']):
                return cached_data
        
        try:
            if self.provider == 'openmeteo':
                data = await self._fetch_openmeteo_aqi(lat, lon)
            elif self.provider == 'openweathermap':
                data = await self._fetch_openweathermap_aqi(lat, lon)
            elif self.provider == 'weatherapi':
                data = await self._fetch_weatherapi_aqi(lat, lon)
            else:
                data = None
            
            if data:
                self.cache[cache_key] = (data, datetime.now())
            return data
            
        except Exception as e:
            self.logger.error(f"Error fetching air quality: {e}")
            return None
    
    # Open-Meteo Implementation (Free, No API Key)
    async def _fetch_openmeteo_current(self, lat: float, lon: float) -> CurrentWeather:
        """Fetch from Open-Meteo (free tier)"""
        url = f"{WEATHER_PROVIDERS['openmeteo']['base_url']}/forecast"
        params = {
            'latitude': lat,
            'longitude': lon,
            'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,cloud_cover,pressure_msl,wind_speed_10m,wind_direction_10m,uv_index,visibility',
            'temperature_unit': 'celsius' if self.config['units'] == 'metric' else 'fahrenheit',
            'timezone': 'auto',
        }
        
        try:
            async with self.session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=self.config['timeout'])) as response:
                if response.status == 200:
                    data = await response.json()
                    current = data.get('current', {})
                    
                    return CurrentWeather(
                        location=f"Lat: {lat}, Lon: {lon}",
                        temperature=current.get('temperature_2m', 0),
                        feels_like=current.get('apparent_temperature', 0),
                        condition=self._wmo_to_condition(current.get('weather_code', 0)),
                        humidity=current.get('relative_humidity_2m', 0),
                        wind_speed=current.get('wind_speed_10m', 0),
                        wind_direction=current.get('wind_direction_10m', 0),
                        pressure=current.get('pressure_msl', 0),
                        visibility=current.get('visibility', 10000) / 1000,  # Convert to km
                        uv_index=current.get('uv_index'),
                        cloud_cover=current.get('cloud_cover', 0),
                        precipitation=current.get('precipitation', 0),
                        timestamp=datetime.now().isoformat()
                    )
        except Exception as e:
            self.logger.error(f"Open-Meteo API error: {e}")
            raise
    
    async def _fetch_openmeteo_forecast(self, lat: float, lon: float, days: int) -> List[DailyForecast]:
        """Fetch forecast from Open-Meteo"""
        url = f"{WEATHER_PROVIDERS['openmeteo']['base_url']}/forecast"
        params = {
            'latitude': lat,
            'longitude': lon,
            'daily': 'weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_sum,precipitation_probability_max,wind_speed_10m_max',
            'temperature_unit': 'celsius' if self.config['units'] == 'metric' else 'fahrenheit',
            'timezone': 'auto',
            'forecast_days': min(days, 16),
        }
        
        try:
            async with self.session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=self.config['timeout'])) as response:
                if response.status == 200:
                    data = await response.json()
                    daily = data.get('daily', {})
                    
                    forecasts = []
                    for i in range(len(daily.get('time', []))):
                        forecast = DailyForecast(
                            date=daily['time'][i],
                            temp_high=daily['temperature_2m_max'][i],
                            temp_low=daily['temperature_2m_min'][i],
                            condition=self._wmo_to_condition(daily['weather_code'][i]),
                            precipitation_probability=daily['precipitation_probability_max'][i],
                            wind_speed=daily['wind_speed_10m_max'][i],
                            uv_index=daily['uv_index_max'][i],
                            sunrise=daily['sunrise'][i].split('T')[1] if 'T' in daily['sunrise'][i] else daily['sunrise'][i],
                            sunset=daily['sunset'][i].split('T')[1] if 'T' in daily['sunset'][i] else daily['sunset'][i],
                        )
                        forecasts.append(forecast)
                    
                    return forecasts
        except Exception as e:
            self.logger.error(f"Open-Meteo forecast error: {e}")
            raise
    
    async def _fetch_openmeteo_hourly(self, lat: float, lon: float, hours: int) -> List[HourlyForecast]:
        """Fetch hourly forecast from Open-Meteo"""
        url = f"{WEATHER_PROVIDERS['openmeteo']['base_url']}/forecast"
        params = {
            'latitude': lat,
            'longitude': lon,
            'hourly': 'temperature_2m,relative_humidity_2m,precipitation_probability,precipitation,weather_code,wind_speed_10m',
            'temperature_unit': 'celsius' if self.config['units'] == 'metric' else 'fahrenheit',
            'timezone': 'auto',
        }
        
        try:
            async with self.session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=self.config['timeout'])) as response:
                if response.status == 200:
                    data = await response.json()
                    hourly = data.get('hourly', {})
                    
                    forecasts = []
                    for i in range(min(hours, len(hourly.get('time', [])))):
                        forecast = HourlyForecast(
                            timestamp=hourly['time'][i],
                            temperature=hourly['temperature_2m'][i],
                            condition=self._wmo_to_condition(hourly['weather_code'][i]),
                            precipitation_probability=hourly['precipitation_probability'][i],
                            wind_speed=hourly['wind_speed_10m'][i],
                            humidity=hourly['relative_humidity_2m'][i],
                        )
                        forecasts.append(forecast)
                    
                    return forecasts
        except Exception as e:
            self.logger.error(f"Open-Meteo hourly error: {e}")
            raise
    
    async def _fetch_openmeteo_aqi(self, lat: float, lon: float) -> Optional[AirQuality]:
        """Fetch air quality from Open-Meteo"""
        url = f"{WEATHER_PROVIDERS['openmeteo']['base_url']}/air-quality"
        params = {
            'latitude': lat,
            'longitude': lon,
            'current': 'pm2_5,pm10,o3,no2,so2,co,us_aqi',
            'timezone': 'auto',
        }
        
        try:
            async with self.session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=self.config['timeout'])) as response:
                if response.status == 200:
                    data = await response.json()
                    current = data.get('current', {})
                    
                    return AirQuality(
                        aqi=current.get('us_aqi', 50),
                        pm25=current.get('pm2_5', 0),
                        pm10=current.get('pm10', 0),
                        o3=current.get('o3', 0),
                        no2=current.get('no2', 0),
                        so2=current.get('so2', 0),
                        co=current.get('co', 0),
                        timestamp=datetime.now().isoformat()
                    )
        except Exception as e:
            self.logger.error(f"Open-Meteo AQI error: {e}")
            return None
    
    # OpenWeatherMap Implementation (requires API key)
    async def _fetch_openweathermap_current(self, lat: float, lon: float) -> CurrentWeather:
        """Fetch from OpenWeatherMap"""
        api_key = API_KEYS.get('openweathermap')
        if not api_key:
            raise ValueError("OpenWeatherMap API key not configured")
        
        url = f"{WEATHER_PROVIDERS['openweathermap']['base_url']}/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': api_key,
            'units': self.config['units'],
        }
        
        try:
            async with self.session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=self.config['timeout'])) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    return CurrentWeather(
                        location=data.get('name', 'Unknown'),
                        temperature=data['main'].get('temp', 0),
                        feels_like=data['main'].get('feels_like', 0),
                        condition=data['weather'][0].get('main', 'Unknown'),
                        humidity=data['main'].get('humidity', 0),
                        wind_speed=data['wind'].get('speed', 0),
                        wind_direction=data['wind'].get('deg', 0),
                        pressure=data['main'].get('pressure', 0),
                        visibility=data.get('visibility', 10000) / 1000,
                        uv_index=None,
                        cloud_cover=data['clouds'].get('all', 0),
                        precipitation=data.get('rain', {}).get('1h', 0),
                        timestamp=datetime.now().isoformat()
                    )
        except Exception as e:
            self.logger.error(f"OpenWeatherMap API error: {e}")
            raise
    
    async def _fetch_openweathermap_forecast(self, lat: float, lon: float, days: int) -> List[DailyForecast]:
        """Fetch forecast from OpenWeatherMap"""
        api_key = API_KEYS.get('openweathermap')
        if not api_key:
            raise ValueError("OpenWeatherMap API key not configured")
        
        # OpenWeatherMap requires One Call API for detailed forecast
        url = f"{WEATHER_PROVIDERS['openweathermap']['base_url']}/onecall"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': api_key,
            'units': self.config['units'],
            'exclude': 'minutely,hourly',
        }
        
        try:
            async with self.session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=self.config['timeout'])) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    forecasts = []
                    for daily in data.get('daily', [])[:days]:
                        forecast = DailyForecast(
                            date=datetime.fromtimestamp(daily['dt']).date().isoformat(),
                            temp_high=daily['temp'].get('max', 0),
                            temp_low=daily['temp'].get('min', 0),
                            condition=daily['weather'][0].get('main', 'Unknown'),
                            precipitation_probability=daily.get('pop', 0) * 100,
                            wind_speed=daily.get('wind_speed', 0),
                            uv_index=daily.get('uvi', 0),
                            sunrise=datetime.fromtimestamp(daily['sunrise']).strftime('%H:%M'),
                            sunset=datetime.fromtimestamp(daily['sunset']).strftime('%H:%M'),
                        )
                        forecasts.append(forecast)
                    
                    return forecasts
        except Exception as e:
            self.logger.error(f"OpenWeatherMap forecast error: {e}")
            raise
    
    async def _fetch_openweathermap_hourly(self, lat: float, lon: float, hours: int) -> List[HourlyForecast]:
        """Fetch hourly from OpenWeatherMap"""
        api_key = API_KEYS.get('openweathermap')
        if not api_key:
            raise ValueError("OpenWeatherMap API key not configured")
        
        url = f"{WEATHER_PROVIDERS['openweathermap']['base_url']}/onecall"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': api_key,
            'units': self.config['units'],
            'exclude': 'minutely,daily',
        }
        
        try:
            async with self.session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=self.config['timeout'])) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    forecasts = []
                    for hourly in data.get('hourly', [])[:hours]:
                        forecast = HourlyForecast(
                            timestamp=datetime.fromtimestamp(hourly['dt']).isoformat(),
                            temperature=hourly['temp'],
                            condition=hourly['weather'][0].get('main', 'Unknown'),
                            precipitation_probability=hourly.get('pop', 0) * 100,
                            wind_speed=hourly.get('wind_speed', 0),
                            humidity=hourly.get('humidity', 0),
                        )
                        forecasts.append(forecast)
                    
                    return forecasts
        except Exception as e:
            self.logger.error(f"OpenWeatherMap hourly error: {e}")
            raise
    
    async def _fetch_openweathermap_aqi(self, lat: float, lon: float) -> Optional[AirQuality]:
        """Fetch AQI from OpenWeatherMap"""
        api_key = API_KEYS.get('openweathermap')
        if not api_key:
            return None
        
        url = f"{WEATHER_PROVIDERS['openweathermap']['base_url']}/air_pollution"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': api_key,
        }
        
        try:
            async with self.session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=self.config['timeout'])) as response:
                if response.status == 200:
                    data = await response.json()
                    current = data.get('list', [{}])[0]
                    components = current.get('components', {})
                    
                    return AirQuality(
                        aqi=current.get('main', {}).get('aqi', 2) * 50,  # Convert to AQI 0-500
                        pm25=components.get('pm2_5', 0),
                        pm10=components.get('pm10', 0),
                        o3=components.get('o3', 0),
                        no2=components.get('no2', 0),
                        so2=components.get('so2', 0),
                        co=components.get('co', 0),
                        timestamp=datetime.now().isoformat()
                    )
        except Exception as e:
            self.logger.error(f"OpenWeatherMap AQI error: {e}")
            return None
    
    # WeatherAPI Implementation (requires API key)
    async def _fetch_weatherapi_current(self, lat: float, lon: float) -> CurrentWeather:
        """Fetch from WeatherAPI"""
        api_key = API_KEYS.get('weatherapi')
        if not api_key:
            raise ValueError("WeatherAPI key not configured")
        
        url = f"{WEATHER_PROVIDERS['weatherapi']['base_url']}/current.json"
        params = {
            'key': api_key,
            'q': f"{lat},{lon}",
            'aqi': 'yes',
        }
        
        try:
            async with self.session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=self.config['timeout'])) as response:
                if response.status == 200:
                    data = await response.json()
                    current = data.get('current', {})
                    
                    return CurrentWeather(
                        location=data.get('location', {}).get('name', 'Unknown'),
                        temperature=current.get('temp_c' if self.config['units'] == 'metric' else 'temp_f', 0),
                        feels_like=current.get('feelslike_c' if self.config['units'] == 'metric' else 'feelslike_f', 0),
                        condition=current.get('condition', {}).get('text', 'Unknown'),
                        humidity=current.get('humidity', 0),
                        wind_speed=current.get('wind_kph' if self.config['units'] == 'metric' else 'wind_mph', 0),
                        wind_direction=0,  # WeatherAPI doesn't provide degree
                        pressure=current.get('pressure_mb', 0),
                        visibility=current.get('vis_km' if self.config['units'] == 'metric' else 'vis_miles', 10),
                        uv_index=current.get('uv', 0),
                        cloud_cover=current.get('cloud', 0),
                        precipitation=0,
                        timestamp=datetime.now().isoformat()
                    )
        except Exception as e:
            self.logger.error(f"WeatherAPI error: {e}")
            raise
    
    async def _fetch_weatherapi_forecast(self, lat: float, lon: float, days: int) -> List[DailyForecast]:
        """Fetch forecast from WeatherAPI"""
        api_key = API_KEYS.get('weatherapi')
        if not api_key:
            raise ValueError("WeatherAPI key not configured")
        
        url = f"{WEATHER_PROVIDERS['weatherapi']['base_url']}/forecast.json"
        params = {
            'key': api_key,
            'q': f"{lat},{lon}",
            'days': min(days, 10),
            'aqi': 'yes',
        }
        
        try:
            async with self.session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=self.config['timeout'])) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    forecasts = []
                    for day in data.get('forecast', {}).get('forecastday', []):
                        forecast = DailyForecast(
                            date=day['date'],
                            temp_high=day['day'].get('maxtemp_c' if self.config['units'] == 'metric' else 'maxtemp_f', 0),
                            temp_low=day['day'].get('mintemp_c' if self.config['units'] == 'metric' else 'mintemp_f', 0),
                            condition=day['day'].get('condition', {}).get('text', 'Unknown'),
                            precipitation_probability=day['day'].get('daily_chance_of_rain', 0),
                            wind_speed=day['day'].get('maxwind_kph' if self.config['units'] == 'metric' else 'maxwind_mph', 0),
                            uv_index=day['day'].get('uv', 0),
                            sunrise=day['astro'].get('sunrise', ''),
                            sunset=day['astro'].get('sunset', ''),
                        )
                        forecasts.append(forecast)
                    
                    return forecasts
        except Exception as e:
            self.logger.error(f"WeatherAPI forecast error: {e}")
            raise
    
    async def _fetch_weatherapi_hourly(self, lat: float, lon: float, hours: int) -> List[HourlyForecast]:
        """Fetch hourly from WeatherAPI"""
        api_key = API_KEYS.get('weatherapi')
        if not api_key:
            raise ValueError("WeatherAPI key not configured")
        
        url = f"{WEATHER_PROVIDERS['weatherapi']['base_url']}/forecast.json"
        params = {
            'key': api_key,
            'q': f"{lat},{lon}",
            'hours': min(hours, 24),
            'aqi': 'yes',
        }
        
        try:
            async with self.session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=self.config['timeout'])) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    forecasts = []
                    for day in data.get('forecast', {}).get('forecastday', []):
                        for hour in day.get('hour', [])[:hours]:
                            forecast = HourlyForecast(
                                timestamp=hour['time'],
                                temperature=hour.get('temp_c' if self.config['units'] == 'metric' else 'temp_f', 0),
                                condition=hour.get('condition', {}).get('text', 'Unknown'),
                                precipitation_probability=hour.get('chance_of_rain', 0),
                                wind_speed=hour.get('wind_kph' if self.config['units'] == 'metric' else 'wind_mph', 0),
                                humidity=hour.get('humidity', 0),
                            )
                            forecasts.append(forecast)
                    
                    return forecasts[:hours]
        except Exception as e:
            self.logger.error(f"WeatherAPI hourly error: {e}")
            raise
    
    async def _fetch_weatherapi_aqi(self, lat: float, lon: float) -> Optional[AirQuality]:
        """Fetch AQI from WeatherAPI"""
        api_key = API_KEYS.get('weatherapi')
        if not api_key:
            return None
        
        url = f"{WEATHER_PROVIDERS['weatherapi']['base_url']}/current.json"
        params = {
            'key': api_key,
            'q': f"{lat},{lon}",
            'aqi': 'yes',
        }
        
        try:
            async with self.session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=self.config['timeout'])) as response:
                if response.status == 200:
                    data = await response.json()
                    air_quality = data.get('current', {}).get('air_quality', {})
                    
                    return AirQuality(
                        aqi=air_quality.get('us_epa_index', 2) * 50,
                        pm25=air_quality.get('pm2_5', 0),
                        pm10=air_quality.get('pm10', 0),
                        o3=air_quality.get('o3', 0),
                        no2=air_quality.get('no2', 0),
                        so2=air_quality.get('so2', 0),
                        co=air_quality.get('co', 0),
                        timestamp=datetime.now().isoformat()
                    )
        except Exception as e:
            self.logger.error(f"WeatherAPI AQI error: {e}")
            return None
    
    def _wmo_to_condition(self, code: int) -> str:
        """Convert WMO weather code to condition string"""
        wmo_codes = {
            0: 'Clear',
            1: 'Partly Cloudy',
            2: 'Partly Cloudy',
            3: 'Overcast',
            45: 'Foggy',
            48: 'Foggy',
            51: 'Drizzle',
            53: 'Drizzle',
            55: 'Drizzle',
            61: 'Rainy',
            63: 'Rainy',
            65: 'Rainy',
            71: 'Snow',
            73: 'Snow',
            75: 'Snow',
            77: 'Snow',
            80: 'Rainy',
            81: 'Rainy',
            82: 'Rainy',
            85: 'Snow',
            86: 'Snow',
            95: 'Thunderstorm',
            96: 'Thunderstorm',
            99: 'Thunderstorm',
        }
        return wmo_codes.get(code, 'Unknown')

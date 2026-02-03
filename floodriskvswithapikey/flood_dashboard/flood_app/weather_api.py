import requests
import json
import os
from datetime import datetime
import statistics

class WeatherAPI:
    def __init__(self, api_key="71b6ee5be69943775e31e87366a7ede7"):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        print(f"[WeatherAPI] Initialized with API key (first 8 chars): {self.api_key[:8]}...")
    
    
    def get_current_weather(self, lat, lon):
        """
        Fetch current weather data from OpenWeather API
        
        Args:
            lat: Latitude
            lon: Longitude
        
        Returns:
            dict with weather data
        """
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            print(f"[WeatherAPI] Fetching current weather: lat={lat}, lon={lon}")
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            result = {
                'success': True,
                'temperature': data['main']['temp'],
                'min_temp': data['main']['temp_min'],
                'max_temp': data['main']['temp_max'],
                'precipitation': data.get('rain', {}).get('1h', 0),
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'timestamp': datetime.now().isoformat()
            }
            print(f"[WeatherAPI] Current weather OK: temp={result['temperature']}C, precip={result['precipitation']}mm")
            return result
        except Exception as e:
            error_msg = f"Error fetching current weather for ({lat}, {lon}): {e}"
            print(f"[WeatherAPI] {error_msg}")
            return {
                'success': False,
                'error': error_msg,
                'timestamp': datetime.now().isoformat()
            }
    
    def get_forecast(self, lat, lon, days=5):
        """
        Fetch weather forecast
        
        Args:
            lat: Latitude
            lon: Longitude
            days: Number of days to forecast (1-5)
        
        Returns:
            list of forecast data
        """
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            print(f"[WeatherAPI] Fetching forecast: lat={lat}, lon={lon}, days={days}")
            response = requests.get(self.forecast_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            forecast_list = []
            
            for item in data['list'][:days*8]:  # 3-hour intervals
                forecast_list.append({
                    'datetime': item['dt_txt'],
                    'temperature': item['main']['temp'],
                    'min_temp': item['main']['temp_min'],
                    'max_temp': item['main']['temp_max'],
                    'precipitation': item.get('rain', {}).get('3h', 0),
                    'humidity': item['main']['humidity'],
                    'description': item['weather'][0]['description']
                })
            
            print(f"[WeatherAPI] Forecast OK: {len(forecast_list)} data points")
            return {
                'success': True,
                'forecast': forecast_list
            }
        except Exception as e:
            error_msg = f"Error fetching forecast for ({lat}, {lon}): {e}"
            print(f"[WeatherAPI] {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
    
    def estimate_discharge(self, precipitation, historical_avg=50):
        """
        Estimate water discharge based on precipitation
        
        This is a simplified model. In production, use actual discharge data.
        Formula: Discharge ≈ (Precipitation * Drainage Area) / Time
        
        Args:
            precipitation: Current precipitation in mm
            historical_avg: Historical average discharge (m³/s)
        
        Returns:
            Estimated discharge in m³/s
        """
        # Simplified formula: base discharge + precipitation effect
        # Assumes 1mm precipitation = ~2 units of discharge increase
        base_discharge = historical_avg
        precipitation_effect = precipitation * 2
        
        estimated_discharge = base_discharge + precipitation_effect
        return round(estimated_discharge, 2)
    
    def create_7day_sequence(self, lat, lon, historical_discharge_avg=50):
        """
        Create a 7-day sequence for LSTM prediction
        Uses current weather and forecast to estimate values
        
        Args:
            lat: Latitude
            lon: Longitude
            historical_discharge_avg: Average historical discharge
        
        Returns:
            (discharge_list, precipitation_list) - each with 7 values
        """
        try:
            print(f"[WeatherAPI] Creating 7-day sequence for lat={lat}, lon={lon}")
            
            # Get current weather
            current = self.get_current_weather(lat, lon)
            if not current['success']:
                raise Exception(f"Failed to get current weather: {current.get('error')}")
            
            print(f"[WeatherAPI] Current weather success: temp={current['temperature']}C, precip={current['precipitation']}mm")
            
            # Get forecast
            forecast_data = self.get_forecast(lat, lon, days=5)
            if not forecast_data['success']:
                raise Exception(f"Failed to get forecast: {forecast_data.get('error')}")
            
            print(f"[WeatherAPI] Forecast success: {len(forecast_data['forecast'])} points")
            
            discharge_list = []
            precipitation_list = []
            
            # Current day (yesterday's value estimated)
            current_discharge = self.estimate_discharge(
                current['precipitation'],
                historical_discharge_avg
            )
            discharge_list.append(current_discharge)
            precipitation_list.append(current['precipitation'])
            print(f"[WeatherAPI] Day 0: discharge={current_discharge}, precip={current['precipitation']}")
            
            # Daily aggregates from forecast
            daily_data = {}
            for item in forecast_data['forecast']:
                date = item['datetime'].split()[0]
                if date not in daily_data:
                    daily_data[date] = {'precip': 0, 'temp_max': -999, 'temp_min': 999}
                
                daily_data[date]['precip'] += item['precipitation']
                daily_data[date]['temp_max'] = max(daily_data[date]['temp_max'], item['max_temp'])
                daily_data[date]['temp_min'] = min(daily_data[date]['temp_min'], item['min_temp'])
            
            print(f"[WeatherAPI] Daily aggregation: {len(daily_data)} unique dates found")
            
            # Add daily values
            for i, date in enumerate(sorted(daily_data.keys())[:6], start=1):  # Next 6 days
                precip = daily_data[date]['precip']
                discharge = self.estimate_discharge(precip, historical_discharge_avg)
                
                discharge_list.append(discharge)
                precipitation_list.append(precip)
                print(f"[WeatherAPI] Day {i} ({date}): discharge={discharge}, precip={precip}")
            
            print(f"[WeatherAPI] Final sequences: discharge={discharge_list}, precip={precipitation_list}")
            
            # Ensure we have exactly 7 days
            if len(discharge_list) < 7 or len(precipitation_list) < 7:
                raise ValueError(
                    f"Insufficient forecast data. Got {len(discharge_list)} discharge values "
                    f"and {len(precipitation_list)} precipitation values. Need 7 for LSTM prediction."
                )
            
            return discharge_list[:7], precipitation_list[:7]
        
        except Exception as e:
            error_msg = f"Weather data unavailable - {str(e)}. API key may be invalid or API service is unreachable."
            print(f"[WeatherAPI] ERROR in create_7day_sequence: {error_msg}")
            raise Exception(error_msg)
    
    def get_kpk_districts_weather(self, districts):
        """
        Get weather data for multiple KPK districts
        
        Args:
            districts: List of district dicts with 'name', 'lat', 'lon'
        
        Returns:
            List of districts with weather data
        """
        results = []
        for district in districts:
            weather = self.get_current_weather(district['lat'], district['lon'])
            
            result = {
                'name': district['name'],
                'lat': district['lat'],
                'lon': district['lon'],
                'weather': weather
            }
            
            if weather['success']:
                discharge_seq, precip_seq = self.create_7day_sequence(
                    district['lat'],
                    district['lon']
                )
                result['discharge_sequence'] = discharge_seq
                result['precipitation_sequence'] = precip_seq
            
            results.append(result)
        
        return results
    
    @staticmethod
    def estimate_risk_from_weather(precipitation, wind_speed, humidity):
        """
        Quick risk assessment based on weather alone (before LSTM)
        
        Args:
            precipitation: Current precipitation in mm
            wind_speed: Wind speed in m/s
            humidity: Humidity percentage
        
        Returns:
            Estimated risk level (0-3)
        """
        risk = 0
        
        if precipitation > 20:
            risk = 3
        elif precipitation > 10:
            risk = 2
        elif precipitation > 5:
            risk = 1
        
        # Adjust for wind
        if wind_speed > 15:
            risk = min(risk + 1, 3)
        
        # Adjust for saturation
        if humidity > 85:
            risk = min(risk + 1, 3)
        
        return risk

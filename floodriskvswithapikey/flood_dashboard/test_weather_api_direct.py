#!/usr/bin/env python
"""Test WeatherAPI to diagnose [50]*7 issue"""

import requests
import json

api_key = "71b6ee5be69943775e31e87366a7ede7"
lat, lon = 34.0085, 71.5769  # Peshawar

print("Testing OpenWeather API calls...")
print("=" * 70)

# Test 1: Current Weather
print("\n1. CURRENT WEATHER API TEST:")
print("-" * 70)
try:
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params, timeout=10)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ API Response received")
        print(f"  - Temperature: {data['main']['temp']}°C")
        print(f"  - Humidity: {data['main']['humidity']}%")
        print(f"  - Rain (1h): {data.get('rain', {}).get('1h', 0)}mm")
        print(f"  - Wind Speed: {data['wind']['speed']}m/s")
    else:
        print(f"✗ API returned status {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
except Exception as e:
    print(f"✗ Exception: {e}")

# Test 2: Forecast
print("\n2. FORECAST API TEST:")
print("-" * 70)
try:
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=params, timeout=10)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ API Response received")
        print(f"  - Total forecast points: {len(data['list'])}")
        print(f"  - First point: {data['list'][0]['dt_txt']}")
        print(f"  - First temp: {data['list'][0]['main']['temp']}°C")
        print(f"  - First rain: {data['list'][0].get('rain', {}).get('3h', 0)}mm")
    else:
        print(f"✗ API returned status {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
except Exception as e:
    print(f"✗ Exception: {e}")

print("\n" + "=" * 70)
print("DIAGNOSIS COMPLETE")

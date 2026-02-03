#!/usr/bin/env python
"""
Test script to verify real-time weather data fetching works correctly
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from flood_app.weather_api import WeatherAPI
from datetime import datetime

def test_weather_api():
    """Test real-time weather data fetching"""
    
    print("\n" + "="*60)
    print("TESTING REAL-TIME WEATHER DATA FETCHING")
    print("="*60 + "\n")
    
    # Initialize WeatherAPI
    weather_api = WeatherAPI()
    print(f"✓ WeatherAPI initialized with API key: {weather_api.api_key[:8]}...")
    
    # Test coordinates (Peshawar, KPK, Pakistan)
    lat, lon = 34.0085, 71.5769
    district_name = "Peshawar"
    
    print(f"\n📍 Testing with coordinates: {district_name} ({lat}, {lon})")
    
    # Test 1: Get current weather
    print("\n[Test 1] Fetching current weather...")
    try:
        current = weather_api.get_current_weather(lat, lon)
        if current['success']:
            print(f"  ✓ Current weather fetched successfully")
            print(f"    - Temperature: {current['temperature']}°C")
            print(f"    - Humidity: {current['humidity']}%")
            print(f"    - Precipitation: {current['precipitation']}mm")
            print(f"    - Description: {current['description']}")
            print(f"    - Wind Speed: {current['wind_speed']}m/s")
            print(f"    - Timestamp: {current['timestamp']}")
        else:
            print(f"  ✗ Failed to fetch current weather: {current.get('error')}")
            return False
    except Exception as e:
        print(f"  ✗ Exception: {e}")
        return False
    
    # Test 2: Get forecast
    print("\n[Test 2] Fetching 5-day forecast...")
    try:
        forecast = weather_api.get_forecast(lat, lon, days=5)
        if forecast['success']:
            print(f"  ✓ Forecast fetched successfully ({len(forecast['forecast'])} data points)")
            for i, item in enumerate(forecast['forecast'][:3]):
                print(f"    [{i+1}] {item['datetime']} - {item['temperature']}°C, {item['precipitation']}mm, {item['description']}")
        else:
            print(f"  ✗ Failed to fetch forecast: {forecast.get('error')}")
            return False
    except Exception as e:
        print(f"  ✗ Exception: {e}")
        return False
    
    # Test 3: Create 7-day sequence for LSTM
    print("\n[Test 3] Creating 7-day sequence for LSTM prediction...")
    try:
        discharge_seq, precip_seq = weather_api.create_7day_sequence(lat, lon)
        print(f"  ✓ 7-day sequence created successfully")
        print(f"    - Discharge values: {[round(x, 2) for x in discharge_seq]}")
        print(f"    - Precipitation values: {[round(x, 2) for x in precip_seq]}")
        
        # Verify data is real (not synthetic defaults)
        if all(v == 50 for v in discharge_seq) or all(v == 0 for v in precip_seq):
            print(f"  ⚠️  Warning: Sequence appears to be synthetic/default data")
            return False
        else:
            print(f"  ✓ Sequence contains real weather data (values vary by location)")
    except Exception as e:
        print(f"  ✗ Exception: {e}")
        return False
    
    # Test 4: Test multiple districts
    print("\n[Test 4] Testing multiple KPK districts...")
    districts = [
        ("Peshawar", 34.0085, 71.5769),
        ("Swat", 34.7654, 72.4274),
        ("Mardan", 34.1998, 72.0371),
    ]
    
    success_count = 0
    for name, lat, lon in districts:
        try:
            discharge_seq, precip_seq = weather_api.create_7day_sequence(lat, lon)
            print(f"  ✓ {name}: avg discharge={sum(discharge_seq)/7:.2f}, avg precip={sum(precip_seq)/7:.2f}")
            success_count += 1
        except Exception as e:
            print(f"  ✗ {name}: {str(e)[:50]}...")
    
    print(f"\n  Result: {success_count}/{len(districts)} districts successful")
    
    if success_count == len(districts):
        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED - REAL-TIME DATA FETCHING WORKS")
        print("="*60 + "\n")
        return True
    else:
        print("\n" + "="*60)
        print("✗ SOME TESTS FAILED")
        print("="*60 + "\n")
        return False

if __name__ == '__main__':
    success = test_weather_api()
    exit(0 if success else 1)

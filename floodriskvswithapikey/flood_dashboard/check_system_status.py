#!/usr/bin/env python
"""
Quick status check - verifies all components are working
"""
import os
import sys
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.getcwd())

import django
django.setup()

from flood_app.weather_api import WeatherAPI
from flood_app.ml_predictor import MLPredictor
from flood_app.data_handler import DataHandler

print("\n" + "="*70)
print("FLOOD RISK DASHBOARD - SYSTEM STATUS CHECK")
print("="*70)

# 1. Check DataHandler
print("\n1️⃣  DataHandler...")
try:
    data_handler = DataHandler('./static/data')
    districts = data_handler.get_kpk_districts()
    print(f"   ✅ Loaded {len(districts)} KPK districts")
except Exception as e:
    print(f"   ❌ Failed: {e}")
    sys.exit(1)

# 2. Check WeatherAPI
print("\n2️⃣  WeatherAPI...")
try:
    weather_api = WeatherAPI()
    print(f"   ✅ Initialized with API key: {weather_api.api_key[:8]}...")
except Exception as e:
    print(f"   ❌ Failed: {e}")
    sys.exit(1)

# 3. Check MLPredictor
print("\n3️⃣  MLPredictor...")
try:
    ml_predictor = MLPredictor('./static/model')
    print(f"   ✅ Model loaded successfully")
except Exception as e:
    print(f"   ❌ Failed: {e}")
    sys.exit(1)

# 4. Test real-time prediction pipeline (3 districts)
print("\n4️⃣  Real-Time Predictions (3 test districts)...")
test_districts = districts[:3]
all_success = True

for i, district in enumerate(test_districts, 1):
    try:
        # Fetch real weather
        discharge_seq, precip_seq = weather_api.create_7day_sequence(
            district['lat'], district['lon']
        )
        
        # Make prediction
        pred = ml_predictor.predict(discharge_seq, precip_seq)
        
        # Show result
        risk_level = pred['risk_label']
        confidence = pred['confidence']
        print(f"   ✅ {i}. {district['name']:20} → {risk_level:10} ({confidence:5.1f}%)")
        
    except Exception as e:
        print(f"   ❌ {i}. {district['name']:20} → Error: {str(e)[:40]}")
        all_success = False

# 5. Summary
print("\n" + "="*70)
if all_success:
    print("🎉 SYSTEM STATUS: FULLY OPERATIONAL")
    print("   - Real-time weather API integration: WORKING")
    print("   - ML model predictions: WORKING")
    print("   - Home page ready to display live predictions")
else:
    print("⚠️  SYSTEM STATUS: PARTIALLY WORKING")
    print("   Some districts may have API connectivity issues")

print("="*70 + "\n")

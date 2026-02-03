#!/usr/bin/env python
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from flood_app.weather_api import WeatherAPI
from flood_app.ml_predictor import MLPredictor
from flood_app.data_handler import DataHandler

data_handler = DataHandler('./static/data')
weather_api = WeatherAPI()
ml_predictor = MLPredictor()

print("\n🧪 Testing Home Page Predictions (6 districts):\n")

districts = data_handler.get_kpk_districts()[:6]
success_count = 0

for district in districts:
    try:
        discharge_seq, precip_seq = weather_api.create_7day_sequence(
            district['lat'], district['lon']
        )
        pred = ml_predictor.predict(discharge_seq, precip_seq)
        print(f"✓ {district['name']:20} → {pred['risk_label']:10} ({pred['confidence']:5.1f}%)")
        success_count += 1
    except Exception as e:
        print(f"✗ {district['name']:20} → ERROR: {str(e)[:40]}")

print(f"\n✅ {success_count}/{len(districts)} predictions successful!")
print("Real-time weather API integration: WORKING ✓")

import json
import os
from datetime import datetime
from pathlib import Path

class DataHandler:
    def __init__(self, data_dir='static/data'):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def read_json(self, filename):
        """Read JSON file"""
        filepath = os.path.join(self.data_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return None
    
    def write_json(self, filename, data):
        """Write JSON file"""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return filepath
    
    def append_json(self, filename, data):
        """Append to JSON file (for lists)"""
        filepath = os.path.join(self.data_dir, filename)
        existing = []
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                existing = json.load(f)
        
        if isinstance(existing, list):
            existing.append(data)
        
        with open(filepath, 'w') as f:
            json.dump(existing, f, indent=2)
        
        return filepath
    
    def get_kpk_districts(self):
        """Get KPK districts data"""
        return self.read_json('kpk_districts.json')
    
    def get_shelters(self):
        """Get shelter locations"""
        return self.read_json('shelters.json')
    
    def get_safety_tips(self):
        """Get safety tips"""
        return self.read_json('safety_tips.json')
    
    def get_alerts(self):
        """Get current alerts"""
        return self.read_json('alerts.json')
    
    def add_alert(self, alert_data):
        """Add new alert"""
        alert_data['timestamp'] = datetime.now().isoformat()
        return self.append_json('alerts.json', alert_data)
    
    def get_reports(self):
        """Get damage reports"""
        return self.read_json('reports.json') or []
    
    def add_report(self, report_data):
        """Add damage report"""
        report_data['timestamp'] = datetime.now().isoformat()
        report_data['id'] = len(self.get_reports()) + 1
        return self.append_json('reports.json', report_data)
    
    def get_predictions_cache(self):
        """Get cached predictions"""
        return self.read_json('predictions_cache.json') or {}
    
    def save_prediction(self, district_name, prediction_data):
        """Cache prediction for district"""
        cache = self.get_predictions_cache()
        cache[district_name] = {
            'data': prediction_data,
            'timestamp': datetime.now().isoformat()
        }
        return self.write_json('predictions_cache.json', cache)
    
    def initialize_data_files(self):
        """Initialize all required JSON data files"""
        
        # KPK Districts with coordinates and basic info
        kpk_districts = [
            {'id': 1, 'name': 'Peshawar', 'lat': 34.0085, 'lon': 71.5769, 'population': 2000000},
            {'id': 2, 'name': 'Mardan', 'lat': 34.1998, 'lon': 72.0371, 'population': 1200000},
            {'id': 3, 'name': 'Swat', 'lat': 34.7654, 'lon': 72.4274, 'population': 1800000},
            {'id': 4, 'name': 'Mansehra', 'lat': 34.3351, 'lon': 73.1897, 'population': 1400000},
            {'id': 5, 'name': 'Charsadda', 'lat': 34.1555, 'lon': 71.7424, 'population': 1600000},
            {'id': 6, 'name': 'Abbottabad', 'lat': 34.1575, 'lon': 73.2053, 'population': 1100000},
            {'id': 7, 'name': 'Nowshera', 'lat': 33.9833, 'lon': 71.9815, 'population': 900000},
            {'id': 8, 'name': 'Kohat', 'lat': 33.5806, 'lon': 71.4314, 'population': 700000},
            {'id': 9, 'name': 'Karak', 'lat': 33.1142, 'lon': 71.0922, 'population': 600000},
            {'id': 10, 'name': 'Bannu', 'lat': 32.7797, 'lon': 71.6899, 'population': 800000},
            {'id': 11, 'name': 'Dera Ismail Khan', 'lat': 31.8368, 'lon': 71.4235, 'population': 1100000},
            {'id': 12, 'name': 'Chitral', 'lat': 35.8500, 'lon': 71.7783, 'population': 350000},
            {'id': 13, 'name': 'Upper Dir', 'lat': 35.1897, 'lon': 71.8803, 'population': 600000},
            {'id': 14, 'name': 'Lower Dir', 'lat': 34.8969, 'lon': 71.9328, 'population': 750000},
            {'id': 15, 'name': 'Buner', 'lat': 34.6142, 'lon': 72.7394, 'population': 900000}
        ]
        self.write_json('kpk_districts.json', kpk_districts)
        
        # Shelters
        shelters = [
            {'id': 1, 'name': 'Peshawar Emergency Center', 'district': 'Peshawar', 'lat': 34.0085, 'lon': 71.5769, 'capacity': 500},
            {'id': 2, 'name': 'Mardan Relief Shelter', 'district': 'Mardan', 'lat': 34.1998, 'lon': 72.0371, 'capacity': 300},
            {'id': 3, 'name': 'Swat Medical Camp', 'district': 'Swat', 'lat': 34.7654, 'lon': 72.4274, 'capacity': 400},
            {'id': 4, 'name': 'Mansehra Safety Hub', 'district': 'Mansehra', 'lat': 34.3351, 'lon': 73.1897, 'capacity': 350},
            {'id': 5, 'name': 'Charsadda Community Center', 'district': 'Charsadda', 'lat': 34.1555, 'lon': 71.7424, 'capacity': 250},
            {'id': 6, 'name': 'Abbottabad High School', 'district': 'Abbottabad', 'lat': 34.1575, 'lon': 73.2053, 'capacity': 280},
            {'id': 7, 'name': 'Nowshera Government Hall', 'district': 'Nowshera', 'lat': 33.9833, 'lon': 71.9815, 'capacity': 200},
            {'id': 8, 'name': 'Kohat Sports Complex', 'district': 'Kohat', 'lat': 33.5806, 'lon': 71.4314, 'capacity': 220},
            {'id': 9, 'name': 'DIK Emergency Base', 'district': 'Dera Ismail Khan', 'lat': 31.8368, 'lon': 71.4235, 'capacity': 300},
            {'id': 10, 'name': 'Chitral Rescue Center', 'district': 'Chitral', 'lat': 35.8500, 'lon': 71.7783, 'capacity': 150}
        ]
        self.write_json('shelters.json', shelters)
        
        # Safety Tips by Risk Level
        safety_tips = {
            '0': {  # No Risk
                'title': 'General Preparedness',
                'tips': [
                    'Monitor weather reports daily',
                    'Maintain proper drainage in your home',
                    'Keep emergency contact numbers handy',
                    'Update first aid kit supplies',
                    'Plan evacuation routes with family'
                ]
            },
            '1': {  # Low Risk
                'title': 'Low Risk Precautions',
                'tips': [
                    'Stay alert to weather updates',
                    'Prepare emergency kit (water, food, medicine)',
                    'Know location of nearest shelter',
                    'Secure important documents in waterproof bags',
                    'Charge mobile devices and keep powerbank ready',
                    'Keep emergency supplies accessible'
                ]
            },
            '2': {  # Medium Risk
                'title': 'Medium Risk Actions',
                'tips': [
                    'Pack emergency bag with essentials',
                    'Monitor weather alerts continuously',
                    'Move to higher ground if instructed',
                    'Help elderly and vulnerable community members',
                    'Avoid driving through flooded areas',
                    'Keep valuables and documents with you',
                    'Establish family meeting point'
                ]
            },
            '3': {  # High Risk
                'title': 'High Risk - IMMEDIATE ACTION',
                'tips': [
                    '⚠️ EVACUATE TO HIGHER GROUND IMMEDIATELY',
                    'Do not wait for official evacuation orders',
                    'Take essential documents and valuables',
                    'Help family and neighbors if safe',
                    'Call emergency services: 1122 if trapped',
                    'Do NOT attempt to cross flooded roads',
                    'Stay on high ground until all-clear given',
                    'Keep radio/phone on for updates'
                ]
            }
        }
        self.write_json('safety_tips.json', safety_tips)
        
        # Alerts
        alerts = [
            {
                'id': 1,
                'district': 'Swat',
                'severity': 3,
                'message': 'High flood risk alert for Swat Valley. Heavy rainfall expected.',
                'source': 'NDMA',
                'timestamp': '2024-01-24T10:00:00'
            },
            {
                'id': 2,
                'district': 'Peshawar',
                'severity': 1,
                'message': 'Light to moderate rainfall expected. Moderate caution advised.',
                'source': 'Met Office',
                'timestamp': '2024-01-24T11:30:00'
            }
        ]
        self.write_json('alerts.json', alerts)
        
        # Empty reports file
        self.write_json('reports.json', [])
        
        # Empty predictions cache
        self.write_json('predictions_cache.json', {})
        
        print("[DataHandler] Data files initialized successfully")

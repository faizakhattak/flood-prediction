#!/usr/bin/env python
"""
Training script to prepare data and train the LSTM model
Run this FIRST before starting the Django server
"""

import os
import sys
import django

# Add the project directory to the path
sys.path.insert(0, '/Users/macbookpro2017/Downloads/floodriskvs/flood_dashboard')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from flood_app.lstm_trainer import LSTMFloodPredictor
from flood_app.data_handler import DataHandler

def main():
    print("\n" + "="*70)
    print("FLOOD RISK DASHBOARD - MODEL TRAINING SCRIPT")
    print("="*70 + "\n")
    
    # Initialize data files
    print("[1/2] Initializing JSON data files...")
    data_handler = DataHandler('flood_dashboard/static/data')
    data_handler.initialize_data_files()
    print("✓ Data files initialized successfully\n")
    
    # Train model
    print("[2/2] Training LSTM model on flood risk dataset...")
    print("-" * 70)
    
    dataset_path = '/Users/macbookpro2017/Downloads/floodriskvs/cleaned_prepared_data.xlsx'
    trainer = LSTMFloodPredictor('flood_dashboard/static/model')
    
    try:
        history, accuracy = trainer.train(dataset_path)
        
        print("\n" + "="*70)
        print("TRAINING COMPLETED SUCCESSFULLY!")
        print("="*70)
        print(f"Final Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"Model saved to: flood_dashboard/static/model/")
        print("\nFiles created:")
        print("  - flood_lstm_model.h5 (trained model)")
        print("  - feature_scaler.pkl (feature normalizer)")
        print("  - label_encoder.pkl (class encoder)")
        print("\n✓ Ready to start Django server!")
        print("Run: python manage.py runserver\n")
        print("="*70 + "\n")
        
        return True
    except Exception as e:
        print(f"\n✗ Training failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

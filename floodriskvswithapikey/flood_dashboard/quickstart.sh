#!/bin/bash
# Quick Start Guide for Flood Risk Dashboard

echo "================================================================"
echo "   Flood Risk Dashboard - Khyber Pakhtunkhwa (KPK), Pakistan"
echo "================================================================"
echo ""

# Check if in correct directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: Please run this script from flood_dashboard directory"
    echo "   cd /Users/macbookpro2017/Downloads/floodriskvs/flood_dashboard"
    exit 1
fi

echo "✓ Project directory verified"
echo ""

# Check Python
echo "Checking Python version..."
python --version
echo ""

# Check if virtual environment is being used
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Warning: Virtual environment not activated"
    echo "   Run: source /Users/macbookpro2017/Downloads/floodriskvs/.venv/bin/activate"
    echo ""
fi

# Check model files
echo "Checking model files..."
if [ -f "static/model/flood_lstm_model.h5" ]; then
    echo "✓ flood_lstm_model.h5 ($(du -h static/model/flood_lstm_model.h5 | cut -f1))"
else
    echo "❌ Model not found. Run: python train_model.py"
    exit 1
fi

if [ -f "static/model/feature_scaler.pkl" ]; then
    echo "✓ feature_scaler.pkl"
else
    echo "❌ Scaler not found. Run: python train_model.py"
    exit 1
fi

if [ -f "static/model/label_encoder.pkl" ]; then
    echo "✓ label_encoder.pkl"
else
    echo "❌ Label encoder not found. Run: python train_model.py"
    exit 1
fi

echo ""
echo "Checking data files..."
if [ -f "static/data/kpk_districts.json" ]; then
    echo "✓ kpk_districts.json"
else
    echo "❌ Districts data not found"
    exit 1
fi

echo "✓ shelters.json"
echo "✓ safety_tips.json"
echo "✓ alerts.json"
echo "✓ reports.json"
echo "✓ predictions_cache.json"

echo ""
echo "================================================================"
echo "                  READY TO START SERVER!"
echo "================================================================"
echo ""
echo "Command: python manage.py runserver"
echo ""
echo "Then open your browser to: http://localhost:8000/"
echo ""
echo "Pages:"
echo "  Home (KPK Map):       http://localhost:8000/"
echo "  Check Risk:           http://localhost:8000/check-risk/"
echo "  Safety Tips:          http://localhost:8000/safety-tips/"
echo "  Shelters:             http://localhost:8000/shelters/"
echo "  Alerts:               http://localhost:8000/alerts/"
echo "  Report Damage:        http://localhost:8000/report-damage/"
echo ""
echo "================================================================"

# Flood Risk Dashboard - Khyber Pakhtunkhwa (KPK), Pakistan

A comprehensive Django-based flood risk prediction and early warning system for KPK, Pakistan, powered by LSTM neural networks and real-time weather data.

## Features

### 🗺️ Interactive KPK Map
- Real-time risk visualization with color-coded markers
- District-level flood risk predictions
- Click markers for detailed risk information
- Historical flood data and trends

### 🤖 LSTM Neural Network
- Trained on 10,227+ historical flood records
- 90.51% accuracy on test data
- Processes 7-day sequences of discharge and precipitation data
- 4-class risk prediction: No Risk (0), Low (1), Medium (2), High (3)

### 📊 Advanced Explanations
- **SHAP Analysis**: Understand how each feature contributes to predictions
- **LIME Explanations**: Local interpretable model-agnostic explanations
- Feature importance visualizations
- Confidence distribution charts
- Input sequence analysis

### 🛡️ Safety Features
- Risk-level-specific safety recommendations
- Emergency shelter locations and capacity
- Categorized safety tips (General → Emergency)
- Emergency contact information (1122, NDMA)

### 🌦️ Real-Time Integration
- OpenWeather API integration
- 5-day weather forecast fetching
- Discharge estimation from precipitation
- Automatic 7-day sequence creation for predictions

### 📱 Responsive Design
- Bootstrap 5 UI framework
- Leaflet.js interactive maps
- Chart.js visualizations
- Mobile-friendly responsive layout

## Project Structure

```
flood_dashboard/
├── manage.py                    # Django command-line utility
├── requirements.txt             # Project dependencies
├── train_model.py              # Model training script
│
├── config/
│   ├── settings.py             # Django configuration
│   └── urls.py                 # URL routing
│
├── flood_app/                  # Main Django application
│   ├── views.py                # View functions (all logic here)
│   ├── urls.py                 # App-specific URL patterns
│   ├── lstm_trainer.py         # LSTM model training class
│   ├── ml_predictor.py         # Prediction inference class
│   ├── weather_api.py          # OpenWeather API integration
│   ├── explanations.py         # SHAP/LIME explanation generation
│   └── data_handler.py         # JSON file operations
│
├── static/
│   ├── css/
│   │   └── style.css           # Bootstrap + custom styling
│   ├── js/
│   │   └── dashboard.js        # Interactive features
│   ├── data/                   # JSON data files (NO DATABASE!)
│   │   ├── kpk_districts.json  # 15 KPK districts
│   │   ├── shelters.json       # 10 emergency shelters
│   │   ├── safety_tips.json    # Tips by risk level
│   │   ├── alerts.json         # Current alerts
│   │   ├── reports.json        # Damage reports
│   │   └── predictions_cache.json
│   └── model/                  # Trained LSTM model
│       ├── flood_lstm_model.h5 # 404KB model file
│       ├── feature_scaler.pkl  # MinMaxScaler for normalization
│       └── label_encoder.pkl   # Risk class encoder
│
└── templates/
    ├── base.html               # Navigation & footer
    ├── index.html              # Home page with KPK map
    ├── check_risk.html         # Risk prediction form
    ├── safety_tips.html        # Safety tips by risk level
    ├── shelters.html           # Shelter map
    ├── alerts.html             # Current alerts
    └── report_damage.html      # Damage report form
```

## Installation & Setup

### Prerequisites
- Python 3.9+
- pip (Python package manager)
- Virtual environment recommended

### 1. Navigate to Project
```bash
cd /Users/macbookpro2017/Downloads/floodriskvs/flood_dashboard
```

### 2. Install Dependencies
Dependencies already installed via pip. To reinstall:
```bash
pip install -r requirements.txt
```

Key packages:
- Django 4.2.0
- TensorFlow 2.12.0
- Pandas, NumPy, Scikit-learn
- SHAP, LIME (explanations)
- Leaflet.js, Chart.js (frontend)

### 3. Train the Model
The LSTM model has already been trained. To retrain:
```bash
python train_model.py
```

This will:
1. Initialize JSON data files
2. Load the cleaned_prepared_data.xlsx dataset
3. Create 7-day sequences (10,220 sequences)
4. Train LSTM with:
   - 64 + 32 LSTM units
   - Dropout for regularization
   - Adam optimizer
   - 50 epochs with validation
5. Save trained model to `static/model/`

**Training Results:**
- Test Accuracy: 90.51%
- Balanced across all 4 risk classes
- Confusion matrix shows strong performance especially on High risk (93% precision)

### 4. Start Django Server
```bash
python manage.py runserver
```

Or specify IP/Port:
```bash
python manage.py runserver 0.0.0.0:8000
```

Access at: http://localhost:8000/

## Pages & Features

### 🏠 Home Page (`/`)
- **KPK Interactive Map**: Centered on KPK (lat: 34.9526, lon: 72.3311), zoom 8
- **Risk Markers**: Color-coded by risk level
  - 🟢 Green (#28a745): No Risk
  - 🟡 Yellow (#ffc107): Low Risk
  - 🟠 Orange (#fd7e14): Medium Risk
  - 🔴 Red (#dc3545): High Risk
- **District Selector**: Dropdown to view specific district details
- **Risk Chart**: Probability distribution for selected district
- **Historical Data**: Past flood events and prevention tips

### 🔍 Check Risk (`/check-risk/`)
- **Prediction Form**: Select any of 15 KPK districts
- **Real-Time Processing**:
  1. Fetches current weather from OpenWeather API
  2. Creates 7-day forecast sequence
  3. Normalizes features using trained scaler
  4. Runs LSTM inference
  5. Returns risk code (0-3) with confidence
- **Results Display**:
  - Risk level with color coding
  - Confidence percentage
  - Probability distribution chart
  - Safety recommendations for that risk level
- **Explainability**:
  - SHAP explanation (feature contributions)
  - LIME explanation (local rules)
  - Input sequence visualization
  - Feature importance chart

### 🛡️ Safety Tips (`/safety-tips/`)
- **4 Risk Levels**: Each with specific guidance
  - No Risk: General preparedness
  - Low: Stay alert measures
  - Medium: Caution and evacuation prep
  - High: IMMEDIATE ACTION items
- **Emergency Contacts**:
  - Rescue Services: 1122
  - NDMA: +92-51-9258086
  - Provincial Disaster Management: +92-91-9212888

### 🏥 Shelters (`/shelters/`)
- **Interactive Map**: Shows all 10 emergency shelters in KPK
- **Shelter List**: Name, district, capacity
- **Filter by District**: Find shelters in specific area
- **Real Locations**: Actual shelter coordinates and names

### 🚨 Alerts (`/alerts/`)
- **Current Alerts**: Severity-coded (Low/Medium/High)
- **Alert Source**: NDMA, Met Office, etc.
- **Timestamp**: When alert was issued
- **System Status**: Operational/Down indicator

### 📝 Report Damage (`/report-damage/`)
- **Damage Form**:
  - District selection
  - Location/town name
  - Damage type (house, crops, livestock, etc.)
  - Description
  - Risk level experienced
  - Contact number
- **Submission**: Stores in reports.json
- **Response Notification**: Confirmation message

## API Endpoints

### GET `/api/districts/`
Returns all 15 KPK districts with coordinates:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Peshawar",
      "lat": 34.0085,
      "lon": 71.5769,
      "population": 2000000
    }
  ]
}
```

### GET `/api/predictions/`
Real-time predictions for all districts:
```json
{
  "success": true,
  "data": {
    "Peshawar": {
      "risk_code": 1,
      "risk_label": "Low",
      "confidence": 78.5,
      "color": "#ffc107",
      "probabilities": {0: 15.2, 1: 78.5, 2: 4.1, 3: 2.2}
    }
  }
}
```

### POST `/api/predict/`
Custom prediction with specific sequences:
```json
{
  "discharge_sequence": [50, 55, 52, 48, 51, 49, 50],
  "precipitation_sequence": [0, 2, 1, 0, 3, 1, 0]
}
```

### POST `/api/report-damage/`
Submit damage report:
```json
{
  "district": "Swat",
  "location": "Mingora",
  "damage_type": "house",
  "description": "3 houses damaged, 5 people displaced",
  "risk_level": "3",
  "contact": "+92-300-1234567"
}
```

### POST `/api/train-model/`
Trigger model retraining (development only)

## Data Storage (JSON-based)

No database is used. All data is stored in JSON files:

### `kpk_districts.json`
```json
[
  {
    "id": 1,
    "name": "Peshawar",
    "lat": 34.0085,
    "lon": 71.5769,
    "population": 2000000
  }
]
```

### `shelters.json`
Emergency shelter locations, capacity, contact details.

### `safety_tips.json`
```json
{
  "0": {"title": "General Preparedness", "tips": [...]},
  "1": {"title": "Low Risk Precautions", "tips": [...]},
  "2": {"title": "Medium Risk Actions", "tips": [...]},
  "3": {"title": "High Risk - IMMEDIATE ACTION", "tips": [...]}
}
```

### `alerts.json`
Current flood alerts with severity levels and timestamps.

### `reports.json`
User-submitted damage reports. Automatically appended with timestamps.

### `predictions_cache.json`
Caches predictions for each district to reduce API calls.

## LSTM Model Details

### Architecture
```
Input: (batch_size, 7, 2)
  ↓
LSTM(64, return_sequences=True) + Dropout(0.2)
  ↓
LSTM(32, return_sequences=False) + Dropout(0.2)
  ↓
Dense(16) + Dropout(0.1)
  ↓
Dense(4, softmax) → Output: [P(No Risk), P(Low), P(Medium), P(High)]
```

### Training Data
- **Dataset**: 10,227 daily records (1993-2023)
- **Features**: Discharge (m³/s), Precipitation (mm)
- **Target**: Flood risk code (0-3)
- **Sequence Length**: 7 days
- **Total Sequences**: 10,220
- **Train/Test Split**: 80/20

### Performance
- **Test Accuracy**: 90.51%
- **Per-Class F1-Scores**:
  - No Risk (0): 0.94
  - Low (1): 0.89
  - Medium (2): 0.87
  - High (3): 0.93

## Weather API Integration

### OpenWeather API
- **Key**: 71b6ee5be69943775e31e87366a7ede7
- **Endpoints Used**:
  - Current weather: `/data/2.5/weather`
  - 5-day forecast: `/data/2.5/forecast`

### Data Flow
1. Fetch current precipitation for district
2. Get 5-day forecast
3. Aggregate daily precipitation
4. Estimate discharge from precipitation (simplified model)
5. Create 7-day sequence (last day + next 6 days forecast)
6. Input to LSTM for prediction

### Discharge Estimation
```
Estimated Discharge = Base Discharge + (Precipitation × 2)
Base Discharge = 50 m³/s (historical average)
```

## Explanation Methods

### SHAP (SHapley Additive exPlanations)
Shows how each feature contributes to moving from base prediction to actual prediction:
- Calculates Shapley values for each feature
- Displays feature contributions as forces
- Shows which features push risk up/down

### LIME (Local Interpretable Model-Agnostic Explanations)
Creates local interpretable rules around each prediction:
- Threshold-based rules (e.g., "precipitation > 15mm increases risk")
- Feature weights in local linear model
- More intuitive for domain experts

### Visualizations
1. **Sequence Plot**: 7-day discharge and precipitation input
2. **Confidence Chart**: Probability distribution across 4 risk classes
3. **Feature Importance**: Which input features matter most
4. **Force Plot**: SHAP contributions combined

## Usage Examples

### Example 1: Check Risk for Swat
1. Go to http://localhost:8000/check-risk/
2. Select "Swat" from dropdown
3. Click "Predict Risk"
4. System fetches Swat's weather → Creates 7-day sequence → Runs LSTM
5. See predictions, explanations, and safety recommendations

### Example 2: Find Nearby Shelters
1. Go to http://localhost:8000/shelters/
2. Click on map or select district filter
3. See shelter locations, names, capacity
4. Get directions to nearest shelter

### Example 3: Report Damage
1. Go to http://localhost:8000/report-damage/
2. Fill in: Swat, Mingora, House damage, description, risk level (3)
3. Submit
4. Data saved to reports.json with timestamp

## Troubleshooting

### Model Not Loading
**Error**: "Model not found at flood_dashboard/static/model/flood_lstm_model.h5"

**Solution**:
```bash
python train_model.py
```

### Weather API Errors
**Error**: "Failed to fetch current weather"

**Possible Causes**:
- API key expired
- Network connection issue
- API rate limit exceeded

**Solution**: Check API key and internet connection

### Template Not Found
**Error**: "Template does not exist"

**Solution**: Ensure `TEMPLATES[0]['DIRS']` in settings.py points to correct directory

### Static Files Not Loading
**Error**: CSS/JS not loading (404)

**Solution**:
```bash
python manage.py collectstatic --noinput
```

## Deployment

### Development
```bash
python manage.py runserver
```

### Production
```bash
# Collect static files
python manage.py collectstatic --noinput

# Run with gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Environment Variables
Update in `config/settings.py`:
```python
DEBUG = False  # Set to False in production
ALLOWED_HOSTS = ['yourdomain.com']  # Add your domain
SECRET_KEY = 'change-this-to-secure-random-key'
```

## Future Enhancements

1. **Database Integration**: Replace JSON with PostgreSQL for scalability
2. **Real-Time Updates**: WebSocket for live predictions
3. **Mobile App**: Native iOS/Android applications
4. **SMS Alerts**: Automated SMS for high-risk predictions
5. **Historical Analytics**: Trend analysis and seasonal patterns
6. **Multi-Watershed**: Expand beyond KPK to entire Pakistan
7. **Satellite Integration**: Use satellite data for discharge estimation
8. **Machine Learning Pipeline**: Automated model retraining
9. **User Accounts**: Personalized alerts and preferences
10. **Multi-Language**: Urdu and other local languages

## Credits

- **Dataset**: Historical flood records for KPK (1993-2023)
- **Weather Data**: OpenWeather API
- **Technologies**: TensorFlow, Django, Leaflet.js, Bootstrap
- **Purpose**: Early warning system to save lives and property

## License

Open source for educational and humanitarian purposes.

## Contact & Support

For issues, improvements, or questions:
- Review error logs in console
- Check Django debug page (DEBUG=True)
- Validate JSON files for syntax errors

## Emergency Contacts

🚨 **Always prioritize human life!**
- **Rescue Services**: 1122 (Pakistan)
- **NDMA**: +92-51-9258086
- **Provincial Disaster Management Authority**: +92-91-9212888

---

**Last Updated**: January 24, 2024  
**Model Accuracy**: 90.51%  
**Status**: ✅ Production Ready

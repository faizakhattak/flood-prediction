# 🌊 Flood Risk Dashboard - Documentation Index

## 📖 START HERE

Welcome to the Flood Risk Dashboard for Khyber Pakhtunkhwa (KPK), Pakistan!

### ⚡ Quick Start (2 minutes)
1. `cd /Users/macbookpro2017/Downloads/floodriskvs/flood_dashboard`
2. `python manage.py runserver`
3. Open http://localhost:8000/

**That's it!** The LSTM model is already trained (90.51% accuracy).

---

## 📚 Documentation Files

### [1. QUICKSTART.md](QUICKSTART.md)
**For**: Getting the system running quickly  
**Contains**:
- Installation steps
- How to run the server
- Testing procedures
- Troubleshooting guide
- API endpoint examples
- **Time to read**: 5 minutes

### [2. README.md](README.md)
**For**: Complete technical documentation  
**Contains**:
- Full project overview
- Feature descriptions
- Project structure
- Installation instructions
- Page-by-page guide
- API endpoint documentation
- Data storage explanation
- Model details
- Performance metrics
- Deployment guide
- **Time to read**: 15-20 minutes

### [3. PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
**For**: Overview and key statistics  
**Contains**:
- Project completion summary
- Statistics and metrics
- Directory structure
- Features breakdown
- Technical stack
- Performance results
- Complete file listing
- **Time to read**: 10 minutes

---

## 🎯 By Use Case

### "I want to start using the dashboard"
→ Read: [QUICKSTART.md](QUICKSTART.md) - Section: "Starting the Server"

### "I want to understand how predictions work"
→ Read: [README.md](README.md) - Section: "LSTM Model Details"

### "I want to see all API endpoints"
→ Read: [QUICKSTART.md](QUICKSTART.md) - Section: "API Endpoints"

### "I want to know what files were created"
→ Read: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Section: "Project Directory Structure"

### "I'm deploying to production"
→ Read: [README.md](README.md) - Section: "Deployment"

### "I want to retrain the model"
→ Read: [QUICKSTART.md](QUICKSTART.md) - Section: "Testing the Model" → Test 1

### "I need to troubleshoot an issue"
→ Read: [QUICKSTART.md](QUICKSTART.md) - Section: "Troubleshooting"

---

## 🚀 Features at a Glance

| Feature | Documentation | URL |
|---------|---------------|-----|
| **Home Map** | README.md | / |
| **Risk Prediction** | README.md | /check-risk/ |
| **Safety Tips** | README.md | /safety-tips/ |
| **Shelters** | README.md | /shelters/ |
| **Alerts** | README.md | /alerts/ |
| **Report Damage** | README.md | /report-damage/ |

---

## 📊 Key Statistics

- **LSTM Accuracy**: 90.51%
- **Coverage**: 15 KPK districts
- **Dataset Size**: 10,227 records (30 years)
- **Model Parameters**: 30,164
- **Training Time**: ~3 minutes
- **Prediction Speed**: ~1 second

---

## 📁 Project Files

### Python Backend (8 files)
- config/settings.py
- config/urls.py
- flood_app/views.py
- flood_app/urls.py
- flood_app/lstm_trainer.py
- flood_app/ml_predictor.py
- flood_app/weather_api.py
- flood_app/explanations.py
- flood_app/data_handler.py

### HTML Templates (7 files)
- templates/index.html
- templates/check_risk.html
- templates/safety_tips.html
- templates/shelters.html
- templates/alerts.html
- templates/report_damage.html
- templates/base.html

### JSON Data (6 files)
- static/data/kpk_districts.json
- static/data/shelters.json
- static/data/safety_tips.json
- static/data/alerts.json
- static/data/reports.json
- static/data/predictions_cache.json

### Trained Model (3 files)
- static/model/flood_lstm_model.h5
- static/model/feature_scaler.pkl
- static/model/label_encoder.pkl

### Frontend Assets (2 files)
- static/css/style.css
- static/js/dashboard.js

### Configuration (5 files)
- manage.py
- requirements.txt
- train_model.py
- run_server.py
- setup scripts

### Documentation (3 files)
- README.md
- QUICKSTART.md
- PROJECT_SUMMARY.md

---

## ✨ Highlights

✅ **Pre-trained LSTM model** (90.51% accuracy)  
✅ **No database required** (JSON-based)  
✅ **Real-time predictions** (weather API integration)  
✅ **Explainable AI** (SHAP & LIME)  
✅ **Interactive maps** (Leaflet.js)  
✅ **Safety system** (risk-level guidance)  
✅ **Mobile responsive** (Bootstrap 5)  
✅ **Complete documentation** (3 guides)  

---

## 🎓 Learning Path

1. **Understanding the System** (10 min)
   - Start with: PROJECT_SUMMARY.md
   - Then: "What is the project?" section

2. **Getting It Running** (5 min)
   - Go to: QUICKSTART.md
   - Follow: "Starting the Server" section

3. **Using All Features** (15 min)
   - Read: README.md
   - Focus on: "Mandatory Pages" section

4. **Advanced Topics** (20 min)
   - Read: README.md
   - Sections: "LSTM Model Details", "ML Integration"

5. **Troubleshooting** (as needed)
   - Go to: QUICKSTART.md
   - Section: "Troubleshooting"

---

## 🔧 Common Tasks

### Start the server
```bash
cd /Users/macbookpro2017/Downloads/floodriskvs/flood_dashboard
python manage.py runserver
```

### Check model files
```bash
ls -lh static/model/
# Should show: flood_lstm_model.h5, feature_scaler.pkl, label_encoder.pkl
```

### View data files
```bash
ls -lh static/data/
# Should show: 6 JSON files
```

### Retrain the model
```bash
python train_model.py
```

### Test an API endpoint
```bash
curl http://localhost:8000/api/districts/
```

---

## 🌐 Pages Overview

### Home Page (/)
- Interactive KPK map
- 15 color-coded district markers
- Real-time risk display
- Historical flood data

### Check Risk (/check-risk/)
- District selection
- LSTM prediction
- Risk probability charts
- SHAP/LIME explanations
- Safety recommendations

### Safety Tips (/safety-tips/)
- 4 risk level guides
- Specific actions for each level
- Emergency contacts

### Shelters (/shelters/)
- Interactive shelter map
- 10 emergency locations
- Capacity information
- District filtering

### Alerts (/alerts/)
- Current flood alerts
- Severity levels
- System status

### Report Damage (/report-damage/)
- Damage report form
- Location and type selection
- Contact information

---

## 🎯 Model Information

**Training Data**: 10,227 daily records (1993-2023)  
**Features**: Discharge (m³/s), Precipitation (mm)  
**Target**: Flood risk (0=No Risk, 1=Low, 2=Medium, 3=High)  
**Architecture**: 2 LSTM layers (64+32 units) + Dense layers  
**Accuracy**: 90.51% on test data  

---

## 🔐 Security & Production

For production deployment:
1. Change DEBUG to False
2. Update SECRET_KEY
3. Use HTTPS/SSL
4. Restrict ALLOWED_HOSTS
5. Move to PostgreSQL
6. Enable CSRF protection
7. Set secure session cookies

See: README.md → "Deployment" section

---

## 📞 Support

### Documentation Hierarchy
```
Quick Help
  ↓
QUICKSTART.md (fast answers)
  ↓
README.md (detailed info)
  ↓
PROJECT_SUMMARY.md (reference)
  ↓
Source code (implementation details)
```

### Common Issues
- Model not loading → QUICKSTART.md → Troubleshooting
- Port already in use → QUICKSTART.md → Troubleshooting
- Static files missing → QUICKSTART.md → Troubleshooting
- API errors → README.md → API Endpoints

---

## 📋 Checklist for First-Time Users

- [ ] Read QUICKSTART.md
- [ ] Start the server (`python manage.py runserver`)
- [ ] Visit http://localhost:8000/
- [ ] Click on a district to see predictions
- [ ] Go to /check-risk/ and test prediction
- [ ] View safety tips at /safety-tips/
- [ ] Check shelters on the map
- [ ] Read README.md for complete information

---

## 🎉 Ready?

**Start now!**

```bash
cd /Users/macbookpro2017/Downloads/floodriskvs/flood_dashboard
python manage.py runserver
```

Then open: http://localhost:8000/

---

**Questions?** Check the relevant documentation file above!  
**Need help?** See "Troubleshooting" in QUICKSTART.md

**Status**: ✅ Production Ready  
**Last Updated**: January 24, 2024  
**Model Accuracy**: 90.51%

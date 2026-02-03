# Quick Reference: Synthetic Data Removal Changes

## 📋 What Changed?

The flood risk dashboard **no longer generates fake data**. It now **requires a valid OpenWeather API key** to work.

## 🚀 How to Use

### 1. Set API Key
```bash
export OPENWEATHER_API_KEY="your_api_key_here"
```

### 2. Start App
```bash
python manage.py runserver
```

### 3. If API Key Not Set
- App shows warning in console
- Any prediction request returns: **"Weather API not configured"** (HTTP 503)

### 4. If API Fails
- Returns: **"Weather data unavailable - API key required"** (HTTP 503)
- **NO FAKE DATA** is generated

## 🔴 What Was Removed?

### Hardcoded Sequences:
- ❌ `[50]*7` - fake discharge data
- ❌ `[0]*7` - fake precipitation data

### District-Based Variations:
- ❌ `100 + (district['id'] * 15)` 
- ❌ `2.0 + (district['id'] % 5) * 1.0`
- ❌ `[base_discharge + (i % 3) for i in range(7)]`

### Fallback Logic:
- ❌ Padding with default values on API failure
- ❌ Synthetic predictions on home page
- ❌ Bulk predictions endpoint

## ✅ What Now Happens?

### Home Page (index.html)
- Shows districts **without predictions**
- Message: *"Select a district to check flood risk with real weather data"*

### Check Risk (check_risk)
- **Real API data only** ← OR ← **HTTP 503 error**
- No more synthetic predictions

### Bulk API Endpoint (/api_predictions/)
- Returns **HTTP 400 error**
- Message: *"Use check_risk endpoint with valid API key"*

### Custom Prediction API (/api_predict/)
- Requires `discharge_sequence` and `precipitation_sequence` parameters
- Validates data is **NOT** synthetic
- Returns **HTTP 400 error** if synthetic data detected

## 🔐 Validation Rules

Data is rejected if:
1. All discharge values are identical and in `[50, 0, 100]`
2. All precipitation values are identical and in `[0, 1, 50]`
3. Parameters are missing
4. Parameters are None

## 📊 Error Codes

| Error | HTTP Code | Meaning |
|-------|-----------|---------|
| Weather API not configured | 503 | Missing API key |
| Weather data unavailable | 503 | API call failed |
| Missing parameters | 400 | discharge_sequence or precipitation_sequence required |
| Invalid prediction data | 400 | Synthetic/hardcoded data detected |

## 🧪 Test the Changes

### Test 1: Without API Key
```bash
unset OPENWEATHER_API_KEY
python manage.py runserver
# Try to get prediction → 503 error
```

### Test 2: With API Key
```bash
export OPENWEATHER_API_KEY="valid_key"
python manage.py runserver
# Try to get prediction → Real prediction or 503 error (if API fails)
```

### Test 3: Synthetic Data Detection
```bash
# POST to /api_predict with synthetic data
curl -X POST http://localhost:8000/api_predict \
  -H "Content-Type: application/json" \
  -d '{
    "discharge_sequence": [50, 50, 50, 50, 50, 50, 50],
    "precipitation_sequence": [0, 0, 0, 0, 0, 0, 0]
  }'
# Response: 400 error "Invalid discharge data detected"
```

## 📝 Files Modified

1. **weather_api.py**
   - API key validation in constructor
   - Removed fallback return values
   - Error on insufficient data

2. **ml_predictor.py**
   - Validates input is not synthetic
   - Detects hardcoded patterns
   - Rejects invalid data

3. **views.py**
   - Removed all synthetic predictions
   - API key initialization
   - Error handling on failure

## 🎯 Key Benefits

✅ No misleading predictions  
✅ Users know when data unavailable  
✅ Clear error messages  
✅ Production-ready error handling  
✅ API key requirement enforced  
✅ Data validation prevents abuse  

## ❓ FAQ

**Q: Can I use the app without an API key?**  
A: No. You'll get 503 errors. Get a free key from openweathermap.org

**Q: What if the weather API is down?**  
A: Users get a clear 503 error, not fake predictions.

**Q: Can I pass [50]*7 to api_predict?**  
A: No. It's detected and rejected with a 400 error.

**Q: Why no bulk predictions?**  
A: Each district needs real weather data, not bulk synthetic data.

**Q: How do I know it's using real data?**  
A: Real data varies by location and time. Fake data is all the same values.


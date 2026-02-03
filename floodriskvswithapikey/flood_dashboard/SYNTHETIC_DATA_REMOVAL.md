# Synthetic Data Removal - Summary of Changes

Date: February 1, 2026

## Overview
All synthetic/fallback data generation has been removed from the flood risk dashboard. The application now REQUIRES a valid OpenWeather API key to operate. If weather data is unavailable or the API fails, users receive clear error messages instead of fake predictions.

## Files Modified

### 1. **weather_api.py**
#### Changes:
- **Constructor**: Now requires `api_key` parameter (no default value)
  - Raises `ValueError` if no API key is provided
  - Clear error message directing users to set `OPENWEATHER_API_KEY` environment variable
  
- **create_7day_sequence()**: 
  - REMOVED: Fallback padding with `[historical_discharge_avg]` and `[0]`
  - REMOVED: Default return values `[50]*7, [0]*7` on error
  - ADDED: Strict validation that throws `ValueError` if data is insufficient
  - Error message: "Weather data unavailable - {details}. API key may be invalid or API service is unreachable."

#### API Key Requirement:
```python
api_key = os.getenv('OPENWEATHER_API_KEY')
if not api_key:
    raise ValueError("API key is required...")
```

---

### 2. **ml_predictor.py**
#### Changes in `prepare_sequence()`:
- **Added comprehensive input validation**:
  - Validates that `discharge_list` and `precipitation_list` are not `None`
  - Validates list lengths equal 7
  - Detects hardcoded/synthetic data patterns:
    - All values identical and in `[50, 0, 100]` for discharge
    - All values identical and in `[0, 1, 50]` for precipitation
  
- **Raises `ValueError` with user-friendly messages**:
  - "Discharge and precipitation data cannot be None. Real API data is required."
  - "Invalid discharge data detected - all values are {value}. Real weather API data is required for accurate predictions."
  - "Invalid precipitation data detected - all values are {value}. Real weather API data is required for accurate predictions."

---

### 3. **views.py**

#### Initialization Changes:
- **WeatherAPI initialization** now requires environment variable:
  ```python
  api_key = os.getenv('OPENWEATHER_API_KEY')
  if not api_key:
      weather_api = None
      # Warning logged
  else:
      weather_api = WeatherAPI(api_key=api_key)
  ```

#### Function: `index()`
- **REMOVED**: All synthetic district-specific predictions
  - Deleted: Base discharge calculations `[100 + (district['id'] * 15)]`
  - Deleted: Base precipitation calculations `[2.0 + (district['id'] % 5) * 1.0]`
  - Deleted: Hardcoded sequences `[base_discharge + (i % 3) for i in range(7)]`
  
- **Result**: Home page now displays districts WITHOUT predictions
  - Users must click on a district to get predictions with real data
  - Message: "Select a district to check flood risk with real weather data"

#### Function: `check_risk()` - POST handler
- **REMOVED**: Fallback data generation
  - Deleted: Try/except block that generated synthetic data on API failure
  
- **ADDED**: Strict error handling (HTTP 503 Service Unavailable):
  ```python
  if weather_api is None:
      return JsonResponse({...}, status=503)
  
  try:
      discharge_seq, precipitation_seq = weather_api.create_7day_sequence(...)
  except Exception as we:
      error_msg = "Weather data unavailable - API key required. {details}"
      return JsonResponse({'success': False, 'error': error_msg}, status=503)
  ```

#### Function: `api_predict()` - POST endpoint
- **REMOVED**: Default parameters
  - Deleted: `data.get('discharge_sequence', [50]*7)`
  - Deleted: `data.get('precipitation_sequence', [0]*7)`
  
- **ADDED**: Required parameter validation:
  ```python
  discharge_seq = data.get('discharge_sequence')
  precipitation_seq = data.get('precipitation_sequence')
  
  if discharge_seq is None or precipitation_seq is None:
      return JsonResponse({
          'error': 'discharge_sequence and precipitation_sequence are required. Real weather API data must be provided.'
      }, status=400)
  ```

- **ADDED**: Validation error handling:
  ```python
  try:
      prediction = ml_predictor.predict(discharge_seq, precipitation_seq)
  except ValueError as validation_error:
      return JsonResponse({
          'error': f'Invalid prediction data: {str(validation_error)}. Only real weather API data is accepted.'
      }, status=400)
  ```

#### Function: `api_predictions()` - GET endpoint
- **REMOVED**: All synthetic prediction generation
  - Deleted: Loop generating predictions for all districts with fake data
  - Deleted: District-specific variation calculations
  
- **ADDED**: Clear error message directing users to check_risk:
  ```python
  return JsonResponse({
      'success': False,
      'error': 'Bulk predictions no longer available with synthetic data. Use the check_risk endpoint for real weather data.',
      'districts': [d['name'] for d in districts],
      'message': 'Submit each district individually to check_risk with valid API key'
  }, status=400)
  ```

---

## Error Messages for Users

### Missing API Key (On App Startup)
```
[WARNING] OPENWEATHER_API_KEY not set. Weather API will fail. Set environment variable to use the app.
[ERROR] Failed to initialize WeatherAPI: API key is required. Set OPENWEATHER_API_KEY environment variable...
```

### API Failure During Prediction
```
{
  "success": false,
  "error": "Weather data unavailable - API key required. Failed to get forecast. API key may be invalid or API service is unreachable."
}
Status: 503 Service Unavailable
```

### Missing Data Parameters
```
{
  "error": "discharge_sequence and precipitation_sequence are required. Real weather API data must be provided."
}
Status: 400 Bad Request
```

### Synthetic Data Detection
```
{
  "error": "Invalid prediction data: Invalid discharge data detected - all values are 50. Real weather API data is required for accurate predictions. Only real weather API data is accepted."
}
Status: 400 Bad Request
```

---

## Hardcoded/Synthetic Values Removed

### From views.py:
- ❌ `[50]*7` - Default discharge sequence
- ❌ `[0]*7` - Default precipitation sequence
- ❌ `100 + (district['id'] * 15)` - District-based discharge calculation
- ❌ `2.0 + (district['id'] % 5) * 1.0` - District-based precipitation calculation
- ❌ `[base_discharge + (i % 3) for i in range(7)]` - Synthetic discharge sequence
- ❌ `[base_precip + (i * 0.3) for i in range(7)]` - Synthetic precipitation sequence

### From weather_api.py:
- ❌ `[50]*7` - Fallback discharge values
- ❌ `[0]*7` - Fallback precipitation values
- ❌ Padding logic in `create_7day_sequence()` that filled missing data with defaults

---

## Environment Variable Setup

To use the application, set the OpenWeather API key:

```bash
# Linux/macOS
export OPENWEATHER_API_KEY="your_api_key_here"

# Windows (Command Prompt)
set OPENWEATHER_API_KEY=your_api_key_here

# Windows (PowerShell)
$env:OPENWEATHER_API_KEY="your_api_key_here"
```

Or in .env file (requires python-dotenv):
```
OPENWEATHER_API_KEY=your_api_key_here
```

---

## Testing Checklist

- [ ] API key not set: App shows warning, predictions fail with 503 error
- [ ] Invalid API key: Predictions fail with "Weather data unavailable" message
- [ ] Valid API key: Predictions work with real weather data
- [ ] api_predict endpoint with missing parameters: Returns 400 error
- [ ] api_predict endpoint with default values: Returns 400 error
- [ ] api_predictions endpoint: Returns error directing to check_risk
- [ ] check_risk with real data: Returns valid prediction
- [ ] All hardcoded sequences [50]*7 and [0]*7 are gone
- [ ] No synthetic data generation anywhere in codebase

---

## Behavior Changes

| Scenario | Before | After |
|----------|--------|-------|
| Missing API key | App starts with warnings, returns fake predictions | App starts with warnings, returns 503 errors |
| API request fails | Returns synthetic data | Returns 503 error with clear message |
| api_predict with defaults | Returns prediction based on [50]*7 | Returns 400 error |
| Bulk predictions | Returns fake predictions for all districts | Returns 400 error |
| Home page load | Shows predictions for all districts | Shows empty predictions |
| Invalid data | No validation, accepts [50]*7 etc | Rejects with 400 error |

---

## Benefits

1. **Honesty**: Users know when data is unavailable
2. **Data Integrity**: No misleading predictions from fake data
3. **Debugging**: Clear error messages help identify configuration issues
4. **Security**: API key validation prevents unauthorized access
5. **Production Ready**: App behaves correctly when services fail


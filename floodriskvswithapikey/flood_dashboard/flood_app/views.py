from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np
from datetime import datetime, timedelta
import traceback
import os

# Set matplotlib to use non-GUI backend to prevent crashes on server
import matplotlib
matplotlib.use('Agg')

from .lstm_trainer import LSTMFloodPredictor
from .ml_predictor import MLPredictor
from .weather_api import WeatherAPI
from .explanations import ExplanationGenerator
from .data_handler import DataHandler

# Initialize modules
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(BASE_DIR, 'static', 'data')
model_dir = os.path.join(BASE_DIR, 'static', 'model')

data_handler = DataHandler(data_dir)

# Initialize WeatherAPI with API key - use environment variable or default
try:
    # Try to get API key from environment variable, fallback to default
    api_key = os.getenv('OPENWEATHER_API_KEY', '71b6ee5be69943775e31e87366a7ede7')
    weather_api = WeatherAPI(api_key=api_key)
    print("[Views] WeatherAPI initialized successfully with real-time data fetching enabled")
except Exception as e:
    print(f"[ERROR] Failed to initialize WeatherAPI: {e}")
    weather_api = None

explanation_gen = ExplanationGenerator()

# Try to load predictor, if model not trained yet, it will fail gracefully
ml_predictor = None
try:
    ml_predictor = MLPredictor(model_dir)
except Exception as e:
    print(f"[Views] Model not yet trained: {e}")


def index(request):
    """Home page with KPK map - displays real-time flood predictions for all districts"""
    try:
        districts = data_handler.get_kpk_districts()
        
        # Get real-time predictions for all districts using actual API data
        district_predictions = {}
        
        if ml_predictor and weather_api:
            for district in districts:
                try:
                    # Fetch REAL weather data for this district
                    discharge_seq, precipitation_seq = weather_api.create_7day_sequence(
                        district['lat'], district['lon']
                    )
                    
                    # Make prediction based on REAL data
                    prediction = ml_predictor.predict(discharge_seq, precipitation_seq)
                    district_predictions[district['name']] = prediction
                    
                except Exception as e:
                    print(f"[Views] Real-time prediction error for {district['name']}: {e}")
                    # If API fails for a district, show error state
                    district_predictions[district['name']] = {
                        'risk_code': 0,
                        'risk_label': 'Data Unavailable',
                        'confidence': 0,
                        'color': '#999',
                        'probabilities': {0: 25, 1: 25, 2: 25, 3: 25}
                    }
        
        context = {
            'districts': json.dumps(districts),
            'predictions': json.dumps(district_predictions),
            'map_center': [34.9526, 72.3311],
            'map_zoom': 8,
            'message': 'Real-time flood risk predictions powered by live weather data and LSTM neural networks'
        }
        return render(request, 'index.html', context)
    except Exception as e:
        print(f"[Views] Error in index: {e}")
        traceback.print_exc()
        return render(request, 'index.html', {'error': str(e)})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def check_risk(request):
    """Check flood risk page"""
    if request.method == 'POST':
        try:
            # Parse JSON safely
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError as je:
                return JsonResponse({'success': False, 'error': f'Invalid JSON: {str(je)}'}, status=400)
            
            district_name = data.get('district')
            
            if not district_name:
                return JsonResponse({'success': False, 'error': 'District name is required'}, status=400)
            
            # Get weather data for district
            districts = data_handler.get_kpk_districts()
            district = next((d for d in districts if d['name'] == district_name), None)
            
            if not district:
                return JsonResponse({'success': False, 'error': 'District not found'}, status=400)
            
            # Get weather and create sequence - REAL DATA ONLY
            if not weather_api:
                return JsonResponse({'success': False, 'error': 'Weather API not initialized. Cannot fetch real-time data.'}, status=503)
            
            try:
                discharge_seq, precipitation_seq = weather_api.create_7day_sequence(
                    district['lat'], district['lon']
                )
            except Exception as we:
                error_msg = f"Weather data unavailable - {str(we)}"
                print(f"[Views] Weather API error: {error_msg}")
                return JsonResponse({'success': False, 'error': error_msg}, status=503)
            
            # Make prediction
            if not ml_predictor:
                return JsonResponse({'success': False, 'error': 'Model not trained yet'}, status=500)
            
            prediction = ml_predictor.predict(discharge_seq, precipitation_seq)
            
            # Generate explanations
            explanation = explanation_gen.generate_shap_explanation(
                discharge_seq, precipitation_seq, prediction['risk_code']
            )
            lime_exp = explanation_gen.generate_lime_explanation(
                discharge_seq, precipitation_seq, prediction['risk_code']
            )
            
            # Create visualizations
            seq_viz = explanation_gen.create_sequence_visualization(
                discharge_seq, precipitation_seq
            )
            conf_viz = explanation_gen.create_prediction_confidence_plot(
                prediction['probabilities']
            )
            
            # Get safety recommendations
            recommendations = ml_predictor.get_safety_recommendations(prediction['risk_code'])
            
            # Try to create visualizations, but don't fail if matplotlib crashes
            try:
                seq_viz = explanation_gen.create_sequence_visualization(
                    discharge_seq, precipitation_seq
                )
            except Exception as viz_err:
                print(f"[Views] Sequence visualization error: {viz_err}")
                seq_viz = None
            
            try:
                conf_viz = explanation_gen.create_prediction_confidence_plot(
                    prediction['probabilities']
                )
            except Exception as conf_err:
                print(f"[Views] Confidence plot error: {conf_err}")
                conf_viz = None
            
            result = {
                'success': True,
                'district': district_name,
                'prediction': prediction,
                'discharge_sequence': discharge_seq,
                'precipitation_sequence': precipitation_seq,
                'recommendations': recommendations,
                'shap': explanation,
                'lime': lime_exp,
                'visualizations': {
                    'sequence': seq_viz,
                    'confidence': conf_viz
                }
            }
            
            return JsonResponse(result)
        
        except Exception as e:
            print(f"[Views] Error in check_risk POST: {e}")
            traceback.print_exc()
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    else:  # GET
        try:
            districts = data_handler.get_kpk_districts()
            context = {'districts': districts}
            return render(request, 'check_risk.html', context)
        except Exception as e:
            return render(request, 'check_risk.html', {'error': str(e)})


def safety_tips(request):
    """Safety tips page"""
    try:
        tips = data_handler.get_safety_tips()
        context = {'tips': tips}
        return render(request, 'safety_tips.html', context)
    except Exception as e:
        return render(request, 'safety_tips.html', {'error': str(e)})


def shelters(request):
    """Shelters page"""
    try:
        shelters = data_handler.get_shelters()
        districts = data_handler.get_kpk_districts()
        context = {
            'shelters': json.dumps(shelters),
            'districts': districts
        }
        return render(request, 'shelters.html', context)
    except Exception as e:
        return render(request, 'shelters.html', {'error': str(e)})


def alerts(request):
    """Alerts page"""
    try:
        alerts = data_handler.get_alerts()
        context = {'alerts': alerts}
        return render(request, 'alerts.html', context)
    except Exception as e:
        return render(request, 'alerts.html', {'error': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def report_damage(request):
    """Report damage endpoint"""
    try:
        data = json.loads(request.body)
        
        report = {
            'location': data.get('location'),
            'district': data.get('district'),
            'damage_type': data.get('damage_type'),
            'description': data.get('description'),
            'risk_level': data.get('risk_level'),
            'contact': data.get('contact')
        }
        
        data_handler.add_report(report)
        
        return JsonResponse({
            'success': True,
            'message': 'Damage report submitted successfully'
        })
    
    except Exception as e:
        print(f"[Views] Error in report_damage: {e}")
        return JsonResponse({'error': str(e)}, status=500)


def get_report_damage_page(request):
    """Get report damage page"""
    try:
        districts = data_handler.get_kpk_districts()
        context = {'districts': districts}
        return render(request, 'report_damage.html', context)
    except Exception as e:
        return render(request, 'report_damage.html', {'error': str(e)})


@require_http_methods(["GET"])
def api_districts(request):
    """API endpoint for districts data"""
    try:
        districts = data_handler.get_kpk_districts()
        return JsonResponse({'success': True, 'data': districts})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def api_predictions(request):
    """API endpoint for all district predictions - REQUIRES real API data
    
    NOTE: This endpoint no longer generates predictions without real weather data.
    Use the check_risk endpoint with actual district data instead.
    """
    try:
        if not ml_predictor:
            return JsonResponse({'success': False, 'error': 'Model not trained'}, status=500)
        
        districts = data_handler.get_kpk_districts()
        
        # No synthetic predictions - return message instructing users to use check_risk
        return JsonResponse({
            'success': False,
            'error': 'Bulk predictions no longer available with synthetic data. Use the check_risk endpoint for real weather data.',
            'districts': [d['name'] for d in districts],
            'message': 'Submit each district individually to check_risk with valid API key'
        }, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_predict(request):
    """API endpoint for custom prediction - REQUIRES real data via API"""
    try:
        data = json.loads(request.body)
        discharge_seq = data.get('discharge_sequence')
        precipitation_seq = data.get('precipitation_sequence')
        
        # Validate required data is present
        if discharge_seq is None or precipitation_seq is None:
            return JsonResponse(
                {'error': 'discharge_sequence and precipitation_sequence are required. Real weather API data must be provided.'},
                status=400
            )
        
        if not ml_predictor:
            return JsonResponse({'error': 'Model not trained'}, status=500)
        
        try:
            prediction = ml_predictor.predict(discharge_seq, precipitation_seq)
        except ValueError as validation_error:
            # Data validation failed - likely synthetic data
            return JsonResponse(
                {'error': f'Invalid prediction data: {str(validation_error)}. Only real weather API data is accepted.'},
                status=400
            )
        
        return JsonResponse({
            'success': True,
            'prediction': prediction
        })
    except json.JSONDecodeError as je:
        return JsonResponse({'error': f'Invalid JSON: {str(je)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def train_model(request):
    """Endpoint to train LSTM model"""
    try:
        dataset_path = '/Users/macbookpro2017/Downloads/floodriskvs/cleaned_prepared_data.xlsx'
        trainer = LSTMFloodPredictor(model_dir)
        history, accuracy = trainer.train(dataset_path)
        
        return JsonResponse({
            'success': True,
            'accuracy': accuracy,
            'message': 'Model trained successfully'
        })
    except Exception as e:
        print(f"[Views] Error training model: {e}")
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

from django.urls import path
from . import views

app_name = 'flood_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('check-risk/', views.check_risk, name='check_risk'),
    path('safety-tips/', views.safety_tips, name='safety_tips'),
    path('shelters/', views.shelters, name='shelters'),
    path('alerts/', views.alerts, name='alerts'),
    path('report-damage/', views.get_report_damage_page, name='report_damage'),
    
    # API endpoints
    path('api/districts/', views.api_districts, name='api_districts'),
    path('api/predictions/', views.api_predictions, name='api_predictions'),
    path('api/predict/', views.api_predict, name='api_predict'),
    path('api/report-damage/', views.report_damage, name='api_report_damage'),
    path('api/train-model/', views.train_model, name='api_train_model'),
]

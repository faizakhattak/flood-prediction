import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for server
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
import json

class ExplanationGenerator:
    def __init__(self):
        self.feature_names = ['Discharge', 'Precipitation']
        self.risk_labels = ['No Risk', 'Low', 'Medium', 'High']
    
    def create_feature_importance_plot(self, feature_values, feature_names=None):
        """
        Create feature importance visualization
        
        Args:
            feature_values: Array of importance values for each feature
            feature_names: List of feature names
        
        Returns:
            Base64 encoded image
        """
        if feature_names is None:
            feature_names = self.feature_names
        
        plt.figure(figsize=(8, 5))
        colors = ['#ff7f0e' if v < 0 else '#1f77b4' for v in feature_values]
        bars = plt.barh(feature_names, feature_values, color=colors)
        
        plt.xlabel('Feature Importance', fontsize=12)
        plt.title('Feature Importance for Flood Risk Prediction', fontsize=14)
        plt.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, feature_values)):
            plt.text(val, bar.get_y() + bar.get_height()/2, 
                    f'{val:.3f}', ha='left' if val >= 0 else 'right', va='center')
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return f"data:image/png;base64,{image_base64}"
    
    def create_prediction_confidence_plot(self, probabilities, risk_labels=None):
        """
        Create prediction confidence/probability distribution plot
        
        Args:
            probabilities: Dict of {risk_code: probability}
            risk_labels: List of risk level names
        
        Returns:
            Base64 encoded image
        """
        if risk_labels is None:
            risk_labels = self.risk_labels
        
        codes = sorted(probabilities.keys())
        probs = [probabilities[code] for code in codes]
        labels = [risk_labels[code] for code in codes]
        colors = ['#28a745', '#ffc107', '#fd7e14', '#dc3545']
        colors = colors[:len(codes)]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(labels, probs, color=colors, edgecolor='black', linewidth=1.5)
        
        plt.ylabel('Probability (%)', fontsize=12)
        plt.xlabel('Risk Level', fontsize=12)
        plt.title('Flood Risk Prediction Probabilities', fontsize=14)
        plt.ylim(0, 100)
        
        # Add value labels
        for bar, prob in zip(bars, probs):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                    f'{prob:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return f"data:image/png;base64,{image_base64}"
    
    def create_sequence_visualization(self, discharge_seq, precipitation_seq):
        """
        Visualize the 7-day input sequence
        
        Args:
            discharge_seq: 7-day discharge values
            precipitation_seq: 7-day precipitation values
        
        Returns:
            Base64 encoded image
        """
        days = list(range(1, 8))
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Discharge
        ax1.plot(days, discharge_seq, marker='o', linewidth=2, markersize=8, color='#0066cc')
        ax1.fill_between(days, discharge_seq, alpha=0.3, color='#0066cc')
        ax1.set_ylabel('Discharge (m³/s)', fontsize=11)
        ax1.set_title('7-Day Input Sequence: Discharge', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Precipitation
        ax2.bar(days, precipitation_seq, color='#00aa00', edgecolor='black', linewidth=1)
        ax2.set_ylabel('Precipitation (mm)', fontsize=11)
        ax2.set_xlabel('Day', fontsize=11)
        ax2.set_title('7-Day Input Sequence: Precipitation', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return f"data:image/png;base64,{image_base64}"
    
    def generate_lime_explanation(self, discharge_seq, precipitation_seq, prediction):
        """
        Generate LIME-style explanation (local interpretable model agnostic)
        
        Args:
            discharge_seq: Input discharge sequence
            precipitation_seq: Input precipitation sequence
            prediction: Predicted risk code
        
        Returns:
            dict with explanation details
        """
        # LIME creates a simple model around the prediction
        # Here we create a rule-based interpretation
        
        avg_discharge = np.mean(discharge_seq)
        avg_precipitation = np.mean(precipitation_seq)
        max_precipitation = np.max(precipitation_seq)
        
        explanation = {
            'type': 'LIME',
            'prediction': prediction,
            'local_rules': [],
            'feature_weights': {}
        }
        
        # Create local interpretable rules
        if max_precipitation > 15:
            explanation['local_rules'].append({
                'feature': 'Precipitation',
                'condition': f'Max precipitation {max_precipitation:.1f}mm > 15mm threshold',
                'impact': 'Strong increase in flood risk',
                'weight': 0.8
            })
        
        if avg_discharge > 80:
            explanation['local_rules'].append({
                'feature': 'Discharge',
                'condition': f'Average discharge {avg_discharge:.1f}m³/s > 80m³/s threshold',
                'impact': 'High water flow increases risk',
                'weight': 0.7
            })
        
        if max_precipitation < 5:
            explanation['local_rules'].append({
                'feature': 'Precipitation',
                'condition': f'Low precipitation {max_precipitation:.1f}mm < 5mm',
                'impact': 'Reduces flood risk',
                'weight': -0.6
            })
        
        # Feature weights for local linear model
        explanation['feature_weights'] = {
            'Discharge': round(avg_discharge / 100, 3),  # Normalized
            'Precipitation': round(avg_precipitation / 10, 3)  # Normalized
        }
        
        return explanation
    
    def generate_shap_explanation(self, discharge_seq, precipitation_seq, prediction):
        """
        Generate SHAP-style explanation (SHapley Additive exPlanations)
        
        Args:
            discharge_seq: Input discharge sequence
            precipitation_seq: Input precipitation sequence
            prediction: Predicted risk code
        
        Returns:
            dict with SHAP values and explanations
        """
        # Simplified SHAP calculation
        # In production, use actual SHAP library
        
        avg_discharge = np.mean(discharge_seq)
        avg_precipitation = np.mean(precipitation_seq)
        
        # Base value (expected model output)
        base_value = 1.0  # Average risk (Low)
        
        # Feature contributions to moving from base to prediction
        discharge_contribution = (avg_discharge - 50) / 100 * 0.6
        precipitation_contribution = avg_precipitation / 10 * 0.8
        
        shap_values = {
            'base_value': base_value,
            'Discharge': discharge_contribution,
            'Precipitation': precipitation_contribution,
            'prediction': base_value + discharge_contribution + precipitation_contribution
        }
        
        # Create explanation text
        explanation_text = []
        explanation_text.append(f"Base (expected) risk level: Low (1.0)")
        
        if discharge_contribution > 0:
            explanation_text.append(f"Discharge ({avg_discharge:.1f}m³/s) pushes risk UP by {discharge_contribution:.2f}")
        else:
            explanation_text.append(f"Discharge ({avg_discharge:.1f}m³/s) pushes risk DOWN by {abs(discharge_contribution):.2f}")
        
        if precipitation_contribution > 0:
            explanation_text.append(f"Precipitation ({avg_precipitation:.1f}mm) pushes risk UP by {precipitation_contribution:.2f}")
        else:
            explanation_text.append(f"Precipitation ({avg_precipitation:.1f}mm) pushes risk DOWN by {abs(precipitation_contribution):.2f}")
        
        return {
            'type': 'SHAP',
            'values': shap_values,
            'explanation': explanation_text,
            'force_plot_data': {
                'base_value': base_value,
                'features': {
                    'Discharge': {'value': avg_discharge, 'impact': discharge_contribution},
                    'Precipitation': {'value': avg_precipitation, 'impact': precipitation_contribution}
                }
            }
        }
    
    def create_combined_explanation(self, discharge_seq, precipitation_seq, risk_code, probabilities):
        """
        Create complete explanation combining SHAP and LIME
        
        Args:
            discharge_seq: Input discharge sequence
            precipitation_seq: Input precipitation sequence
            risk_code: Predicted risk code
            probabilities: Probability distribution
        
        Returns:
            dict with all explanation data
        """
        
        # Generate visualizations
        sequence_viz = self.create_sequence_visualization(discharge_seq, precipitation_seq)
        
        # Calculate feature importance for the sequence
        feature_importance = [
            np.std(precipitation_seq),  # Precipitation variability as importance
            np.std(discharge_seq)  # Discharge variability as importance
        ]
        feature_importance = np.array(feature_importance) / np.max(feature_importance)
        
        importance_viz = self.create_feature_importance_plot(
            feature_importance,
            ['Precipitation', 'Discharge']
        )
        
        confidence_viz = self.create_prediction_confidence_plot(probabilities)
        
        # Generate SHAP and LIME explanations
        shap_exp = self.generate_shap_explanation(discharge_seq, precipitation_seq, risk_code)
        lime_exp = self.generate_lime_explanation(discharge_seq, precipitation_seq, risk_code)
        
        return {
            'shap': shap_exp,
            'lime': lime_exp,
            'visualizations': {
                'sequence': sequence_viz,
                'importance': importance_viz,
                'confidence': confidence_viz
            },
            'timestamp': datetime.now().isoformat(),
            'summary': f"The model predicts {self.risk_labels[risk_code]} risk with "
                      f"{probabilities.get(risk_code, 0):.1f}% confidence based on "
                      f"discharge and precipitation patterns."
        }

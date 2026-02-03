import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import joblib
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class LSTMFloodPredictor:
    def __init__(self, model_dir='static/model'):
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.timesteps = 7
        self.feature_scaler = None
        
    def load_and_prepare_data(self, filepath):
        """Load and preprocess the dataset"""
        print(f"Loading dataset from {filepath}...")
        df = pd.read_excel(filepath)
        
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)
        
        print(f"Dataset shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print(f"\nFirst few rows:")
        print(df.head())
        print(f"\nFlood risk distribution:")
        print(df['flood_risk_code'].value_counts().sort_index())
        
        return df
    
    def create_sequences(self, data, labels, timesteps=7):
        """Create sequences for LSTM"""
        X, y = [], []
        for i in range(len(data) - timesteps):
            X.append(data[i:(i + timesteps)])
            y.append(labels[i + timesteps])
        return np.array(X), np.array(y)
    
    def prepare_features(self, df):
        """Prepare features for LSTM"""
        # Select features for prediction
        feature_cols = ['discharge', 'precipitation']
        
        # Normalize features
        self.feature_scaler = MinMaxScaler()
        features_scaled = self.feature_scaler.fit_transform(df[feature_cols].fillna(0))
        
        # Extract target
        y = df['flood_risk_code'].values
        
        # Label encode the target
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Create sequences
        X, y_seq = self.create_sequences(features_scaled, y_encoded, self.timesteps)
        
        print(f"\nSequences created:")
        print(f"X shape: {X.shape}")
        print(f"y shape: {y_seq.shape}")
        print(f"Risk classes: {self.label_encoder.classes_}")
        
        return X, y_seq
    
    def build_model(self, input_shape):
        """Build LSTM model"""
        print("\nBuilding LSTM model...")
        model = Sequential([
            LSTM(64, return_sequences=True, activation='relu', input_shape=input_shape),
            Dropout(0.2),
            LSTM(32, return_sequences=False, activation='relu'),
            Dropout(0.2),
            Dense(16, activation='relu'),
            Dropout(0.1),
            Dense(4, activation='softmax')
        ])
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        model.summary()
        return model
    
    def train(self, dataset_path):
        """Train the LSTM model"""
        # Load data
        df = self.load_and_prepare_data(dataset_path)
        
        # Prepare features
        X, y = self.prepare_features(df)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"\nTrain set size: {X_train.shape}")
        print(f"Test set size: {X_test.shape}")
        
        # Build and train model
        input_shape = (X_train.shape[1], X_train.shape[2])
        self.model = self.build_model(input_shape)
        
        print("\nTraining model...")
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_test, y_test),
            epochs=50,
            batch_size=32,
            verbose=1
        )
        
        # Evaluate
        print("\nEvaluating model...")
        y_pred = np.argmax(self.model.predict(X_test), axis=1)
        
        accuracy = accuracy_score(y_test, y_pred)
        print(f"\nTest Accuracy: {accuracy:.4f}")
        
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        print("\nClassification Report:")
        print(classification_report(
            y_test, y_pred,
            target_names=self.label_encoder.classes_.astype(str)
        ))
        
        # Save model
        self.save_model()
        
        return history, accuracy
    
    def save_model(self):
        """Save trained model and preprocessing objects"""
        print(f"\nSaving model to {self.model_dir}...")
        
        model_path = os.path.join(self.model_dir, 'flood_lstm_model.h5')
        self.model.save(model_path)
        
        scaler_path = os.path.join(self.model_dir, 'feature_scaler.pkl')
        joblib.dump(self.feature_scaler, scaler_path)
        
        le_path = os.path.join(self.model_dir, 'label_encoder.pkl')
        joblib.dump(self.label_encoder, le_path)
        
        print(f"Model saved to {model_path}")
        print(f"Scaler saved to {scaler_path}")
        print(f"Label encoder saved to {le_path}")
    
    def load_model(self):
        """Load trained model"""
        model_path = os.path.join(self.model_dir, 'flood_lstm_model.h5')
        scaler_path = os.path.join(self.model_dir, 'feature_scaler.pkl')
        le_path = os.path.join(self.model_dir, 'label_encoder.pkl')
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")
        
        self.model = keras.models.load_model(model_path)
        self.feature_scaler = joblib.load(scaler_path)
        self.label_encoder = joblib.load(le_path)
        
        print("Model loaded successfully")
    
    def predict(self, data_sequence):
        """Make prediction on sequence"""
        # data_sequence should be shape (timesteps, features)
        if data_sequence.shape != (self.timesteps, 2):
            raise ValueError(f"Expected shape ({self.timesteps}, 2), got {data_sequence.shape}")
        
        data_scaled = self.feature_scaler.transform(data_sequence)
        X = np.expand_dims(data_scaled, axis=0)
        
        prediction = self.model.predict(X, verbose=0)
        risk_code = np.argmax(prediction[0])
        confidence = float(np.max(prediction[0]))
        
        return risk_code, confidence, prediction[0]


if __name__ == "__main__":
    # Path to your dataset
    dataset_path = '/Users/macbookpro2017/Downloads/floodriskvs/cleaned_prepared_data.xlsx'
    
    # Train the model
    trainer = LSTMFloodPredictor(model_dir='static/model')
    history, accuracy = trainer.train(dataset_path)
    
    print("\n" + "="*50)
    print("TRAINING COMPLETED SUCCESSFULLY")
    print("="*50)

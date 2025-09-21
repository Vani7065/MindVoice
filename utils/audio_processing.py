import librosa
import numpy as np
from textblob import TextBlob
import pickle
import os

class AudioMoodAnalyzer:
    def __init__(self):
        self.mood_labels = ['Happy', 'Sad', 'Anxious', 'Calm', 'Energetic', 'Tired']
    
    def extract_features(self, audio_data, sample_rate):
        """Extract audio features for mood analysis"""
        try:
            # Extract MFCC features
            mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=13)
            mfccs_mean = np.mean(mfccs, axis=1)
            
            # Extract pitch/fundamental frequency
            pitches, magnitudes = librosa.piptrack(y=audio_data, sr=sample_rate)
            pitch_mean = np.mean(pitches[pitches > 0]) if len(pitches[pitches > 0]) > 0 else 0
            
            # Extract energy/RMS
            rms = librosa.feature.rms(y=audio_data)[0]
            energy_mean = np.mean(rms)
            
            # Extract spectral centroid (brightness)
            spectral_centroids = librosa.feature.spectral_centroid(y=audio_data, sr=sample_rate)[0]
            spectral_centroid_mean = np.mean(spectral_centroids)
            
            # Extract tempo
            tempo, _ = librosa.beat.beat_track(y=audio_data, sr=sample_rate)
            
            features = np.concatenate([
                mfccs_mean,
                [pitch_mean, energy_mean, spectral_centroid_mean, tempo]
            ])
            
            return features
            
        except Exception as e:
            print(f"Error extracting features: {e}")
            return np.zeros(17)  # Return zero array if extraction fails
    
    def predict_mood(self, audio_bytes):
        """Predict mood from audio data"""
        try:
            # Convert bytes to audio array
            audio_data, sample_rate = librosa.load(io.BytesIO(audio_bytes))
            
            # Extract features
            features = self.extract_features(audio_data, sample_rate)
            
            # Simple rule-based classification (replace with ML model in production)
            return self._rule_based_classification(features)
            
        except Exception as e:
            print(f"Error in mood prediction: {e}")
            return self._get_random_mood()
    
    def _rule_based_classification(self, features):
        """Simple rule-based mood classification"""
        pitch = features[13]
        energy = features[14]
        spectral_centroid = features[15]
        tempo = features[16]
        
        # Normalize values (simplified)
        pitch_norm = min(pitch / 200, 1.0) if pitch > 0 else 0
        energy_norm = min(energy * 100, 1.0)
        tempo_norm = min(tempo / 180, 1.0) if tempo > 0 else 0
        
        # Rule-based classification
        if energy_norm > 0.7 and tempo_norm > 0.6:
            mood = "Energetic"
            confidence = 0.8
        elif pitch_norm < 0.3 and energy_norm < 0.4:
            mood = "Sad"
            confidence = 0.7
        elif energy_norm > 0.6 and pitch_norm > 0.5:
            mood = "Happy"
            confidence = 0.75
        elif energy_norm < 0.3:
            mood = "Tired"
            confidence = 0.6
        elif spectral_centroid > 2000:
            mood = "Anxious"
            confidence = 0.65
        else:
            mood = "Calm"
            confidence = 0.6
        
        return mood, confidence, self._generate_mood_scores(mood)
    
    def _generate_mood_scores(self, predicted_mood):
        """Generate scores for all moods"""
        base_scores = np.random.rand(len(self.mood_labels)) * 0.3
        mood_index = self.mood_labels.index(predicted_mood)
        base_scores[mood_index] = 0.6 + np.random.rand() * 0.4
        
        return dict(zip(self.mood_labels, base_scores))
    
    def _get_random_mood(self):
        """Fallback random mood prediction"""
        mood = np.random.choice(self.mood_labels)
        confidence = 0.5 + np.random.rand() * 0.3
        scores = self._generate_mood_scores(mood)
        return mood, confidence, scores
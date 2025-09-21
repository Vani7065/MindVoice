from textblob import TextBlob
import re
import numpy as np

class TextMoodAnalyzer:
    def __init__(self):
        self.emotion_keywords = {
            'happy': ['happy', 'joy', 'excited', 'great', 'amazing', 'wonderful', 'fantastic', 'love', 'excellent'],
            'sad': ['sad', 'depressed', 'down', 'miserable', 'awful', 'terrible', 'horrible', 'crying', 'tears'],
            'angry': ['angry', 'mad', 'furious', 'irritated', 'annoyed', 'frustrated', 'hate', 'rage'],
            'anxious': ['anxious', 'worried', 'nervous', 'scared', 'afraid', 'panic', 'stress', 'overwhelmed'],
            'calm': ['calm', 'peaceful', 'relaxed', 'serene', 'tranquil', 'content', 'balanced'],
            'tired': ['tired', 'exhausted', 'sleepy', 'drained', 'weary', 'fatigue']
        }
    
    def analyze_text_mood(self, text):
        """Comprehensive text mood analysis"""
        # Basic sentiment analysis using TextBlob
        blob = TextBlob(text.lower())
        polarity = blob.sentiment.polarity  # -1 (negative) to 1 (positive)
        subjectivity = blob.sentiment.subjectivity  # 0 (objective) to 1 (subjective)
        
        # Keyword-based emotion detection
        emotion_scores = self._calculate_emotion_scores(text.lower())
        
        # Determine primary mood
        primary_mood = self._determine_primary_mood(polarity, emotion_scores)
        
        # Get appropriate emoji
        emoji = self._get_mood_emoji(primary_mood)
        
        # Calculate confidence based on keyword matches and polarity strength
        confidence = self._calculate_confidence(polarity, emotion_scores, text)
        
        return {
            'mood': primary_mood,
            'polarity': polarity,
            'subjectivity': subjectivity,
            'emoji': emoji,
            'confidence': confidence,
            'emotion_scores': emotion_scores
        }
    
    def _calculate_emotion_scores(self, text):
        """Calculate scores for different emotions based on keywords"""
        emotion_scores = {}
        words = re.findall(r'\b\w+\b', text)
        
        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for word in words if word in keywords)
            # Normalize by text length
            emotion_scores[emotion] = score / max(len(words), 1)
        
        return emotion_scores
    
    def _determine_primary_mood(self, polarity, emotion_scores):
        """Determine the primary mood from analysis"""
        # Find emotion with highest score
        if emotion_scores:
            max_emotion = max(emotion_scores, key=emotion_scores.get)
            max_score = emotion_scores[max_emotion]
            
            # If emotion score is significant, use it
            if max_score > 0.05:  # At least 5% of words are emotional
                return max_emotion.title()
        
        # Fall back to polarity-based classification
        if polarity > 0.1:
            return "Happy"
        elif polarity < -0.1:
            return "Sad"
        else:
            return "Neutral"
    
    def _get_mood_emoji(self, mood):
        """Get appropriate emoji for mood"""
        emoji_map = {
            'Happy': '😊',
            'Sad': '😢',
            'Angry': '😠',
            'Anxious': '😰',
            'Calm': '😌',
            'Tired': '😴',
            'Neutral': '😐'
        }
        return emoji_map.get(mood, '🤔')
    
    def _calculate_confidence(self, polarity, emotion_scores, text):
        """Calculate confidence score for the mood prediction"""
        # Base confidence on polarity strength
        polarity_confidence = abs(polarity)
        
        # Add confidence from emotion keywords
        max_emotion_score = max(emotion_scores.values()) if emotion_scores else 0
        keyword_confidence = min(max_emotion_score * 5, 1.0)  # Scale up keyword score
        
        # Text length factor (longer texts might be more reliable)
        length_factor = min(len(text.split()) / 50, 1.0)
        
        # Combine factors
        confidence = (polarity_confidence * 0.4 + keyword_confidence * 0.4 + length_factor * 0.2)
        
        return min(max(confidence, 0.3), 0.95)  # Clamp between 30% and 95%

class MoodInsights:
    @staticmethod
    def generate_insights(mood_history, journal_entries):
        """Generate personalized insights from mood data"""
        insights = []
        
        if not mood_history:
            return ["Start tracking your moods to get personalized insights!"]
        
        # Recent mood pattern
        recent_moods = [entry['mood'] for entry in mood_history[-7:]]
        if len(set(recent_moods)) == 1:
            insights.append(f"Your mood has been consistently {recent_moods[0].lower()} this week.")
        elif len(set(recent_moods)) > 5:
            insights.append("You've experienced a wide range of emotions this week - that's completely normal!")
        
        # Most common mood
        all_moods = [entry['mood'] for entry in mood_history]
        most_common = max(set(all_moods), key=all_moods.count)
        insights.append(f"Your most frequently recorded mood is {most_common.lower()}.")
        
        # Tracking consistency
        if len(mood_history) > 14:
            insights.append("Great job maintaining consistent mood tracking! This helps identify patterns.")
        
        # Journal analysis
        if journal_entries:
            avg_rating = np.mean([entry['mood_rating'] for entry in journal_entries])
            if avg_rating > 7:
                insights.append("Your journal entries show generally positive mood ratings!")
            elif avg_rating < 4:
                insights.append("Your recent journal entries suggest you might benefit from additional support.")
        
        return insights
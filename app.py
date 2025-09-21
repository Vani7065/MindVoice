import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import base64
from io import BytesIO

# Configure page
st.set_page_config(
    page_title="MindCare - Mental Health Support",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .tab-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #4A90E2;
        margin-bottom: 1rem;
    }
    .mood-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4A90E2;
        margin: 0.5rem 0;
    }
    .stButton > button {
        background: linear-gradient(90deg, #4A90E2, #50C878);
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .record-button {
        background: linear-gradient(90deg, #FF6B6B, #FF8E8E) !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 1rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'mood_history' not in st.session_state:
    st.session_state.mood_history = []
if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False
if 'current_mood' not in st.session_state:
    st.session_state.current_mood = "Neutral"
if 'mood_score' not in st.session_state:
    st.session_state.mood_score = 5

# Helper functions
def add_mood_entry(mood, score, notes="", voice_analysis=""):
    entry = {
        'timestamp': datetime.now(),
        'mood': mood,
        'score': score,
        'notes': notes,
        'voice_analysis': voice_analysis
    }
    st.session_state.mood_history.append(entry)

def get_mood_emoji(mood):
    mood_emojis = {
        "Very Happy": "😄",
        "Happy": "😊",
        "Neutral": "😐",
        "Sad": "😢",
        "Very Sad": "😭",
        "Anxious": "😰",
        "Angry": "😠",
        "Excited": "🤩",
        "Calm": "😌"
    }
    return mood_emojis.get(mood, "😐")

def simulate_voice_analysis():
    """Simulate voice mood analysis"""
    moods = ["Happy", "Sad", "Anxious", "Calm", "Excited", "Neutral"]
    confidence = np.random.uniform(75, 95)
    detected_mood = np.random.choice(moods)
    
    analysis = {
        "detected_mood": detected_mood,
        "confidence": confidence,
        "voice_features": {
            "pitch_variation": np.random.uniform(0.3, 0.8),
            "speech_rate": np.random.uniform(100, 200),
            "energy_level": np.random.uniform(0.2, 0.9)
        }
    }
    return analysis

# Main App Header
st.markdown('<h1 class="main-header">🧠 MindCare - Mental Health Support</h1>', unsafe_allow_html=True)

# Sidebar for quick actions
with st.sidebar:
    st.markdown("### 🎯 Quick Actions")
    
    # Current mood display
    st.markdown(f"""
    <div class="mood-card">
        <h3>Current Mood</h3>
        <h2>{get_mood_emoji(st.session_state.current_mood)} {st.session_state.current_mood}</h2>
        <p>Score: {st.session_state.mood_score}/10</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick mood buttons
    st.markdown("#### Quick Mood Log")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("😊 Good"):
            add_mood_entry("Happy", 7, "Quick log - feeling good")
            st.success("Mood logged!")
    with col2:
        if st.button("😢 Down"):
            add_mood_entry("Sad", 3, "Quick log - feeling down")
            st.success("Mood logged!")
    
    # Statistics
    if st.session_state.mood_history:
        st.markdown("### 📊 Quick Stats")
        avg_score = np.mean([entry['score'] for entry in st.session_state.mood_history])
        st.metric("Average Mood", f"{avg_score:.1f}/10")
        st.metric("Entries Today", len([e for e in st.session_state.mood_history 
                                      if e['timestamp'].date() == datetime.now().date()]))

# Main content tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎙️ Voice Mood Detection", 
    "📊 Mood Analyzer", 
    "📈 Mood Tracker", 
    "📝 Journal", 
    "🏥 Resources"
])

# Tab 1: Voice Mood Detection
with tab1:
    st.markdown('<h2 class="tab-header">🎙️ Voice Mood Detection</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Record Your Voice")
        st.markdown("Speak for 10-30 seconds about how you're feeling today. Our AI will analyze your voice patterns to detect your mood.")
        
        # Voice recorder simulation
        record_col1, record_col2, record_col3 = st.columns([1, 2, 1])
        with record_col2:
            if not st.session_state.is_recording:
                if st.button("🎤 Start Recording", key="start_record"):
                    st.session_state.is_recording = True
                    st.rerun()
            else:
                if st.button("⏹️ Stop Recording", key="stop_record"):
                    st.session_state.is_recording = False
                    # Simulate analysis
                    with st.spinner("Analyzing your voice..."):
                        time.sleep(2)
                        analysis = simulate_voice_analysis()
                        st.session_state.voice_analysis = analysis
                    st.rerun()
        
        # Recording status
        if st.session_state.is_recording:
            st.markdown("🔴 **Recording in progress...** Speak naturally about your feelings.")
            
            # Simulate audio waveform
            progress_bar = st.progress(0)
            for i in range(100):
                progress_bar.progress(i + 1)
                time.sleep(0.05)
    
    with col2:
        st.markdown("### 💡 Tips for Better Analysis")
        st.info("""
        - Speak naturally and clearly
        - Describe your current feelings
        - Mention recent events affecting you
        - Take 10-30 seconds minimum
        - Find a quiet environment
        """)
    
    # Display analysis results
    if hasattr(st.session_state, 'voice_analysis') and st.session_state.voice_analysis:
        st.markdown("### 🔍 Voice Analysis Results")
        
        analysis = st.session_state.voice_analysis
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Detected Mood", f"{get_mood_emoji(analysis['detected_mood'])} {analysis['detected_mood']}")
        with col2:
            st.metric("Confidence", f"{analysis['confidence']:.1f}%")
        with col3:
            mood_score = np.random.randint(1, 11)
            st.metric("Mood Score", f"{mood_score}/10")
        
        # Voice features
        st.markdown("#### Voice Pattern Analysis")
        feature_col1, feature_col2, feature_col3 = st.columns(3)
        
        with feature_col1:
            st.markdown(f"""
            <div class="metric-card">
                <strong>Pitch Variation</strong><br>
                {analysis['voice_features']['pitch_variation']:.2f}
            </div>
            """, unsafe_allow_html=True)
        
        with feature_col2:
            st.markdown(f"""
            <div class="metric-card">
                <strong>Speech Rate</strong><br>
                {analysis['voice_features']['speech_rate']:.0f} WPM
            </div>
            """, unsafe_allow_html=True)
        
        with feature_col3:
            st.markdown(f"""
            <div class="metric-card">
                <strong>Energy Level</strong><br>
                {analysis['voice_features']['energy_level']:.2f}
            </div>
            """, unsafe_allow_html=True)
        
        # Save analysis
        col1, col2 = st.columns([3, 1])
        with col1:
            notes = st.text_area("Add notes about this analysis:", key="voice_notes")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💾 Save Analysis"):
                add_mood_entry(
                    analysis['detected_mood'], 
                    mood_score, 
                    notes, 
                    f"Voice analysis - {analysis['confidence']:.1f}% confidence"
                )
                st.success("Analysis saved to your mood history!")

# Tab 2: Mood Analyzer
with tab2:
    st.markdown('<h2 class="tab-header">📊 Mood Analyzer</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Current Mood Assessment")
        
        # Mood selection
        mood_options = ["Very Happy", "Happy", "Neutral", "Sad", "Very Sad", "Anxious", "Angry", "Excited", "Calm"]
        selected_mood = st.selectbox("How are you feeling right now?", mood_options, 
                                   index=mood_options.index(st.session_state.current_mood))
        
        # Mood intensity slider
        mood_intensity = st.slider("Rate the intensity (1-10)", 1, 10, st.session_state.mood_score)
        
        # Factors affecting mood
        st.markdown("#### What's affecting your mood today?")
        factors = st.multiselect(
            "Select all that apply:",
            ["Work/Study", "Relationships", "Health", "Weather", "Sleep", "Exercise", "Social Media", 
             "News", "Finances", "Family", "Future Concerns", "Past Events"]
        )
        
        # Additional notes
        mood_notes = st.text_area("Additional thoughts or context:", 
                                placeholder="Describe what led to this mood or any other relevant details...")
        
        # Physical symptoms
        st.markdown("#### Physical Symptoms (if any)")
        symptoms = st.multiselect(
            "Select any physical symptoms you're experiencing:",
            ["Headache", "Fatigue", "Muscle tension", "Stomach issues", "Sleep problems", 
             "Appetite changes", "Restlessness", "Low energy", "None"]
        )
        
        if st.button("📊 Analyze & Save Mood"):
            # Update session state
            st.session_state.current_mood = selected_mood
            st.session_state.mood_score = mood_intensity
            
            # Create detailed notes
            detailed_notes = f"{mood_notes}\nFactors: {', '.join(factors) if factors else 'None specified'}\nSymptoms: {', '.join(symptoms) if symptoms else 'None'}"
            
            # Save to history
            add_mood_entry(selected_mood, mood_intensity, detailed_notes)
            
            st.success("Mood analysis saved successfully!")
    
    with col2:
        st.markdown("### 🎯 Mood Insights")
        
        # Current mood display
        st.markdown(f"""
        <div class="mood-card">
            <h3>Current Assessment</h3>
            <h2>{get_mood_emoji(selected_mood)} {selected_mood}</h2>
            <h3>Intensity: {mood_intensity}/10</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Recommendations based on mood
        if selected_mood in ["Very Sad", "Sad", "Anxious"]:
            st.warning("💙 **Self-Care Recommendations:**\n- Practice deep breathing\n- Reach out to a friend\n- Consider professional help\n- Try gentle exercise")
        elif selected_mood in ["Very Happy", "Happy", "Excited"]:
            st.success("🌟 **Great to hear you're doing well!**\n- Share your positivity\n- Engage in favorite activities\n- Plan for the future\n- Help others")
        else:
            st.info("😌 **Neutral mood suggestions:**\n- Try a new activity\n- Practice mindfulness\n- Connect with others\n- Set small goals")

# Tab 3: Mood Tracker
with tab3:
    st.markdown('<h2 class="tab-header">📈 Mood Tracker</h2>', unsafe_allow_html=True)
    
    if st.session_state.mood_history:
        # Create dataframe from mood history
        df = pd.DataFrame(st.session_state.mood_history)
        df['date'] = df['timestamp'].dt.date
        df['time'] = df['timestamp'].dt.strftime('%H:%M')
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            avg_score = df['score'].mean()
            st.metric("Average Mood Score", f"{avg_score:.1f}/10")
        with col2:
            total_entries = len(df)
            st.metric("Total Entries", total_entries)
        with col3:
            best_mood = df.loc[df['score'].idxmax()]['mood']
            st.metric("Best Mood Recorded", f"{get_mood_emoji(best_mood)} {best_mood}")
        with col4:
            days_tracked = df['date'].nunique()
            st.metric("Days Tracked", days_tracked)
        
        # Mood trend chart
        st.markdown("### 📈 Mood Trends")
        
        # Group by date for daily averages
        daily_mood = df.groupby('date')['score'].agg(['mean', 'count']).reset_index()
        daily_mood.columns = ['date', 'avg_score', 'entry_count']
        
        fig = px.line(daily_mood, x='date', y='avg_score', 
                     title='Daily Average Mood Score',
                     labels={'avg_score': 'Average Mood Score', 'date': 'Date'})
        fig.update_traces(line_color='#4A90E2', line_width=3)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Mood distribution
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🎭 Mood Distribution")
            mood_counts = df['mood'].value_counts()
            fig_pie = px.pie(values=mood_counts.values, names=mood_counts.index,
                           title="Distribution of Recorded Moods")
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("### ⏰ Mood by Time of Day")
            df['hour'] = df['timestamp'].dt.hour
            hourly_mood = df.groupby('hour')['score'].mean().reset_index()
            fig_bar = px.bar(hourly_mood, x='hour', y='score',
                           title="Average Mood Score by Hour",
                           labels={'hour': 'Hour of Day', 'score': 'Average Mood Score'})
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Recent entries table
        st.markdown("### 📋 Recent Mood Entries")
        recent_df = df.sort_values('timestamp', ascending=False).head(10)
        display_df = recent_df[['timestamp', 'mood', 'score', 'notes']].copy()
        display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        display_df['mood'] = display_df['mood'].apply(lambda x: f"{get_mood_emoji(x)} {x}")
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Export functionality
        if st.button("📥 Export Mood Data"):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="mood_data.csv">Download CSV file</a>'
            st.markdown(href, unsafe_allow_html=True)
    
    else:
        st.info("No mood data available yet. Start by recording your mood in the Voice Detection or Mood Analyzer tabs!")
        
        # Sample data button for demonstration
        if st.button("📊 Load Sample Data (Demo)"):
            # Generate sample mood data
            sample_dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
            sample_moods = ["Happy", "Sad", "Neutral", "Anxious", "Excited", "Calm"]
            
            for date in sample_dates:
                if np.random.random() > 0.3:  # 70% chance of entry per day
                    mood = np.random.choice(sample_moods)
                    score = np.random.randint(3, 9) if mood != "Very Sad" else np.random.randint(1, 5)
                    notes = f"Sample entry for {date.strftime('%Y-%m-%d')}"
                    
                    entry = {
                        'timestamp': date,
                        'mood': mood,
                        'score': score,
                        'notes': notes,
                        'voice_analysis': ""
                    }
                    st.session_state.mood_history.append(entry)
            
            st.success("Sample data loaded! Refresh to see your mood tracker.")
            st.rerun()

# Tab 4: Journal
with tab4:
    st.markdown('<h2 class="tab-header">📝 Digital Journal</h2>', unsafe_allow_html=True)
    
    # Journal entry form
    st.markdown("### ✍️ New Journal Entry")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        journal_title = st.text_input("Entry Title (optional)", placeholder="Today's thoughts...")
        journal_content = st.text_area("How was your day? What's on your mind?", 
                                      height=200,
                                      placeholder="Write about your experiences, thoughts, feelings, or anything else you'd like to remember...")
    
    with col2:
        st.markdown("#### 📝 Writing Prompts")
        prompts = [
            "What made me smile today?",
            "What challenged me today?",
            "What am I grateful for?",
            "What did I learn about myself?",
            "How did I handle stress?",
            "What are my goals for tomorrow?"
        ]
        
        selected_prompt = st.selectbox("Need inspiration?", ["Choose a prompt..."] + prompts)
        if selected_prompt != "Choose a prompt...":
            st.write(f"💭 *{selected_prompt}*")
    
    # Tags for categorization
    journal_tags = st.multiselect(
        "Add tags (optional):",
        ["Work", "Relationships", "Health", "Goals", "Gratitude", "Challenges", "Success", "Learning", "Travel", "Family"]
    )
    
    if st.button("💾 Save Journal Entry"):
        if journal_content.strip():
            entry = {
                'timestamp': datetime.now(),
                'title': journal_title or f"Journal Entry - {datetime.now().strftime('%Y-%m-%d')}",
                'content': journal_content,
                'tags': journal_tags
            }
            
            # Initialize journal entries if not exists
            if 'journal_entries' not in st.session_state:
                st.session_state.journal_entries = []
            
            st.session_state.journal_entries.append(entry)
            st.success("Journal entry saved!")
        else:
            st.error("Please write something before saving.")
    
    # Display previous entries
    if hasattr(st.session_state, 'journal_entries') and st.session_state.journal_entries:
        st.markdown("### 📖 Previous Entries")
        
        # Sort entries by date (newest first)
        sorted_entries = sorted(st.session_state.journal_entries, key=lambda x: x['timestamp'], reverse=True)
        
        for i, entry in enumerate(sorted_entries[:5]):  # Show last 5 entries
            with st.expander(f"{entry['title']} - {entry['timestamp'].strftime('%Y-%m-%d %H:%M')}"):
                st.write(entry['content'])
                if entry['tags']:
                    st.write(f"**Tags:** {', '.join(entry['tags'])}")
    else:
        st.info("No journal entries yet. Start writing your first entry above!")

# Tab 5: Resources
with tab5:
    st.markdown('<h2 class="tab-header">🏥 Mental Health Resources</h2>', unsafe_allow_html=True)
    
    # Emergency contacts
    st.error("""
    ### 🚨 Emergency Contacts
    If you're in crisis or having thoughts of self-harm:
    - **National Suicide Prevention Lifeline:** 988 (US)
    - **Crisis Text Line:** Text HOME to 741741
    - **Emergency Services:** 911
    - **International Crisis Lines:** [findahelpline.com](https://findahelpline.com)
    """)
    
    # Resource categories
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🧘 Self-Care Tools")
        
        st.info("""
        **Breathing Exercises**
        - 4-7-8 Breathing technique
        - Box breathing (4-4-4-4)
        - Diaphragmatic breathing
        
        **Mindfulness Apps**
        - Headspace
        - Calm
        - Insight Timer
        - Ten Percent Happier
        """)
        
        st.success("""
        **Physical Wellness**
        - Regular exercise routine
        - Adequate sleep (7-9 hours)
        - Balanced nutrition
        - Hydration tracking
        - Nature walks/outdoor time
        """)
    
    with col2:
        st.markdown("### 🏥 Professional Help")
        
        st.info("""
        **When to Seek Professional Help:**
        - Persistent sad or anxious mood
        - Loss of interest in activities
        - Significant changes in sleep/appetite
        - Difficulty concentrating
        - Thoughts of self-harm
        - Substance use concerns
        """)
        
        st.success("""
        **Types of Mental Health Professionals:**
        - Psychologists
        - Psychiatrists
        - Licensed therapists/counselors
        - Social workers
        - Support groups
        """)
    
    # Online resources
    st.markdown("### 🌐 Online Resources")
    
    resource_col1, resource_col2, resource_col3 = st.columns(3)
    
    with resource_col1:
        st.markdown("""
        **Educational Resources**
        - NAMI (National Alliance on Mental Illness)
        - Mental Health America
        - Psychology Today
        - WebMD Mental Health
        """)
    
    with resource_col2:
        st.markdown("""
        **Online Therapy Platforms**
        - BetterHelp
        - Talkspace
        - MDLIVE
        - Amwell
        """)
    
    with resource_col3:
        st.markdown("""
        **Support Communities**
        - 7 Cups (free emotional support)
        - Mental Health America online groups
        - NAMI Connection groups
        - Reddit mental health communities
        """)
    
    # Coping strategies
    st.markdown("### 🛠️ Coping Strategies")
    
    coping_strategies = {
        "Anxiety": [
            "Practice deep breathing exercises",
            "Use grounding techniques (5-4-3-2-1 method)",
            "Progressive muscle relaxation",
            "Limit caffeine intake",
            "Challenge negative thoughts"
        ],
        "Depression": [
            "Maintain a daily routine",
            "Engage in physical activity",
            "Connect with supportive people",
            "Practice gratitude journaling",
            "Set small, achievable goals"
        ],
        "Stress": [
            "Time management techniques",
            "Regular exercise",
            "Mindfulness meditation",
            "Healthy work-life balance",
            "Social support networks"
        ]
    }
    
    selected_strategy = st.selectbox("Choose a concern for specific strategies:", list(coping_strategies.keys()))
    
    if selected_strategy:
        st.markdown(f"**Strategies for {selected_strategy}:**")
        for strategy in coping_strategies[selected_strategy]:
            st.write(f"• {strategy}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>MindCare - Mental Health Support App</strong></p>
    <p>Remember: This app is for support and tracking purposes only. It does not replace professional medical advice, diagnosis, or treatment.</p>
    <p>If you're experiencing a mental health crisis, please contact emergency services or a mental health professional immediately.</p>
</div>
""", unsafe_allow_html=True)
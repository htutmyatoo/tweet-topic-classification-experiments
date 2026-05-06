import streamlit as st
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import time

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="TopicLens AI",
    page_icon="🐣",
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Custom CSS for a premium look and high header
st.markdown("""
    <style>
    /* Remove top padding to move header higher */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 0rem;
    }
    
    /* Hide the sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }

    .main { background-color: #f8f9fa; }
    .stTextArea textarea { border-radius: 10px; border: 1px solid #ddd; }
    .stButton>button { border-radius: 20px; width: 100%; font-weight: bold; background-color: #1DA1F2; color: white; border: none; }
    
    .prediction-card { 
        background-color: white; 
        padding: 2rem; 
        border-radius: 15px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
        text-align: center;
        border: 1px solid #f0f0f0;
    }
    
    .topic-title { font-size: 2rem; font-weight: 800; color: #1f77b4; margin-top: 10px;}
    
    .footer {
        position: relative;
        width: 100%;
        color: #888;
        text-align: center;
        padding: 20px;
        font-size: 0.9rem;
        margin-top: 50px;
        border-top: 1px solid #eee;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. APP INITIALIZATION & CACHING
# ==========================================
@st.cache_resource(show_spinner="Initializing NLP Engine...")
def initialize_app():
    for resource in ['stopwords', 'punkt', 'wordnet', 'punkt_tab']:
        nltk.download(resource, quiet=True)
    
    try:
        model = joblib.load('model/best_tweet_classifier.pkl') # model loading
        return model
    except FileNotFoundError:
        st.error("Model file 'best_tweet_classifier.pkl' not found.")
        return None

model = initialize_app()
lemmatizer = WordNetLemmatizer()
try:
    STOP_WORDS = set(stopwords.words('english'))
except:
    STOP_WORDS = set()

LABEL_MAP = {
    0: ('Arts & Culture', '🎨'),
    1: ('Business & Entrepreneurs', '💼'),
    2: ('Pop Culture', '🍿'),
    3: ('Daily Life', '☕'),
    4: ('Sports & Gaming', '⚽'),
    5: ('Science & Technology', '🔬')
}

# ==========================================
# 3. PREPROCESSING PIPELINE
# ==========================================
def preprocess_minimal(text):
    text = text.lower()
    text = re.sub(r'\{\{[^}]+\}\}', '', text)
    text = re.sub(r'\{@[^}]+@\}', '', text)
    return text.strip()

def preprocess_standard(text):
    text = preprocess_minimal(text)
    text = re.sub(r'http\S+|www\.\S+', '', text)
    text = re.sub(r'#(\w+)', r'\1', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in STOP_WORDS and len(t) > 1]
    return ' '.join(tokens)


# ==========================================
# 4. UI/UX LAYOUT
# ==========================================
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>🐣 TopicLens AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; margin-bottom: 30px;'>Intelligent Twitter Topic Classification Service</p>", unsafe_allow_html=True)

if "tweet_input" not in st.session_state:
    st.session_state.tweet_input = ""

def update_text_area():
    st.session_state.tweet_input = st.session_state.example_dropdown

# Two Column Layout
col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    st.subheader("1. Enter a Tweet")
    
    EXAMPLES = {
        "": "✨ Select an example...",
        "Just watched an incredible exhibition at the modern art museum, stunning!": "🎨 Arts & Culture",
        "The stock market is down again. Investors are pulling back from tech.": "💼 Business & Entrepreneurs",
        "Can't believe the season finale of that show. Mind blown.": "🍿 Pop Culture",
        "Had the best coffee this morning and now ready to tackle the day!": "☕ Daily Life",
        "Champions League final tomorrow. City vs Real Madrid!": "⚽ Sports & Gaming",
        "New research shows CRISPR gene editing can target cancer cells directly.": "🔬 Science & Technology"
    }
    
    st.selectbox(
        "💡 Try an example:", 
        options=list(EXAMPLES.keys()), 
        format_func=lambda text: f"{EXAMPLES[text]}" if text else EXAMPLES[text],
        key="example_dropdown", 
        on_change=update_text_area
    )

    user_text = st.text_area(
        "Or type your own tweet here:", 
        value=st.session_state.tweet_input,
        height=150, 
        placeholder="Type a tweet here to classify its topic..."
    )
    
    if user_text != st.session_state.tweet_input:
        st.session_state.tweet_input = user_text

    predict_button = st.button("🚀 Classify Tweet", type="primary")

with col2:
    st.subheader("2. Prediction Result")
    
    if predict_button:
        if not user_text.strip():
            st.warning("Please enter some text to classify.")
        elif model is None:
            st.error("Model is not loaded.")
        else:
            with st.spinner("Analyzing text..."):
                time.sleep(0.5) 
                cleaned_text = preprocess_standard(user_text)
                
                if not cleaned_text.strip():
                    st.warning("Input is too short after cleaning.")
                else:
                    prediction = model.predict([cleaned_text])[0]
                    topic_name, emoji = LABEL_MAP[prediction]
                    
                    st.markdown(f"""
                        <div class="prediction-card">
                            <div style="font-size: 4rem;">{emoji}</div>
                            <div style="color: #666; margin-top: 10px;">Predicted Category</div>
                            <div class="topic-title">{topic_name}</div>
                        </div><br>
                    """, unsafe_allow_html=True)
                    
                    st.success("Classification successful!")
                    with st.expander("Show processing details"):
                        st.code(cleaned_text)
    else:
        st.markdown("""
            <div class="prediction-card" style="background-color: #f1f3f5; border: 2px dashed #ccc; padding: 4rem 2rem;">
                <div style="font-size: 3rem; color: #aaa;">🔍</div>
                <div style="color: #888; margin-top: 10px;">Awaiting input...</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("""
    <div class="footer">
        <p> TopicLens AI © 2026 Htut Myat Oo</p>
        <p style="font-size: 0.8rem;">Built with Streamlit & Scikit-Learn | Linear SVM Model </p>
    </div>
""", unsafe_allow_html=True)
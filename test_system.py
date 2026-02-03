"""
Streamlit frontend for Trump Tweet Search Engine
"""

import streamlit as st
import requests
import pandas as pd
from typing import List, Dict

# Configuration
API_URL = "http://localhost:8000"

# Page config
st.set_page_config(
    page_title="Trump Tweet Search",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .tweet-card {
        background-color: rgba(200, 200, 200, 0.3);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .tweet-text {
        color: #222;
        font-size: 1rem;
        line-height: 1.6;
    }
    .score-badge {
        background-color: #1f77b4;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 5px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    .rank-number {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)


def check_api_health() -> bool:
    """Check if API is running"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def get_stats() -> Dict:
    """Get search engine statistics"""
    try:
        response = requests.get(f"{API_URL}/stats")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def search_tweets(query: str, top_k: int = 10) -> Dict:
    """Search for tweets"""
    try:
        response = requests.post(
            f"{API_URL}/search",
            json={"query": query, "top_k": top_k}
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Search failed: {response.json().get('detail', 'Unknown error')}")
            return None
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return None


# Main UI
st.markdown('<div class="main-header">Trump Tweet Search Engine</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Information Retrieval System using TF-IDF & Cosine Similarity</div>',
    unsafe_allow_html=True
)

# Check API status
if not check_api_health():
    st.error("WARNING: Backend API is not running! Please start the FastAPI server.")
    st.code("cd backend && uvicorn app.main:app --reload", language="bash")
    st.stop()

# Sidebar with stats
with st.sidebar:
    st.header("System Statistics")
    
    stats = get_stats()
    if stats:
        st.metric("Total Tweets", f"{stats['total_documents']:,}")
        st.metric("Vocabulary Size", f"{stats['vocabulary_size']:,}")
        st.metric("Max Features", stats['max_features'])
        
        with st.expander("About"):
            st.markdown("""
            This system uses:
            - **TF-IDF** for document representation
            - **Cosine Similarity** for relevance ranking
            - **spaCy** for text preprocessing
            - Dataset: Donald Trump tweets (2019)
            """)
    else:
        st.warning("Unable to fetch statistics")
    
    st.divider()
    
    # Settings
    st.header("Settings")
    top_k = st.slider("Number of results", min_value=1, max_value=50, value=10)

# Main search interface
st.header("Search Tweets")

# Search input
col1, col2 = st.columns([4, 1])
with col1:
    query = st.text_input(
        "Enter search query",
        placeholder="e.g., immigration policy, economy, foreign affairs...",
        label_visibility="collapsed"
    )
with col2:
    search_button = st.button("Search", type="primary", use_container_width=True)

# Perform search
if search_button or (query and len(query) > 0):
    if not query:
        st.warning("Please enter a search query")
    else:
        with st.spinner("Searching..."):
            results = search_tweets(query, top_k)
        
        if results and results.get('results'):
            st.success(f"Found {results['total_results']} relevant tweets")
            
            # Display results
            st.divider()
            
            for result in results['results']:
                with st.container():
                    # Score badge
                    st.markdown(
                        f'<span class="score-badge">Rank #{result["rank"]} • Score: {result["score"]:.3f}</span>',
                        unsafe_allow_html=True
                    )
                    
                    # Tweet text with better styling
                    st.markdown(
                        f'''<div class="tweet-card">
                            <div class="tweet-text">{result["tweet"]}</div>
                        </div>''',
                        unsafe_allow_html=True
                    )
                    
                    # Show cleaned tweet in expander
                    if result.get("cleaned_tweet"):
                        with st.expander("View preprocessed text"):
                            st.code(result["cleaned_tweet"], language="text")
            
            # Download results as CSV
            st.divider()
            df_results = pd.DataFrame(results['results'])
            csv = df_results.to_csv(index=False)
            st.download_button(
                label="Download results as CSV",
                data=csv,
                file_name=f"search_results_{query.replace(' ', '_')}.csv",
                mime="text/csv"
            )
            
        elif results and results['total_results'] == 0:
            st.info("No matching tweets found. Try different keywords.")
        else:
            st.error("Search failed. Please try again.")

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        Created by Ferdian Nur Fariza & Arsenio Farrell Winoto | A11.2023
    </div>
""", unsafe_allow_html=True)
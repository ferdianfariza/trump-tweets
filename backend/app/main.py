"""
FastAPI application for Trump Tweet Search Engine
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
from pathlib import Path

from .models import (
    SearchRequest, 
    SearchResponse, 
    SearchResult,
    StatsResponse,
    HealthResponse
)
from .search_engine import TweetSearchEngine
from .preprocessing import preprocess_batch

# Initialize FastAPI app
app = FastAPI(
    title="Trump Tweet Search API",
    description="Information Retrieval system for Donald Trump's tweets using TF-IDF",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Streamlit URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global search engine instance
search_engine = None
documents = []


@app.on_event("startup")
async def startup_event():
    """
    Load dataset and initialize search engine on startup
    """
    global search_engine, documents
    
    print("🚀 Starting Trump Tweet Search API...")
    
    try:
        # Path to dataset
        data_path = Path(__file__).parent.parent / "data" / "Donald-Tweets!.csv"
        
        if not data_path.exists():
            print(f"⚠️  Dataset not found at {data_path}")
            print("Please download the dataset and place it in backend/data/")
            return
        
        # Load dataset
        print(f"📂 Loading dataset from {data_path}")
        df_raw = pd.read_csv(data_path)
        
        # Get first 7000 tweets
        documents = df_raw['Tweet_Text'].dropna().tolist()[:7000]
        print(f"✓ Loaded {len(documents)} tweets")
        
        # Preprocess documents
        print("🔄 Preprocessing documents...")
        cleaned_docs = preprocess_batch(documents)
        print(f"✓ Preprocessing complete")
        
        # Initialize and fit search engine
        print("🔍 Initializing search engine...")
        search_engine = TweetSearchEngine(
            max_features=5000,
            min_df=2,
            max_df=0.8
        )
        search_engine.fit(documents, cleaned_docs)
        print("✓ Search engine ready!")
        
    except Exception as e:
        print(f"❌ Error during startup: {str(e)}")
        raise


@app.get("/", response_model=HealthResponse)
async def root():
    """
    Health check endpoint
    """
    if search_engine is None:
        return HealthResponse(
            status="initializing",
            message="Search engine is still loading..."
        )
    
    return HealthResponse(
        status="healthy",
        message="Trump Tweet Search API is running"
    )


@app.post("/search", response_model=SearchResponse)
async def search_tweets(request: SearchRequest):
    """
    Search for relevant tweets based on query
    
    Args:
        request (SearchRequest): Search query and parameters
        
    Returns:
        SearchResponse: Search results with scores and tweets
    """
    if search_engine is None:
        raise HTTPException(
            status_code=503,
            detail="Search engine not initialized. Please wait or check logs."
        )
    
    try:
        # Perform search
        results = search_engine.search(request.query, request.top_k)
        
        # Convert to response model
        search_results = [SearchResult(**result) for result in results]
        
        return SearchResponse(
            query=request.query,
            total_results=len(search_results),
            results=search_results
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )


@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """
    Get search engine statistics
    
    Returns:
        StatsResponse: Statistics about the search engine
    """
    if search_engine is None:
        raise HTTPException(
            status_code=503,
            detail="Search engine not initialized"
        )
    
    try:
        stats = search_engine.get_stats()
        return StatsResponse(**stats)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get stats: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """
    Simple health check
    """
    return {
        "status": "ok" if search_engine is not None else "loading",
        "total_tweets": len(documents) if documents else 0
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
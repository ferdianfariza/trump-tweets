"""
Pydantic models for request and response validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class SearchRequest(BaseModel):
    """Request model for search endpoint"""
    query: str = Field(..., description="Search query string", min_length=1)
    top_k: int = Field(default=5, description="Number of top results to return", ge=1, le=50)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "immigration policy",
                "top_k": 10
            }
        }


class SearchResult(BaseModel):
    """Model for individual search result"""
    rank: int = Field(..., description="Ranking position")
    score: float = Field(..., description="Cosine similarity score")
    tweet: str = Field(..., description="Original tweet text")
    cleaned_tweet: Optional[str] = Field(None, description="Preprocessed tweet text")


class SearchResponse(BaseModel):
    """Response model for search endpoint"""
    query: str = Field(..., description="Original query")
    total_results: int = Field(..., description="Number of results returned")
    results: List[SearchResult] = Field(..., description="List of search results")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "immigration policy",
                "total_results": 5,
                "results": [
                    {
                        "rank": 1,
                        "score": 0.85,
                        "tweet": "We need strong borders!",
                        "cleaned_tweet": "need strong border"
                    }
                ]
            }
        }


class StatsResponse(BaseModel):
    """Response model for stats endpoint"""
    total_documents: int = Field(..., description="Total number of tweets")
    vocabulary_size: int = Field(..., description="Size of vocabulary")
    tfidf_shape: tuple = Field(..., description="Shape of TF-IDF matrix")
    max_features: int = Field(..., description="Maximum features used")
    min_df: int = Field(..., description="Minimum document frequency")
    max_df: float = Field(..., description="Maximum document frequency")


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str = Field(..., description="Service status")
    message: str = Field(..., description="Status message")
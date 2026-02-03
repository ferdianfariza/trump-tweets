"""
Search engine module using TF-IDF and cosine similarity
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict
from .preprocessing import preprocess


class TweetSearchEngine:
    """
    Information Retrieval system for tweets using TF-IDF and cosine similarity
    """
    
    def __init__(self, max_features: int = 5000, min_df: int = 2, max_df: float = 0.8):
        """
        Initialize the search engine
        
        Args:
            max_features (int): Maximum number of features for TF-IDF
            min_df (int): Minimum document frequency
            max_df (float): Maximum document frequency
        """
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            min_df=min_df,
            max_df=max_df
        )
        self.tfidf_matrix = None
        self.documents = []
        self.cleaned_docs = []
        
    def fit(self, documents: List[str], cleaned_docs: List[str]):
        """
        Fit the TF-IDF vectorizer on cleaned documents
        
        Args:
            documents (List[str]): Original documents
            cleaned_docs (List[str]): Preprocessed documents
        """
        self.documents = documents
        self.cleaned_docs = cleaned_docs
        self.tfidf_matrix = self.vectorizer.fit_transform(cleaned_docs)
        
        print(f"✓ TF-IDF matrix shape: {self.tfidf_matrix.shape}")
        print(f"✓ Vocabulary size: {len(self.vectorizer.get_feature_names_out())}")
        
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for most relevant tweets based on query
        
        Args:
            query (str): Search query
            top_k (int): Number of top results to return
            
        Returns:
            List[Dict]: List of search results with scores and tweets
        """
        if self.tfidf_matrix is None:
            raise ValueError("Model not fitted yet. Call fit() first.")
        
        # Preprocess query
        query_clean = preprocess(query)
        
        # Transform query to TF-IDF vector
        query_vec = self.vectorizer.transform([query_clean])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        # Get top K results
        ranked_idx = similarities.argsort()[::-1][:top_k]
        
        # Format results
        results = []
        for rank, idx in enumerate(ranked_idx, 1):
            if similarities[idx] > 0:
                results.append({
                    "rank": rank,
                    "score": float(similarities[idx]),
                    "tweet": self.documents[idx],
                    "cleaned_tweet": self.cleaned_docs[idx]
                })
        
        return results
    
    def get_stats(self) -> Dict:
        """
        Get statistics about the search engine
        
        Returns:
            Dict: Statistics including vocab size, doc count, etc.
        """
        if self.tfidf_matrix is None:
            return {"status": "not fitted"}
        
        return {
            "total_documents": len(self.documents),
            "vocabulary_size": len(self.vectorizer.get_feature_names_out()),
            "tfidf_shape": self.tfidf_matrix.shape,
            "max_features": self.vectorizer.max_features,
            "min_df": self.vectorizer.min_df,
            "max_df": self.vectorizer.max_df
        }
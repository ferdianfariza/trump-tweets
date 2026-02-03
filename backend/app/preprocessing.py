"""
Text preprocessing module for tweet cleaning and normalization
"""

import re
import string
import spacy

# Load spaCy model globally
nlp = spacy.load("en_core_web_sm")


def preprocess(text: str) -> str:
    """
    Preprocess text by:
    - Lowercasing
    - Removing URLs, mentions, hashtags, numbers
    - Removing punctuation
    - Tokenization and lemmatization
    - Removing stopwords
    
    Args:
        text (str): Raw text to preprocess
        
    Returns:
        str: Cleaned and preprocessed text
    """
    # Convert to lowercase
    text = str(text).lower()
    
    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)
    
    # Remove mentions (@username)
    text = re.sub(r"@[A-Za-z0-9_]+", "", text)
    
    # Remove hashtags (#hashtag)
    text = re.sub(r"#[A-Za-z0-9_]+", "", text)
    
    # Remove numbers
    text = re.sub(r"\d+", "", text)
    
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()
    
    # Tokenization + lemmatization + stopword removal
    doc = nlp(text)
    tokens = [
        token.lemma_ 
        for token in doc 
        if not token.is_stop and len(token.text) > 2
    ]
    
    return " ".join(tokens)


def preprocess_batch(documents: list) -> list:
    """
    Preprocess a batch of documents
    
    Args:
        documents (list): List of raw text documents
        
    Returns:
        list: List of cleaned documents
    """
    return [preprocess(doc) for doc in documents]
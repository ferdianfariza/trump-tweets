# 🔍 Trump Tweet Search Engine

Information Retrieval System menggunakan Vector Space Model (TF-IDF) dan Cosine Similarity untuk mencari tweet Donald Trump yang relevan berdasarkan query.

## 👥 Tim Pengembang

- **Ferdian Nur Fariza** (A11.2023.15074)
- **Arsenio Farrell Winoto** (A11.2023.15065)

## 🎯 Tujuan

- Membangun sistem Information Retrieval sederhana menggunakan dataset tweet Donald Trump tahun 2019
- Implementasi preprocessing teks, pembobotan TF-IDF, dan penghitungan cosine similarity
- Memahami pola komunikasi politik dan pengelompokan pesan berdasarkan kesamaan makna

## 🏗️ Arsitektur

```
trump-tweet-search/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── main.py            # FastAPI application
│   │   ├── search_engine.py   # TF-IDF & cosine similarity
│   │   ├── preprocessing.py   # Text preprocessing
│   │   └── models.py          # Pydantic models
│   └── data/
│       └── Donald-Tweets!.csv # Dataset (download separately)
├── frontend/                   # Streamlit Frontend
│   └── app.py                 # Streamlit UI
├── requirements.txt
└── README.md
```

## 🚀 Setup & Installation

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd trump-tweet-search
```

### 2. Create Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Download Dataset

- Download dataset dari [Kaggle](https://www.kaggle.com/datasets/kingburrito666/better-donald-trump-tweets)
- Letakkan file `Donald-Tweets!.csv` di folder `backend/data/`

Atau gunakan kagglehub:

```python
import kagglehub
path = kagglehub.dataset_download("kingburrito666/better-donald-trump-tweets")
```

## 💻 Running the Application

### Backend (FastAPI)

```bash
cd backend
uvicorn app.main:app --reload
```

API akan berjalan di: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### Frontend (Streamlit)

Buka terminal baru:

```bash
cd frontend
streamlit run app.py
```

Frontend akan berjalan di: `http://localhost:8501`

## 📡 API Endpoints

### 1. Health Check

```bash
GET /
GET /health
```

### 2. Search Tweets

```bash
POST /search
```

Request body:

```json
{
  "query": "immigration policy",
  "top_k": 10
}
```

Response:

```json
{
  "query": "immigration policy",
  "total_results": 10,
  "results": [
    {
      "rank": 1,
      "score": 0.856,
      "tweet": "We need strong borders!",
      "cleaned_tweet": "need strong border"
    }
  ]
}
```

### 3. Get Statistics

```bash
GET /stats
```

Response:

```json
{
  "total_documents": 7000,
  "vocabulary_size": 5000,
  "tfidf_shape": [7000, 5000],
  "max_features": 5000,
  "min_df": 2,
  "max_df": 0.8
}
```

## 🔬 Teknologi yang Digunakan

### Backend

- **FastAPI** - Modern web framework untuk API
- **scikit-learn** - TF-IDF vectorization & cosine similarity
- **spaCy** - NLP preprocessing (tokenization, lemmatization)
- **pandas** - Data manipulation

### Frontend

- **Streamlit** - Interactive web interface
- **requests** - HTTP client untuk API calls

### Text Processing

- **TF-IDF (Term Frequency-Inverse Document Frequency)** - Document representation
- **Cosine Similarity** - Relevance ranking
- **Lemmatization** - Word normalization
- **Stopword Removal** - Noise reduction

## 🧪 Preprocessing Pipeline

1. **Lowercase conversion** - Normalisasi case
2. **URL removal** - Hapus link
3. **Mention removal** - Hapus @username
4. **Hashtag removal** - Hapus #hashtag
5. **Number removal** - Hapus angka
6. **Punctuation removal** - Hapus tanda baca
7. **Tokenization** - Pemisahan kata
8. **Lemmatization** - Normalisasi kata ke bentuk dasar
9. **Stopword removal** - Hapus kata umum (a, the, is, dll)

## 📊 Features

### Search Interface

- Real-time search dengan query input
- Adjustable number of results (1-50)
- Relevance score untuk setiap hasil
- View preprocessed text
- Download results as CSV

### Statistics Dashboard

- Total tweets dalam dataset
- Vocabulary size
- TF-IDF configuration parameters

## 🎨 Screenshots

(Tambahkan screenshots di sini setelah aplikasi berjalan)

## 📚 Referensi

- Dataset: [Better Donald Trump Tweets](https://www.kaggle.com/datasets/kingburrito666/better-donald-trump-tweets)
- [TF-IDF Vectorizer - scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
- [Cosine Similarity - scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html)
- [spaCy Documentation](https://spacy.io/)

## 🔮 Future Improvements

- [ ] Add caching untuk query yang sering dicari
- [ ] Implement pagination untuk hasil yang banyak
- [ ] Add advanced filters (date range, sentiment, etc)
- [ ] Deploy ke cloud (Heroku/Railway/Render)
- [ ] Add visualization (word clouds, topic modeling)
- [ ] Implement BM25 sebagai alternatif TF-IDF
- [ ] Add query expansion/suggestion

## 📝 License

This project is for educational purposes.

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

**Dibuat dengan ❤️ untuk mata kuliah Information Retrieval**

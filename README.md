# Trump Tweet Search Engine

So basically, this is a search engine that lets you dig through Donald Trump's tweets from 2019. I built it using TF-IDF and cosine similarity to find the most relevant tweets based on whatever you're searching for.

## Developers

- **Ferdian Nur Fariza**
- **Arsenio Farrell Winoto**

## How It's Organized

```
trump-tweet-search/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── main.py            # Main API application
│   │   ├── search_engine.py   # The search logic (TF-IDF stuff)
│   │   ├── preprocessing.py   # Text cleaning
│   │   └── models.py          # Data models
│   └── data/
│       └── Donald-Tweets!.csv # The tweet dataset (you need to download this)
├── frontend/                   # Streamlit Frontend
│   └── app.py                 # Web interface
├── requirements.txt
└── README.md
```

## Setup

### Clone Repo

```bash
git clone https://github.com/ferdianfariza/trump-tweets.git
cd trump-tweets
```

### Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate  # on Linux/Mac
# venv\Scripts\activate   # on Windows
```

### Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Get the Dataset

Visit this link [Kaggle](https://www.kaggle.com/datasets/kingburrito666/better-donald-trump-tweets) and download the dataset. Drop the `Donald-Tweets!.csv` file into `backend/data/`.

Or use kagglehub:

```python
import kagglehub
path = kagglehub.dataset_download("kingburrito666/better-donald-trump-tweets")
```

### Backend

```bash
cd backend
uvicorn app.main:app --reload
```

Your API should be running at `http://localhost:8000`. Check out the auto-generated docs at `http://localhost:8000/docs`.

### Frontend

Open another terminal and run:

```bash
cd frontend
streamlit run app.py
```

The web interface will pop up at `http://localhost:8501`.

## API

```bash
GET /health
```

```bash
POST /search
```

### Example:

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

```bash
GET /stats
```

## References

- Dataset came from [Kaggle](https://www.kaggle.com/datasets/kingburrito666/better-donald-trump-tweets)
- Used [scikit-learn's TF-IDF docs](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) as reference
- Same with [cosine similarity](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html)
- [spaCy docs](https://spacy.io/)

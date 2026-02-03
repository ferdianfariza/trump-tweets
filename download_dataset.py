"""
Script to download Trump tweets dataset from Kaggle
"""

import kagglehub
import shutil
from pathlib import Path

def download_dataset():
    """Download dataset and move to backend/data folder"""
    
    print("Downloading Trump tweets dataset from Kaggle...")
    
    try:
        # Download dataset
        path = kagglehub.dataset_download("kingburrito666/better-donald-trump-tweets")
        print(f"Dataset downloaded to: {path}")
        
        # Create data directory if it doesn't exist
        data_dir = Path(__file__).parent / "backend" / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Find the CSV file
        source_path = Path(path) / "Donald-Tweets!.csv"
        dest_path = data_dir / "Donald-Tweets!.csv"
        
        if source_path.exists():
            # Copy file to backend/data
            shutil.copy2(source_path, dest_path)
            print(f"Dataset copied to: {dest_path}")
            print(f"Ready to use")
        else:
            print(f"ERROR: CSV file not found in downloaded path")
            print(f"Please manually copy the dataset to: {data_dir}")
            
    except Exception as e:
        print(f"ERROR: Failed to download dataset: {str(e)}")
        print("\nAlternative: Download manually from:")
        print("https://www.kaggle.com/datasets/kingburrito666/better-donald-trump-tweets")
        print(f"Then place it in: backend/data/Donald-Tweets!.csv")

if __name__ == "__main__":
    download_dataset()
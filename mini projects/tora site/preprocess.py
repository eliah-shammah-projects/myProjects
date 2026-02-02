import json
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def clean_text(text):
    # Remove punctuation and special characters, keep Hebrew letters
    text = re.sub(r'[^\u0590-\u05FF\s]', '', text)  # Keep Hebrew range and spaces
    return text.strip()

def preprocess_data(json_file="verses_data.json"):
    # Load data
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Clean text
    df['clean_text'] = df['text'].apply(clean_text)
    
    # Tokenize (simple split for words)
    df['tokens'] = df['clean_text'].apply(lambda x: x.split())
    
    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(max_features=5000)  # Limit features for simplicity
    X = vectorizer.fit_transform(df['clean_text'])
    y = df['book_type']
    
    return X, y, vectorizer, df

if __name__ == "__main__":
    X, y, vectorizer, df = preprocess_data()
    print(f"Processed {len(df)} verses. TF-IDF shape: {X.shape}")
    # Optionally save vectorizer
    import joblib
    joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
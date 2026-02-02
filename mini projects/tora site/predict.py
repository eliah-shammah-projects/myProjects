import joblib
import numpy as np

# Load model and vectorizer
model = joblib.load("classification_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

def predict_verse(verse):
    # Clean verse (similar to preprocess)
    import re
    clean_verse = re.sub(r'[^\u0590-\u05FF\s]', '', verse).strip()
    
    # Vectorize
    X = vectorizer.transform([clean_verse])
    
    # Predict
    prediction = model.predict(X)[0]
    probabilities = model.predict_proba(X)[0]
    prob_dict = dict(zip(model.classes_, probabilities))
    
    # Top keywords: get top 5 features with highest coefficients for the predicted class
    class_idx = list(model.classes_).index(prediction)
    coef = model.coef_[class_idx]
    feature_names = vectorizer.get_feature_names_out()
    top_indices = np.argsort(coef)[-5:][::-1]  # Top 5
    top_keywords = [feature_names[i] for i in top_indices]
    
    return {
        "prediction": prediction,
        "probabilities": prob_dict,
        "top_keywords": top_keywords
    }

# Example usage
if __name__ == "__main__":
    sample_verse = "בראשית ברא אלהים את השמים ואת הארץ"  # Genesis 1:1
    result = predict_verse(sample_verse)
    print(f"This verse is most likely from: {result['prediction']} ({result['probabilities'][result['prediction']]*100:.1f}%)")
    print(f"Top keywords: {', '.join(result['top_keywords'])}")
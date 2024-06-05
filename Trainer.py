import os

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from joblib import dump


class ModelTrainer:
    def __init__(self):
        self.model = None
        self.vectorizer = TfidfVectorizer()

    def train_model(self, X_train, y_train):
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        self.model = MultinomialNB()
        self.model.fit(X_train_tfidf, y_train)

    def save_model(self, model_path):
        dump(self.model, model_path)
        print("Model został pomyślnie zapisany.")


data = pd.read_csv("opinie.csv", sep=';')

# Podział danych na cechy (X) i etykiety (y)
X = data["Opinia"]
y = data["Etykieta"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

trainer = ModelTrainer()

trainer.train_model(X_train, y_train)

if os.path.exists('model_naive_bayes.joblib'):
    os.remove('model_naive_bayes.joblib')
    print(f"File '{'model_naive_bayes.joblib'}' has been successfully removed.")
else:
    print(f"File '{'model_naive_bayes.joblib'}' does not exist.")

trainer.save_model('model_naive_bayes.joblib')

y_pred = trainer.model.predict(trainer.vectorizer.transform(X_test))

print("Dokładność:", accuracy_score(y_test, y_pred))
print("Raport klasyfikacji:\n", classification_report(y_test, y_pred, zero_division=1))

from joblib import load

from Trainer import trainer


class ModelPredictor:
    def __init__(self, model_path, vectorizer):
        self.model = load(model_path)
        self.vectorizer = vectorizer

    def predict(self, new_data):
        new_data_tfidf = self.vectorizer.transform(new_data)
        predictions = self.model.predict(new_data_tfidf)
        return predictions

# 0 - pozytywny
# 1 - negatywny
# 2 - neutralny

nowe_dane = ["Czy sztuczna inteligencja sprawi, że stanę się zbędny"]

# Wczytanie modelu i przewidywanie na nowych danych
predictor = ModelPredictor('model_naive_bayes.joblib', trainer.vectorizer)
predykcje = predictor.predict(nowe_dane)

# Wyświetlenie predykcji
print("Predykcje:", predykcje)

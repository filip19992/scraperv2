from joblib import load

from Trainer import trainer
import csv


class ModelPredictor:
    def __init__(self, model_path, vectorizer):
        self.model = load(model_path)
        self.vectorizer = vectorizer

    def predict(self, new_data):
        new_data_tfidf = self.vectorizer.transform(new_data)
        predictions = self.model.predict(new_data_tfidf)
        return predictions

    def read_csv(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Usunięcie znaków nowej linii z każdej linii i utworzenie listy zdań
        sentences = [line.strip() for line in lines]
        return  sentences

# 0 - pozytywny
# 1 - negatywny
# 2 - neutralny


# Wczytanie modelu i przewidywanie na nowych danych
predictor = ModelPredictor('model_naive_bayes.joblib', trainer.vectorizer)
nowe_dane = predictor.read_csv('output.csv')
print(nowe_dane)
predykcje = predictor.predict(nowe_dane)

# Wyświetlenie predykcji
print("Predykcje:", predykcje)

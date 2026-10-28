import os
import json
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

def run_train():
    data_path = os.path.join("data", "cosmeticos.json")
    if not os.path.exists(data_path):
        print(f"Arquivo {data_path} não encontrado.")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # Features (texto da descrição) e Target (categoria)
    X = df["descricao"]
    y = df["categoria"]

    # Pipeline: Vetorização de texto + Classificador
    model = Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True)),
        ("classifier", MultinomialNB())
    ])

    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    model_output = os.path.join("models", "classifier.joblib")
    joblib.dump(model, model_output)
    print(f"Modelo treinado e exportado com sucesso em: {model_output}")

if __name__ == "__main__":
    run_train()
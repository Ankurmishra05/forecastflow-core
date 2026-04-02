from src.data.ingestion import load_data
from src.features.build_features import create_features
from src.models.train import train_model
from src.models.evaluate import evaluate_model
import joblib
import os

def run_pipeline():
    df = load_data()
    df_features = create_features(df)

    y = df_features['Passengers']
    X = df_features.drop(columns=['Passengers'])

    train_size = len(df_features) - 12

    X_train = X.iloc[:train_size]
    X_test = X.iloc[train_size:]
    y_train = y.iloc[:train_size]
    y_test = y.iloc[train_size:]

    model = train_model(X_train, y_train, X_test, y_test)

    predictions = model.predict(X_test)

    metrics = evaluate_model(y_test, predictions)

    print("Model Performance:", metrics)

    # Save model
    os.makedirs("artifacts", exist_ok=True)
    joblib.dump(model, "artifacts/model.pkl")

    return model


if __name__ == "__main__":
    run_pipeline()
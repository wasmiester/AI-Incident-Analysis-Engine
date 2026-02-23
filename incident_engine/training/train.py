from sklearn.ensemble import IsolationForest

from incident_engine.training.dataset import load_metric_history
from incident_engine.training.model_store import save_model


def train():
    df = load_metric_history()

    if df.empty:
        raise RuntimeError("No metric history found for training")

    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42,
    )

    model.fit(df)

    save_model(model)
    print("Model trained and saved")


if __name__ == "__main__":
    train()

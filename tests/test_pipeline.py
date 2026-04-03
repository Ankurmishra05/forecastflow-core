import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from api import app as api_app


class DummyModel:
    def __init__(self):
        self.seen_features = None

    def predict(self, values):
        self.seen_features = values
        return [123.45]


class ApiPredictionTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(api_app.app)
        api_app.model = None

    def tearDown(self):
        api_app.model = None

    def test_build_feature_vector_matches_training_shape(self):
        features = api_app.build_feature_vector(
            prediction_date=api_app.date(1960, 1, 1),
            history=[float(i) for i in range(1, 15)],
        )

        self.assertEqual(features.shape, (1, 11))
        self.assertEqual(features[0, 6], 14.0)
        self.assertEqual(features[0, 7], 8.0)
        self.assertEqual(features[0, 8], 1.0)

    def test_predict_returns_prediction_when_model_is_available(self):
        dummy_model = DummyModel()

        with patch.object(api_app, "get_model", return_value=dummy_model):
            response = self.client.post(
                "/predict",
                json={
                    "date": "1960-01-01",
                    "last_values": [float(i) for i in range(1, 15)],
                },
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"prediction": 123.45})
        self.assertEqual(dummy_model.seen_features.shape, (1, 11))

    def test_predict_rejects_insufficient_history(self):
        response = self.client.post(
            "/predict",
            json={
                "date": "1960-01-01",
                "last_values": [380, 390, 400, 410, 420, 430, 440],
            },
        )

        self.assertEqual(response.status_code, 422)

    def test_predict_returns_503_when_model_is_missing(self):
        with patch("api.app.os.path.exists", return_value=False):
            response = self.client.post(
                "/predict",
                json={
                    "date": "1960-01-01",
                    "last_values": [float(i) for i in range(1, 15)],
                },
            )

        self.assertEqual(response.status_code, 503)
        self.assertIn("Model artifact is missing", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()

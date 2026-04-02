from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np

def evaluate_model(y_test, predictions):
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)

    return {
        "RMSE": rmse,
        "MAE": mae,
        "MSE": mse
    }
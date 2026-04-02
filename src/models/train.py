import xgboost as xgb

def train_model(X_train, y_train, X_test, y_test):
    model = xgb.XGBRegressor(
        n_estimators=1000,
        learning_rate=0.05,
        early_stopping_rounds=50,
        eval_metric='rmse'
    )

    model.fit(
        X_train,
        y_train,
        eval_set=[(X_test, y_test)],
        verbose=False
    )

    return model
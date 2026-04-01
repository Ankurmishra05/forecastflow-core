def create_features(df):
    df = df.copy()

    df['year'] = df.index.year
    df['month'] = df.index.month
    df['week_of_year'] = df.index.isocalendar().week.astype(int)
    df['day_of_year'] = df.index.dayofyear
    df['day_of_week'] = df.index.dayofweek
    df['is_weekend'] = (df.index.dayofweek >= 5).astype(int)

    df['lag_1'] = df['Passengers'].shift(1)
    df['lag_7'] = df['Passengers'].shift(7)
    df['lag_14'] = df['Passengers'].shift(14)

    df['rolling_mean_7'] = df['Passengers'].rolling(7).mean().shift(1)
    df['rolling_std_7'] = df['Passengers'].rolling(7).std().shift(1)

    df = df.dropna()

    return df
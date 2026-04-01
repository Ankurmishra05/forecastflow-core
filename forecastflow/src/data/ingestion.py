import pandas as pd

def load_data():
    url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/monthly-airline-passengers.csv"
    
    df = pd.read_csv(url, header=0, index_col=0, parse_dates=True)
    df.index.name = "Month"
    df.columns = ["Passengers"]
    
    return df
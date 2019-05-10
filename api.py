import numpy as np
import csv

def load_stock_data(symbol):
    prices = [[],[],[],[],[]]
    fname = f"./{symbol}.csv"
    with open(fname) as f:
        reader = csv.DictReader(f)
        for row in reader:
            prices[0].insert(0, float(row['open'].replace(',','')))
            prices[1].insert(0, float(row['close'].replace(',','')))
            prices[2].insert(0, float(row['high'].replace(',','')))
            prices[3].insert(0, float(row['low'].replace(',','')))
            prices[4].insert(0, float(row['volume'].replace(',','')))
    return np.array(prices)

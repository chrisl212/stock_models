import numpy as np
import json

def load_stock_data(symbol):
    prices = [[],[],[],[]]
    fname = f"../resources/stock_data/{symbol}_chart.json"
    json_data = json.load(open(fname))
    for day in json_data:
        if 'open' in day and 'close' in day and 'high' in day and 'low' in day:
            prices[0].append(day['open'])
            prices[1].append(day['close'])
            prices[2].append(day['high'])
            prices[3].append(day['low'])
    return np.array(prices)

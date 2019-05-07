import numpy as np
import json
import matplotlib.pyplot as plt

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

def smooth(data):
    alpha = 0.5
    smoothed = np.zeros(data.shape)
    for i in np.arange(0, data.shape[0]):
        if i == 0:
            smoothed[i] = data[i]
        else:
            smoothed[i] = alpha * data[i] + (1 - alpha) * smoothed[i-1]
    return smoothed

def rsi(data):
    strength = np.zeros(data[0].shape[0]-14)
    for i in np.arange(0, strength.shape[0]):
        opens = data[0][i:i+14]
        closes = data[1][i:i+14]
        change = closes - opens
        gains = sum(change[change > 0])/change[change > 0].shape[0]
        losses = abs(sum(change[change < 0]))/change[change < 0].shape[0]
        strength[i] = 100 * (1 - 1/(1 + gains/losses))
    return strength

def stoch(data):
    osc = np.zeros(data[0].shape[0]-14)
    for i in np.arange(0, osc.shape[0]):
        l14 = np.min(data[3][i:i+14])
        h14 = np.max(data[2][i:i+14])
        osc[i] = 100 * (data[1][i] - l14) / (h14 - l14)
    return osc

def will(data):
    williams = np.zeros(data[0].shape[0]-14)
    for i in np.arange(0, williams.shape[0]):
        l14 = np.min(data[3][i:i+14])
        h14 = np.max(data[2][i:i+14])
        williams[i] = -100 * (h14 - data[1][i]) / (h14 - l14)
    return williams

def ema(data, n):
    ret = np.zeros(data.shape[0]-n)
    ret[0] = np.mean(data[0:n])
    k = 2 / (n + 1)
    for i in np.arange(1, ret.shape[0]):
        ret[i] = k * data[i] + ret[i-1] * (1 - k)
    return ret

def macd(data):
    return ema(data[1],12)[14:] - ema(data[1],26)

def signalLine(data):
    return ema(macd(data),9)

def proc(data, n):
    ret = np.zeros(data.shape[0]-n)
    for i in np.arange(0, ret.shape[0]):
        ret[i] = (data[i+n] - data[i])/data[i]
    return ret

if __name__ == '__main__':
    prices = load_stock_data('AAPL')
    x = np.arange(0, prices[0].shape[0])
    smoothedPrices = np.array([smooth(prices[0]), smooth(prices[1]), smooth(prices[2]), smooth(prices[3])])
    RSI = rsi(smoothedPrices)
    stochastic = stoch(smoothedPrices)
    percent_r = will(smoothedPrices)
    MACD = macd(smoothedPrices)
    signal = signalLine(smoothedPrices)
    plt.plot(x, prices[0], 'r')
    plt.plot(x, smoothedPrices[0], 'b')
    plt.plot(x[14:], RSI, 'g')
    plt.plot(x[14:], stochastic, 'y')
    plt.plot(x[14:], percent_r, 'm')
    plt.plot(x[26:], MACD, 'c')
    plt.plot(x[35:], signal, 'r')
    plt.legend(['prices','smoothed','RSI','Stoch','%R','MACD','Sig'])
    plt.show()
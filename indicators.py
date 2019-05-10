import numpy as np

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
        if change[change > 0].shape[0] == 0:
            gains = 0
        else:
            gains = np.mean(change[change > 0])
        if change[change <= 0].shape[0] == 0:
            strength[i] = 100
        else:
            losses = np.abs(np.mean(change[change <= 0]))
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

def obv(data):
    ret = np.zeros(data[4].shape)
    ret[0] = data[4][0]
    for i in np.arange(1, ret.shape[0]):
        if data[1][i] > data[1][i-1]:
            ret[i] = ret[i-1] + data[4][i]
        elif data[1][i] < data[1][i-1]:
            ret[i] = ret[i-1] - data[4][i]
        else:
            ret[i] = ret[i-1]
    return ret
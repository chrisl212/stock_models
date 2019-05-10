import matplotlib.pyplot as plt
from indicators import *
from api import *
from sklearn.ensemble import RandomForestClassifier

if __name__ == '__main__':
    prices = load_stock_data('GOOGL')
    x = np.arange(0, prices[0].shape[0])
    smoothedPrices = np.array([smooth(prices[0]), smooth(prices[1]), smooth(prices[2]), smooth(prices[3]), smooth(prices[4])])
    RSI = rsi(smoothedPrices)
    stochastic = stoch(smoothedPrices)
    percent_r = will(smoothedPrices)
    MACD = macd(smoothedPrices)
    signal = signalLine(smoothedPrices)
    PROC = proc(smoothedPrices[1],1)
    OBV = obv(smoothedPrices)
    plt.plot(x, prices[0], 'r')
    plt.plot(x, smoothedPrices[0], 'b')
    # plt.plot(x, OBV, 'g')
    # plt.plot(x[1:], PROC, 'c')
    plt.plot(x[14:], RSI, 'g')
    plt.plot(x[14:], stochastic, 'y')
    plt.plot(x[14:], percent_r, 'm')
    plt.plot(x[26:], MACD, 'c')
    plt.plot(x[35:], signal, 'r')
    plt.legend(['prices','smoothed','RSI','Stoch','%R','MACD','Sig'])
    # plt.show()
    forest = RandomForestClassifier(n_estimators=65,criterion='gini',verbose=0,n_jobs=-1)
    training_cnt = 2000
    start = 35
    # period = 90
    features = np.array([RSI[21:-1], stochastic[21:-1], percent_r[21:-1], MACD[9:-1], signal[:-1], PROC[34:-1], OBV[35:-1]])
    test_features = features[:,:training_cnt]
    outputs = np.array(prices[1][1:] > prices[1][:-1]).astype(int)
    outputs[outputs == 0] -= 1
    forest.fit(test_features.T, outputs[start:start+training_cnt])
    test_features = features[:,training_cnt:]
    print(forest.score(test_features.T, outputs[start+training_cnt:]))
    # plt.plot(np.arange(0,outputs[training_cnt:].shape[0]), forest.predict(test_features.T))
    # plt.figure()
    # plt.plot(np.arange(0,outputs[training_cnt:].shape[0]), outputs[training_cnt:])
    # plt.show()
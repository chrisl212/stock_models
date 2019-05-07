import matplotlib.pyplot as plt
from indicators import *
from api import *

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
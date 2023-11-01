import os
import yfinance as yf
import pandas as pd
import tti.indicators

def saveToCSV(histo, filename):
    histo.to_csv(filename)

def loadFromCSV(filename):
    yfhisto = pd.read_csv(filename)
    datedf = pd.to_datetime(yfhisto['Date'], utc = True)
    yfhisto['Date'] = datedf
    yfhisto.set_index('Date', inplace = True)
    return yfhisto

def loadFromYF(ticker, period = '5y'):
    yfticker = yf.Ticker(ticker)
    return yfticker.history(period = period)

# @return current figure
def get_yfinance(isin_code, tmppath):
    filename = os.path.join(tmppath, f'{isin_code}.csv')
    if os.path.isfile(filename):
        print(f'{isin_code} from file')
        hist = loadFromCSV(filename)
    else:
        print(f'{isin_code} from internet')
        hist = loadFromYF(isin_code)
        if hist.size == 0:
            return None
        saveToCSV(hist, filename)

    indicator = tti.indicators.IchimokuCloud(hist)
    # print(f"Signal for {sys.argv[1]} : {indicator.getTiSignal()}")
    plt = indicator.getTiGraph()
    return plt.gcf()

import os, sys
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

def cleanIsInCache(tmppath, isin_code):
    filename = os.path.join(tmppath, f'{isin_code}.csv')
    if os.path.isfile(filename):
        try:
            os.remove(filename)
        except:
            print(f'Echec effacement {filename}')

# @param period 'D' Day, 'W' Week or 'M'Month
def convertHistToPeriod(hist, period):
    # hist is:
    # Open        High         Low       Close  Volume  Dividends  Stock Splits  Capital Gains
    # Date
    hist.reset_index(inplace=True)
    df = hist.groupby([pd.Grouper(key='Date', freq=period)])
    datelist=[]
    openlist=[]
    closelist=[]
    highlist=[]
    lowlist=[]
    volumelist = []
    dividendslist = []
    stocklist = []

    for elt in df:
        firstdate = elt[1].iloc[0]['Date']
        lastdate = elt[1].iloc[-1]['Date']
        thehigh = elt[1]['High'].max()
        thelow = elt[1]['Low'].min()
        theopen = elt[1].loc[elt[1]['Date'] == firstdate, 'Open'].iloc[0]
        theclose = elt[1].loc[elt[1]['Date'] == lastdate, 'Close'].iloc[0]

        thevolume = elt[1]['Volume'].sum()
        thedividends = elt[1]['Dividends'].sum()
        thestock = elt[1]['Stock Splits'].sum()

        datelist.append(firstdate)
        openlist.append(theopen)
        closelist.append(theclose)
        highlist.append(thehigh)
        lowlist.append(thelow)
        volumelist.append(thevolume)
        dividendslist.append(thedividends)
        stocklist.append(thestock)

    hist = pd.DataFrame({'Open':openlist, 'High':highlist,
        'Low':lowlist, 'Close':closelist, 'Volume':volumelist, 'Dividends':dividendslist,
        'Stock Splits':stocklist},
        index=datelist)
    hist.rename_axis("Date")

    return hist

# @param period 'D' for Day, 'W' for Week, 'M' for Month
# @param load_period period to load from yfinance '5y' = 5 years
# @return current figure
def get_yfinance(isin_code, nom, tmppath, period = 'D', load_period = '5y'):
    filename = os.path.join(tmppath, f'{isin_code}.csv')
    if os.path.isfile(filename):
        print(f'{isin_code} from file')
        hist = loadFromCSV(filename)
    else:
        print(f'{isin_code} from internet')
        hist = loadFromYF(isin_code, period = load_period)
        if hist.size == 0:
            return None
        saveToCSV(hist, filename)

    if period != 'D':
        # conversion des donnees
        hist = convertHistToPeriod(hist, period)

    if period == 'D':
        period_string = 'Jour'
    elif period == 'W':
        period_string = 'Semaine'
    elif period == 'M':
        period_string = 'Mois'
    else:
        period_string = 'période inconnue'

    indicator = tti.indicators.IchimokuCloud(hist)
    indicator._properties['long_name'] = f'{nom} \n {isin_code} - {period_string}'
    # print(f"Signal for {sys.argv[1]} : {indicator.getTiSignal()}")
    plt = indicator.getTiGraph()
    return plt.gcf()

# Afficher les childs d'un widget
def all_children(wid, finList=None, indent=0):
    finList = finList or []
    print(f"{'   ' * indent}{wid=}")
    children = wid.winfo_children()
    for item in children:
        finList.append(item)
        all_children(item, finList, indent + 1)
    return finList

def create_tickers_csv_sample(ticker_file):
    with open(ticker_file, "w") as fobj:
        fobj.write("QS0009080720,AMUNDI LABEL MONETAIRE ESR - F,ON\n")

def DEBUG_LINE():
    return sys._getframe(1).f_lineno

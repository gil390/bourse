import pandas as pd
import matplotlib.pyplot as plt
import sys
import tti.indicators

def loadFromCSV(filename):
    yfhisto = pd.read_csv(filename)
    datedf = pd.to_datetime(yfhisto['Date'], utc = True)
    yfhisto['Date'] = datedf
    yfhisto.set_index('Date', inplace = True)
    return yfhisto

def get(hist):
    indicator = tti.indicators.IchimokuCloud(hist)
    plt = indicator.getTiGraph()
    return plt.gcf()

df = loadFromCSV(sys.argv[1])
print(df.columns)
fig = get(df)
fig.suptitle("THE figure")
ax = fig.add_subplot()
plt.show()

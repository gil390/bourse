import sys, os
import csv
import yfinance as yf
import tti.indicators
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import *
from tkscrolledframe import ScrolledFrame

global_envdic = None

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

class STopLevel(Toplevel):
    def __init__(self, parent, isin, title):
        super().__init__(parent)
        self._isin = isin
        self.title(title)
        figure = self.figureCreate()
        canvas = FigureCanvasTkAgg(figure,
                               master = self)
        toolbar = NavigationToolbar2Tk(canvas,
                                   self)
        toolbar.update()
        canvas.get_tk_widget().pack(expand=1, fill="both")

    def figureCreate(self):
        # @TODO: global_envdic doit etre une classe singleton
        global global_envdic
        fig = get_yfinance(self._isin, global_envdic['tmp'])
        return fig

class SFrame(LabelFrame):
    def __init__(self, parent, figure, title, isin):
        super().__init__(parent, text = title)
        #self.configure(background='#FF0000')
        canvas = FigureCanvasTkAgg(figure,
                               master = self)
        toolbar = NavigationToolbar2Tk(canvas,
                                   self)
        toolbar.update()
        canvas.get_tk_widget().pack(expand=1, fill="both")

        self.bind('<Button-1>', lambda x: STopLevel(parent, isin, title))

class TheApp():
    def __init__(self, ticker_file):
        self._envdic = {
            "tmp" : os.environ['TMPDIR']
        }

        # @TODO a transformer en une classe singleton
        global global_envdic
        global_envdic = self._envdic

        self._window = Tk()
        self._window.resizable(True, True)

        self._window.title('Plotting in Tkinter')
        #self._window.geometry("1024x768")

        self.setMenuBar()

        # je force un backend qui n est pas Tk
        plt.switch_backend('agg')

        self._window.rowconfigure(0, weight=1)
        self._window.columnconfigure(0, weight=1)

        sf = ScrolledFrame(self._window)
        sf.grid(row = 0, column = 0, sticky = "NSEW")

        inner_frame = sf.display_widget(Frame)

        numfig = 0
        with open(ticker_file, newline = '') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                code, nom = row
                fig = get_yfinance(code, self._envdic['tmp'])
                if type(fig) != type(None):
                    sframe = SFrame(inner_frame, fig, f"{code} - {nom}", code)
                    sframe.grid(row = numfig // 2, column = numfig % 2, sticky = "NSEW", padx = 4, pady = 4)
                    numfig += 1
                else:
                    print(f'NO STOCK POUR {code}')

        self._window.mainloop()
        plt.close('all')

    def setMenuBar(self):
        menubar = Menu(self._window)
        self._window.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu.add_command(
            label='Exit',
            command=self._window.destroy
        )
        menubar.add_cascade(
            label="File",
            menu=filemenu
        )

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

TheApp('tickers.csv')

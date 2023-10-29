import sys
import csv
import yfinance as yf
import tti.indicators
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import *
from tkscrolledframe import ScrolledFrame

class SFrame(LabelFrame):
    def __init__(self, parent, figure, title):
        super().__init__(parent, text = title)
        #self.configure(background='#FF0000')
        canvas = FigureCanvasTkAgg(figure,
                               master = self)
        toolbar = NavigationToolbar2Tk(canvas,
                                   self)
        toolbar.update()
        canvas.get_tk_widget().pack(expand=1, fill="both")

class TheApp():
    def __init__(self, ticker_file):
        self._window = Tk()
        self._window.resizable(True, True)

        self._window.title('Plotting in Tkinter')
        #self._window.geometry("1024x768")

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
                fig = get_yfinance(code)
                if type(fig) != type(None):
                    sframe = SFrame(inner_frame, fig, f"{code} - {nom}")
                    sframe.grid(row = numfig // 2, column = numfig % 2, sticky = "NSEW", padx = 4, pady = 4)
                    numfig += 1
                else:
                    print(f'NO STOCK POUR {code}')

        self._window.mainloop()
        plt.close('all')

# @return current figure
def get_yfinance(isin_code):
    msft = yf.Ticker(isin_code)
    hist = msft.history(period="5y")
    if hist.size == 0:
        return None

    indicator = tti.indicators.IchimokuCloud(hist)
    # print(f"Signal for {sys.argv[1]} : {indicator.getTiSignal()}")
    plt = indicator.getTiGraph()
    return plt.gcf()

TheApp('tickers.csv')

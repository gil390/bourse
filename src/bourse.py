import sys
import yfinance as yf
import tti.indicators
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import *

class SFrame(Frame):
    def __init__(self, parent, figure):
        super().__init__(parent)
        self.configure(background='#FF0000')
        canvas = FigureCanvasTkAgg(figure,
                               master = self)
        toolbar = NavigationToolbar2Tk(canvas,
                                   self)
        toolbar.update()
        canvas.get_tk_widget().pack(expand=1, fill="both")

class TheApp():
    def __init__(self, isin_codes):
        self._window = Tk()
        self._window.resizable(True, True)
        self._window.columnconfigure(0, weight=1)

        self._window.title('Plotting in Tkinter')
        #self._window.geometry("1024x768")

        # je force un backend qui n est pas Tk
        plt.switch_backend('agg')

        print(type(isin_codes))
        therow = 0
        for code in isin_codes:
            self._window.rowconfigure(therow, weight=1)
            fig = get_yfinance(code)
            sframe = SFrame(self._window, fig)
            sframe.grid(row = therow, column = 0, sticky = "NSEW")
            therow += 1

        self._window.mainloop()
        plt.close('all')

# @return current figure
def get_yfinance(isin_code):
    msft = yf.Ticker(isin_code)
    hist = msft.history(period="5y")
    indicator = tti.indicators.IchimokuCloud(hist)
    # print(f"Signal for {sys.argv[1]} : {indicator.getTiSignal()}")
    plt = indicator.getTiGraph()
    return plt.gcf()

TheApp(sys.argv[1:])

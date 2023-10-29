import sys
import yfinance as yf
import tti.indicators
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import *

class TheApp():
    def __init__(self, argsobj):
        window = Tk()
        window.title('Plotting in Tkinter')
        window.geometry("1024x768")

        # je force un backend qui n est pas Tk
        plt.switch_backend('agg')

        get_yfinance(argsobj[1], None if len(argsobj) == 2 else argsobj[2])
        fig = plt.figure(num=1)
        canvas = FigureCanvasTkAgg(fig,
                               master = window)
        toolbar = NavigationToolbar2Tk(canvas,
                                   window)
        toolbar.update()
        canvas.get_tk_widget().pack()
        window.mainloop()
        plt.close('all')

def get_yfinance(isin_code, nom = None):
    subtitle = "Code: " + isin_code
    if type(nom) != type(None):
        subtitle += " Nom: " + nom

    msft = yf.Ticker(isin_code)
    hist = msft.history(period="5y")
    indicator = tti.indicators.IchimokuCloud(hist)
    # print(f"Signal for {sys.argv[1]} : {indicator.getTiSignal()}")
    plt = indicator.getTiGraph()
    plt.suptitle(subtitle)
    #plt.show()
    return plt

TheApp(sys.argv)

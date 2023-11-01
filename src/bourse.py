import sys, os
import csv
import yfinance as yf
import tti.indicators
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter as tk
import tkinter.ttk as ttk
import util_fcts
from tkscrolledframe import ScrolledFrame

global_envdic = None

class STopLevel(tk.Toplevel):
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
        fig = util_fcts.get_yfinance(self._isin, global_envdic['tmp'])
        return fig

class SFrame(ttk.LabelFrame):
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

        self._ticker_file = ticker_file
        self._stockFrames = []

        self._window = tk.Tk()
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

        self._inner_frame = sf.display_widget(ttk.Frame)

        self.loadStockTickers()

        self._window.mainloop()
        plt.close('all')

    def loadStockTickers(self):
        if self._stockFrames and len(self._stockFrames) > 0:
            self.delAllStockFrames()

        self._stockFrames = []
        numfig = 0
        with open(self._ticker_file, newline = '') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                code, nom = row
                fig = util_fcts.get_yfinance(code, self._envdic['tmp'])
                if type(fig) != type(None):
                    sframe = SFrame(self._inner_frame, fig, f"{code} - {nom}", code)
                    sframe.grid(row = numfig // 2, column = numfig % 2, sticky = "NSEW", padx = 4, pady = 4)
                    self._stockFrames.append(sframe)
                    numfig += 1
                else:
                    print(f'NO STOCK POUR {code}')

    def delAllStockFrames(self):
        for i in self._stockFrames:
            i.grid_forget()
            i.destroy()
        self._stockFrames=None
        plt.close('all')

    def setMenuBar(self):
        menubar = tk.Menu(self._window)
        self._window.config(menu=menubar)
        filemenu = tk.Menu(menubar)
        filemenu.add_command(
            label='Exit',
            command=self._window.destroy
        )
        filemenu.add_command(
            label='Widget Childs',
            command=lambda: util_fcts.all_children(self._window)
        )
        filemenu.add_command(
            label='Frame Forget',
            command=self.delAllStockFrames
        )
        filemenu.add_command(
            label='Load Tickers',
            command=self.loadStockTickers
        )
        menubar.add_cascade(
            label="File",
            menu=filemenu
        )

TheApp('tickers.csv')

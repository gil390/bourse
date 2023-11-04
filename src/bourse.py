import sys, os
import csv
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter as tk
import tkinter.ttk as ttk

import util_fcts
import sellistframe

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

        # pour chaque entree
        # 'frame': frame widget associe
        self._stockDic = {}

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

        self.loadStockTickersLazyFrame()

        self._window.mainloop()
        plt.close('all')
        self.saveCSV()

    def saveCSV(self):
        with open(self._ticker_file, 'w', newline='') as csvfile:
            owrite = csv.writer(csvfile)
            for isin in self._stockDic:
                nom = self._stockDic[isin]['nom']
                etat = "ON" if self._stockDic[isin]['state'] else "OFF"
                owrite.writerow([isin, nom, etat])

    def getIsinSFrame(self, parent, code, nom):
        sframe = None
        fig = util_fcts.get_yfinance(code, self._envdic['tmp'])
        if type(fig) != type(None):
            sframe = SFrame(parent, fig, f"{code} - {nom}", code)
            sframe.grid_forget()
        else:
            print(f'NO STOCK POUR {code}')
        return sframe

    def loadStockTickersLazyFrame(self):
        if len(self._stockDic) > 0:
            self.delAllStockFrame()

        with open(self._ticker_file, newline = '') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                code, nom, etat = row
                if type(etat) == type("") and etat.upper() == 'ON':
                    etat = True
                else:
                    etat = False

                if code not in self._stockDic:
                    sframe = None
                    if etat:
                        sframe = self.getIsinSFrame(self._inner_frame, code, nom)
                        if not sframe:
                            etat = False

                    self._stockDic[code] = {
                        'frame':sframe,
                        'state':etat,
                        'nom':nom
                    }
                else:
                    print(f'STOCK DEJA EN LISTE POUR {code}')
        self.refreshDisplay()

    def refreshDisplay(self):
        if len(self._stockDic) > 0:
            # Hide
            for i in self._stockDic:
                frame = self._stockDic[i]['frame']
                if frame:
                    frame.grid_forget()

            # show
            num = 0
            for i in self._stockDic:
                if self._stockDic[i]['state']:
                    if not self._stockDic[i]['frame']:
                        # Lazy load
                        code = i
                        nom = self._stockDic[i]['nom']
                        frame = self.getIsinSFrame(self._inner_frame, code, nom)
                        if frame:
                            self._stockDic[i]['frame'] = frame
                        else:
                            self._stockDic[i]['state'] = False
                            continue

                    sframe = self._stockDic[i]['frame']
                    sframe.grid(row = num // 2, column = num % 2, sticky = "NSEW", padx = 4, pady = 4)
                    num += 1

    def cleanAllIsinCache(self):
        for i in self._stockDic:
            util_fcts.cleanIsInCache(global_envdic['tmp'], i)
        self.delAllStockFrame()

    def delAllStockFrame(self):
        for i in self._stockDic:
            frame = self._stockDic[i]['frame']
            if frame:
                frame.grid_forget()
                frame.destroy()
                frame = None
            self._stockDic[i]['state'] = False
        plt.close('all')

    def switchVisiIsin(self, isin):
        if isin in self._stockDic:
            new_state = not self._stockDic[isin]['state']
            self._stockDic[isin]['state'] = new_state
            self.refreshDisplay()

    def dumpDic(self):
        for isin in self._stockDic:
            sframe = self._stockDic[isin]['frame']
            etat = self._stockDic[isin]['state']
            nom = self._stockDic[isin]['nom']
            print(f"{isin} / {etat} / {nom} / {sframe}")

    def setMenuBar(self):
        menulist = [
            ['Recharger tous ISIN', self.loadStockTickersLazyFrame],
            ['Selection ISIN', lambda: sellistframe.SelListWidget(self._window, self._stockDic,
                self.switchVisiIsin)],
            ['Effacer les fichiers en cache', self.cleanAllIsinCache],
            ['Exit', self._window.destroy],
        ]
        menubar = tk.Menu(self._window)
        self._window.config(menu=menubar)
        filemenu = tk.Menu(menubar)
        for i in menulist:
            filemenu.add_command(
                label=i[0],
                command= i[1]
            )
        menubar.add_cascade(
            label="File",
            menu=filemenu
        )

TheApp('tickers.csv')

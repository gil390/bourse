import sys, os
import csv
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter as tk
import tkinter.ttk as ttk
import utils
import sellistframe
import datetime
from tickerscsveditor import TickersCsvEditor

from tkscrolledframe import ScrolledFrame

class STopLevel(tk.Toplevel):
    def __init__(self, parent, isin, title, period='D'):
        super().__init__(parent)
        self._isin = isin
        self.title(title)
        figure = self.figureCreate(period)
        canvas = FigureCanvasTkAgg(figure,
                               master = self)
        toolbar = NavigationToolbar2Tk(canvas,
                                   self)
        toolbar.update()
        canvas.get_tk_widget().pack(expand=1, fill="both")

    def figureCreate(self, period):
        fig = utils.get_yfinance(self._isin, \
            utils.Config().get_temp_path(), period)
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


        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Semaine",
                                    command=lambda: STopLevel( \
                                    parent, isin, title + ' - Week', 'W'))
        self.popup_menu.add_command(label="Mois",
                                    command=lambda: STopLevel( \
                                    parent, isin, title + ' - Month', 'M'))

        self.bind('<Button-1>', lambda x: STopLevel(parent, isin, title))
        self.bind("<Button-3>", self.popup)

    def WeekShow(self):
        pass

    def MonthShow(self):
        pass

    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

class TheApp():
    def __init__(self):

        self._config = utils.Config()

        self._ticker_file = self._config.cfg("tickers_file_name")
        print(f'Tickers file : {self._ticker_file}')
        if not os.path.exists(self._ticker_file):
            # creation d un sample de fichier csv
            utils.create_tickers_csv_sample(self._ticker_file)

        # pour chaque entree
        # 'frame': frame widget associe
        self._stockDic = {}

        self._window = tk.Tk()
        self._window.resizable(True, True)
        w, h = self._window.winfo_screenwidth(), self._window.winfo_screenheight()
        self._window.geometry("%dx%d+0+0" % (w, h))

        self._window.title('Plotting in Tkinter')

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
        self._config.writeConfig()

    def saveCSV(self):
        with open(self._ticker_file, 'w', newline='') as csvfile:
            owrite = csv.writer(csvfile)
            for isin in self._stockDic:
                nom = self._stockDic[isin]['nom']
                etat = "ON" if self._stockDic[isin]['state'] else "OFF"
                owrite.writerow([isin, nom, etat])

    def getIsinSFrame(self, parent, code, nom):
        sframe = None
        fig = utils.get_yfinance(code, self._config.get_temp_path())
        if type(fig) != type(None):
            sframe = SFrame(parent, fig, f"{code} - {nom}", code)
            sframe.grid_forget()
        else:
            print(f'NO STOCK POUR {code}')
        return sframe

    def loadStockTickersLazyFrame(self):
        if len(self._stockDic) > 0:
            self.delAllStockFrame()

        self._stockDic={}

        with open(self._ticker_file, newline = '') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                code, nom, etat = row
                if type(etat) == type("") and etat.upper() == 'ON':
                    etat = True
                else:
                    etat = False

                # verification clean anciens fichiers ISIN CSV
                if self._config.cfg('auto_del_isin_csv') == True:
                    self.deloldisinfiles(code)

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
            utils.cleanIsInCache(self._config.get_temp_path(), i)
        self.loadStockTickersLazyFrame()

    def delAllStockFrame(self):
        for i in self._stockDic:
            frame = self._stockDic[i]['frame']
            if frame:
                frame.grid_forget()
                frame.destroy()
                self._stockDic[i]['frame'] = None
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
            ['Mise à jour ISIN', lambda: TickersCsvEditor(self._window, \
                self._ticker_file)],
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

    def deloldisinfiles(self, isin_code):
        today = datetime.date.today()

        for r, d, f in os.walk(self._config.get_temp_path()):
            for name in f:
                if isin_code.lower() in name.lower():
                    _, e = os.path.splitext(name)
                    if '.csv' == e.lower():
                        fname = os.path.join(r, name)
                        modifdate = os.path.getmtime(fname) # modifdate is a float
                        modifdate = datetime.date.fromtimestamp(modifdate)
                        if (today - modifdate).total_seconds() != 0:
                            os.remove(fname)

TheApp()

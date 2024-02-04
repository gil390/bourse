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
import traceback

from tickerscsveditor import TickersCsvEditor

from tkscrolledframe import ScrolledFrame

class STopLevel(tk.Toplevel):
    def __init__(self, parent, isin, title, period='D', load_period = '5y'):
        super().__init__(parent)
        self._isin = isin
        self.title(title)
        self._title = title
        figure = self.figureCreate(period, load_period)
        canvas = FigureCanvasTkAgg(figure,
                               master = self)
        toolbar = NavigationToolbar2Tk(canvas,
                                   self)
        toolbar.update()
        canvas.get_tk_widget().pack(expand=1, fill="both")
        self.attributes('-topmost', 'true')

    def figureCreate(self, period, loadperiod = '5y'):
        fig = utils.get_yfinance(self._isin, self._title, \
            utils.Config().get_temp_path(), period, loadperiod)
        return fig

class SFrame(ttk.LabelFrame):
    def __init__(self, parent, figure, title, isin, load_period):
        super().__init__(parent, text = title)
        #self.configure(background='#FF0000')
        canvas = FigureCanvasTkAgg(figure,
                               master = self)
        toolbar = NavigationToolbar2Tk(canvas,
                                   self)
        toolbar.update()
        canvas.get_tk_widget().pack(expand=1, fill="both")


        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Jour",
                                    command=lambda: STopLevel( \
                                    parent, isin, title + ' - Jour', 'D', \
                                    load_period))
        self.popup_menu.add_command(label="Semaine",
                                    command=lambda: STopLevel( \
                                    parent, isin, title + ' - Semaine', 'W', \
                                    load_period))
        self.popup_menu.add_command(label="Mois",
                                    command=lambda: STopLevel( \
                                    parent, isin, title + ' - Mois', 'M', \
                                    load_period))
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

        # pour debugger l'application
        self._exceptionlist = []

        self._fileIsModified = False
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

        try:
            self.loadStockTickersLazyFrame()
        except:
            self._exceptionlist.append(traceback.format_exc())
            sys.stderr.write(traceback.format_exc());

        self._window.mainloop()
        plt.close('all')
        self.saveCSV()
        self._config.writeConfig()

    def saveCSV(self):
        if self._fileIsModified:
            with open(self._ticker_file, 'w', newline='') as csvfile:
                owrite = csv.writer(csvfile)
                for isin in self._stockDic:
                    nom = self._stockDic[isin]['nom']
                    etat = "ON" if self._stockDic[isin]['state'] else "OFF"
                    periode = self._stockDic[isin]['periode']
                    owrite.writerow([isin, nom, etat, periode])
            self._fileIsModified = False

    def getIsinSFrame(self, parent, code, nom, periode):
        sframe = None
        fig = utils.get_yfinance(code, nom, self._config.get_temp_path(), \
            periode, self._config.cfg('load_period'))
        if type(fig) != type(None):
            sframe = SFrame(parent, fig, f"{code} - {nom}", code, \
             self._config.cfg('load_period'))
            sframe.grid_forget()
        else:
            print(f'NO STOCK POUR {code}')
        return sframe

    def exceptionWindow(self):
        utils.TopLvlWindow(self._window, "exception window", self._exceptionlist)

    def loadStockTickersLazyFrame(self):
        if len(self._stockDic) > 0:
            self.delAllStockFrame()

        self._stockDic={}

        with open(self._ticker_file, newline = '') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                code, nom, etat, periode = row
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
                        sframe = self.getIsinSFrame(self._inner_frame, \
                            code, nom, periode)
                        if not sframe:
                            etat = False

                    self._stockDic[code] = {
                        'frame':sframe,
                        'state':etat,
                        'nom':nom,
                        'periode':periode,
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
                        periode = self._stockDic[i]['periode']
                        frame = self.getIsinSFrame(self._inner_frame, \
                            code, nom, periode)
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
            self._fileIsModified = True

    def dumpDic(self):
        for isin in self._stockDic:
            sframe = self._stockDic[isin]['frame']
            etat = self._stockDic[isin]['state']
            nom = self._stockDic[isin]['nom']
            periode = self._stockDic[isin]['periode']
            print(f"{isin} / {etat} / {nom} / {sframe} / {periode}")

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

        debugmenulist = [
            ['Exception', self.exceptionWindow],
        ]

        menubar = tk.Menu(self._window)
        self._window.config(menu=menubar)
        filemenu = tk.Menu(menubar)
        for i in menulist:
            filemenu.add_command(
                label=i[0],
                command= i[1]
            )

        debugmenu = tk.Menu(menubar)
        for i in debugmenulist:
            debugmenu.add_command(
                label=i[0],
                command= i[1]
            )

        menubar.add_cascade(
            label="File",
            menu=filemenu
        )
        menubar.add_cascade(
            label="Debug",
            menu=debugmenu
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

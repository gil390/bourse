import tkinter as tk
import tkinter.ttk as ttk

class SelListFrame(tk.Frame):
    def __init__(self, master, text, state, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._var = tk.IntVar(master=self, value=state)
        self._button = ttk.Checkbutton(self, text = text,
            variable = self._var)
        self._button.pack()


class SelListWidget(tk.Toplevel):
    def __init__(self, parent, stockinfo, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        for isin in stockinfo:
            state = stockinfo[isin]['state']
            nom = f'{stockinfo[isin]["nom"]} (isin:{isin})'
            obj = SelListFrame(self, nom, state)
            obj.pack()

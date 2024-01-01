import tkinter as tk

####################################################################
class ScrollText(tk.Text):
    def __init__(self, parent):
        #self._f = tk.Frame(parent)
        myscrollY = tk.Scrollbar(parent, orient=tk.VERTICAL)
        myscrollY.pack(fill=tk.Y, side=tk.RIGHT)
        myscrollX = tk.Scrollbar(parent, orient=tk.HORIZONTAL)
        myscrollX.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Text.__init__(self, parent, yscrollcommand=myscrollY.set, xscrollcommand=myscrollX.set, wrap="none")
        myscrollY.config(command = self.yview)
        myscrollX.config(command = self.xview)

    def setTxt(self, arg):
        for l in arg:
            self.insert('end', l)

class TopLvlWindow(tk.Toplevel):
    def __init__(self, parent, title, linesarg):
        super().__init__(parent)
        self.title(title)

        self._frame = tk.Frame(self)
        self._stxt = ScrollText(self._frame)

        self._stxt.setTxt(linesarg)

        self._stxt.pack(expand=True, fill=tk.BOTH)
        self._frame.pack(expand=True, fill=tk.BOTH)
        tk.Button(self,
                text='Close',
                command=self.destroy).pack()
        self.attributes('-topmost', 'true')


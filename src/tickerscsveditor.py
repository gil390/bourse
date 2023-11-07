from tkinter import *
import tkinter.messagebox as tkMessageBox
import tkinter.filedialog as tkFileDialog
import tkinter.font as tkFont
import csv

##
# Copie de CSV GUI Editor written in python using tkinter
# - A lightweight csv editor
# - (c) 2017 Sebastian Safari ssebs@ymail.com
#
# Des ameliorations de code seraient a apporter
##

class TickersCsvEditorFrame(Frame):

    def __init__(self, master, csvfilename):
        super().__init__(master)
        self._csvfilename = csvfilename
        self._cellList = []
        self._currentCells = []
        self._currentCell = None

        self._width = 7
        self._height = 1

        self.grid()
        #self.createDefaultWidgets()
        self.loadCells()

        menubar = Menu(self)

        filemenu = Menu(menubar, tearoff=0)
        #filemenu.add_command(label="New", command=self.newCells)     # add save dialog
        # add save dialog
        #filemenu.add_command(label="Ouvrir", command=self.loadCells)
        filemenu.add_command(label="Sauvegarder", command=self.saveCells)
        filemenu.add_command(label="Ajouter une ligne", command=self.add_row)

        menubar.add_cascade(label="File", menu=filemenu)
        #menubar.add_command(label="Exit", command=self.quit)

        self.master.title('Tickers.csv Editor - Alt+Flèche pour changer de cellule')
        self.master.config(menu=menubar)

        default_font = tkFont.nametofont("TkTextFont")
        default_font.configure(family="Helvetica")

        self.option_add("*Font", default_font)

    def focus_tab(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def focus_sh_tab(self, event):
        event.widget.tk_focusPrev().focus()
        return "break"

    def focus_right(self, event):
        #event.widget.tk_focusNext().focus()
        widget = event.widget.focus_get()

        for i in range(len(self._currentCells)):
            for j in range(len(self._currentCells[0])):
                if widget == self._currentCells[i][j]:
                    if(j >= len(self._currentCells[0]) - 1 ):
                        j = -1
                    self._currentCells[i][j+1].focus()
        return "break"

    def focus_left(self, event):
        #event.widget.tk_focusNext().focus()
        widget = event.widget.focus_get()

        for i in range(len(self._currentCells)):
            for j in range(len(self._currentCells[0])):
                if widget == self._currentCells[i][j]:
                    if(j == 0):
                        j = len(self._currentCells[0])
                    self._currentCells[i][j-1].focus()
        return "break"

    def focus_up(self, event):
        #event.widget.tk_focusNext().focus()
        widget = event.widget.focus_get()

        for i in range(len(self._currentCells)):
            for j in range(len(self._currentCells[0])):
                if widget == self._currentCells[i][j]:
                    if(i < 0):
                        i = len(self._currentCells)
                    self._currentCells[i-1][j].focus()
        return "break"

    def focus_down(self, event):
        #event.widget.tk_focusNext().focus()
        widget = event.widget.focus_get()

        for i in range(len(self._currentCells)):
            for j in range(len(self._currentCells[0])):
                if widget == self._currentCells[i][j]:
                    if( i >= len(self._currentCells) - 1):
                        i = -1
                    self._currentCells[i+1][j].focus()
        return "break"

    def selectall(self, event):
        event.widget.tag_add("sel", "1.0", "end")
        event.widget.mark_set(INSERT, "1.0")
        event.widget.see(INSERT)
        return "break"

    def saveFile(self, event):
        self.saveCells()

    # TODO: Create bind for arrow keys and enter
    def createTitle(self, j, tmp):
        if j == 0:
            tmp.insert(1.0, "ISIN")
        elif j == 1:
            tmp.insert(1.0, "NOM")
        elif j == 2:
            tmp.insert(1.0, "ON/OFF")
        else:
            tmp.insert(1.0, "Periode (D,W,M)")
        tmp['state'] = DISABLED
        tmp.config(font=("Helvetica", 10, tkFont.BOLD))
        tmp.config(relief=FLAT, background = 'lightgray')

    def createDefaultWidgets(self):
        w, h = 7, 1
        self.sizeX = 4
        self.sizeY = 6
        defaultCells = []
        for i in range(self.sizeY):
            defaultCells.append([])
            for j in range(self.sizeX):
                defaultCells[i].append([])

        for i in range(self.sizeY):
            for j in range(self.sizeX):
                tmp = Text(self, width=w, height=h)
                tmp.bind("<Tab>", self.focus_tab)
                tmp.bind("<Shift-Tab>", self.focus_sh_tab)
                tmp.bind("<Return>", self.focus_down)
                tmp.bind("<Shift-Return>", self.focus_up)
                tmp.bind("<Alt-Right>", self.focus_right)
                tmp.bind("<Alt-Left>", self.focus_left)
                tmp.bind("<Alt-Up>", self.focus_up)
                tmp.bind("<Alt-Down>", self.focus_down)
                tmp.bind("<Control-s>", self.saveFile)

                if i > 0:
                    #TODO: Add resize check on column when changing focus
                    tmp.bind("<Control-a>", self.selectall)
                    tmp.insert(END, "")
                else:
                    self.createTitle(j, tmp)

                tmp.grid(padx=0, pady=0, column=j, row=i)

                defaultCells[i][j] = tmp
                self._cellList.append(tmp)

        defaultCells[1][0].focus_force()
        self._currentCells = defaultCells
        self._currentCell = self._currentCells[1][0]

        # TODO: Add buttons to create new rows/columns

    def newCells(self):
        self.removeCells()
        self.createDefaultWidgets()

    def removeCells(self):
        while(len(self._cellList) > 0):
            for cell in self._cellList:
                # print str(i) + str(j)
                cell.destroy()
                self._cellList.remove(cell)

    def add_row(self):
        self._currentCells.append([])
        for j in range(4):
            self._currentCells[-1].append([])
            tmp = Text(self, width=self._width, height=self._height)
            tmp.bind("<Tab>", self.focus_tab)
            tmp.bind("<Shift-Tab>", self.focus_sh_tab)
            tmp.bind("<Return>", self.focus_down)
            tmp.bind("<Shift-Return>", self.focus_up)
            tmp.bind("<Alt-Right>", self.focus_right)
            tmp.bind("<Alt-Left>", self.focus_left)
            tmp.bind("<Alt-Up>", self.focus_up)
            tmp.bind("<Alt-Down>", self.focus_down)
            tmp.bind("<Control-s>", self.saveFile)

            tmp.bind("<Control-a>", self.selectall)
            tmp.insert(END, "")

            tmp.grid(padx=0, pady=0, column=j, row= len(self._currentCells) - 1)

            self._cellList.append(tmp)
            self._currentCells[-1][j] = tmp

        self._currentCells[-1][0].focus_force()
        self._currentCell = self._currentCells[-1][0]

    def loadCells(self):
        filename = self._csvfilename
        #tkFileDialog.askopenfilename(initialdir=".", title="Select file",
        #                                        filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

        ary = []
        col = -1
        rows = []

        # get array size & get contents of rows
        with open(filename, "r") as csvfile:
            rd = csv.reader(csvfile, delimiter=",", quotechar='"')
            for row in rd:
                ary.append([])
                col = len(row)
                if col != 4:
                    print('ERROR tickers.csv file column error')
                rows.append(row)

        # create the array
        for i in range(len(ary)):
            for j in range(col):
                ary[i].append([])

        # fill the array
        for i in range(len(ary)):
            for j in range(col):
                ary[i][j] = rows[i][j]

        self.removeCells()

        # get the max width of the cells
        mx = 0
        for i in range(len(ary)):
            for j in range(len(ary[0])):
                if(len(ary[i][j]) >= mx):
                    mx = len(ary[i][j])
        w = mx
        self._width = mx

        loadCells = []
        for i in range(len(ary) + 1):
            loadCells.append([])
            for j in range(len(ary[0])):
                loadCells[i].append([])

        # create the new cells
        for i in range(len(ary) + 1):
            for j in range(len(ary[0])):
                tmp = Text(self, width=w, height=1)
                tmp.bind("<Tab>", self.focus_tab)
                tmp.bind("<Shift-Tab>", self.focus_sh_tab)
                tmp.bind("<Return>", self.focus_down)
                tmp.bind("<Shift-Return>", self.focus_up)
                tmp.bind("<Alt-Right>", self.focus_right)
                tmp.bind("<Alt-Left>", self.focus_left)
                tmp.bind("<Alt-Up>", self.focus_up)
                tmp.bind("<Alt-Down>", self.focus_down)
                tmp.bind("<Control-s>", self.saveFile)

                if i > 0:
                    tmp.insert(END, ary[i - 1][j])
                    tmp.bind("<Control-a>", self.selectall)
                else:
                    self.createTitle(j, tmp)

                loadCells[i][j] = tmp
                tmp.focus_force()
                self._cellList.append(tmp)

                tmp.grid(padx=0, pady=0, column=j, row=i)

        self._currentCells = loadCells
        self._currentCell = self._currentCells[0][0]


    def saveCells(self):
        filename = self._csvfilename
        #tkFileDialog.asksaveasfilename(initialdir=".", title="Save File", filetypes=(
        #    ("csv files", "*.csv"), ("all files", "*.*")), defaultextension=".csv")

        vals = []
        for i in range(1, len(self._currentCells)):
            for j in range(len(self._currentCells[0])):
                vals.append(self._currentCells[i][j].get(1.0, END).strip())

        with open(filename, "w") as csvfile:
            for rw in range(1, len(self._currentCells)):
                row = ""
                validity = True
                for i in range(len(self._currentCells[0])):
                    x = (rw - 1) * len(self._currentCells[0])
                    if vals[x + i].strip() == '':
                        validity = False
                        break

                    if(i != len(self._currentCells[0]) - 1):
                        row += vals[x + i] + ","
                    else:
                        row += vals[x + i]

                if validity:
                    csvfile.write(row + "\n")

        tkMessageBox.showinfo("", "Sauvegardé !", parent=self)

class TickersCsvEditor(Toplevel):
    def __init__(self, master, csvfilename, cnf={}):
        super().__init__(master, cnf)
        self._frame = TickersCsvEditorFrame(self, csvfilename)
        self.attributes('-topmost', 'true')

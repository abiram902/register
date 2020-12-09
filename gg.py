# register
python register
from tkinter import *
import tkinter.ttk as ttk
import csv
import pandas as pd
from tkinter import ttk as ted
import re
import prac as gg
import os


xis = ''
file1 = os.environ["HOMEPATH"] + r"\Desktop\todays_entry.csv"
f = open('item.dat', 'r+')
itemlist = [line.rstrip("\n") for line in f.readlines()]
f.close()
ff = open('customer.dat', 'r+')
tolist = [line.rstrip("\n") for line in ff.readlines()]
f.close()
fff = open('supplier.dat', 'r+')
fromlist = [line.rstrip("\n") for line in fff.readlines()]
f.close()


class AutocompleteEntry(Entry):
    def __init__(self, autocompleteList, *args, **kwargs):

        # Listbox length
        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 8

        # Custom matches function
        if 'matchesFunction' in kwargs:
            self.matchesFunction = kwargs['matchesFunction']
            del kwargs['matchesFunction']
        else:
            def matches(fieldValue, acListEntry):
                pattern = re.compile('.*' + re.escape(fieldValue) + '.*', re.IGNORECASE)
                return re.match(pattern, acListEntry)

            self.matchesFunction = matches

        Entry.__init__(self, *args, **kwargs)
        self.focus()

        self.autocompleteList = autocompleteList

        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.moveUp)
        self.bind("<Down>", self.moveDown)

        self.listboxUp = False

    def changed(self, name, index, mode):
        if self.var.get() == '':
            if self.listboxUp:
                self.listbox.destroy()
                self.listboxUp = False
        else:
            words = self.comparison()
            if words:
                if not self.listboxUp:
                    self.listbox = Listbox(width=self["width"], height=self.listboxLength)
                    self.listbox.bind("<Button-1>", self.selection)
                    self.listbox.bind("<Right>", self.selection)
                    self.listbox.place(relx=0.48, rely=0.13, relwidth=0.20)
                    self.listboxUp = True

                self.listbox.delete(0, END)
                for w in words:
                    self.listbox.insert(END, w)
            else:
                if self.listboxUp:
                    self.listbox.destroy()
                    self.listboxUp = False

    def selection(self, event):
        if self.listboxUp:
            self.var.set(self.listbox.get(ACTIVE))
            self.listbox.destroy()
            self.listboxUp = False
            self.icursor(END)

    def moveUp(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]

            if index != '0':
                self.listbox.selection_clear(first=index)
                index = str(int(index) - 1)

                self.listbox.see(index)  # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def moveDown(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]

            if index != END:
                self.listbox.selection_clear(first=index)
                index = str(int(index) + 1)

                self.listbox.see(index)  # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def comparison(self):
        return [w for w in self.autocompleteList if self.matchesFunction(self.var.get(), w)]


if __name__ == '__main__':
    Listofto = tolist
    Listoffrom = fromlist
    Listofitem = itemlist

    def matches(fieldValue, acListEntry):
        pattern = re.compile(re.escape(fieldValue) + '.*', re.IGNORECASE)
        return re.match(pattern, acListEntry)

# data entry function
def tempfile():
    df = pd.read_csv('todays_entry.csv')
    pf = pd.read_csv('three_years_entry.csv')
    x = pf.shape[0]
    i = df.shape
    u = i[0]+x
    with open('todays_entry.csv', 'a+', newline='')as f:
        thew = csv.writer(f)
        tn = e9.get()
        tn = str(tn).upper()
        tn = "".join(tn.split())
        thew.writerows([[u, int(e1.get()), str(e2.get()).upper(), str(e3.get()).upper(), e4.get(), str(e5.get()).upper(), str(e6.get()).upper(), e7.get(), e8.get(), tn]])

    e3.delete(0, END)
    e4.delete(0, END)
    e1.focus_set()
    # to clear tree view widget
    for i in tree.get_children():
        tree.delete(i)

    with open('todays_entry.csv') as f:
        reader = csv.DictReader(f, delimiter=',')

        for row in reader:
            index = row['index']
            lr = row['l_r_no']
            iv = row['invoice_no']
            it = row['item']
            qa = row['quantity']
            fr = row['from']
            to = row['to']
            lrd = row['l_r_date']
            ivd = row['invoice_date']
            tn = row['truck_no']

            tree.insert("", 0, values=(index, lr, iv, it, qa, fr, to, lrd, ivd, tn))

# function to add the daily entries to total entries
def append():
    df = pd.read_csv('todays_entry.csv', index_col='index')
    df.to_csv('three_years_entry.csv', mode='a', header=False)
    df = pd.read_csv('three_years_entry.csv', index_col='index')
    df = df.reset_index()
    df = df.drop(columns='index')
    df.index.name = 'index'
    df.to_csv('three_years_entry.csv')
    with open('todays_entry.csv', 'w', newline='')as f:
        thew = csv.writer(f)
        thew.writerows([['index', 'l_r_no', 'invoice_no', 'item', 'quantity', 'from', 'to', 'l_r_date', 'invoice_date', 'truck_no']])
    for i in tree.get_children():
        tree.delete(i)
    gg.old_data_migration()
# to check temp csv
def check_entry(file):
    for i in tree.get_children():
        tree.delete(i)
    with open(file) as f:
        reader = csv.DictReader(f, delimiter=',')

        for row in reader:
            index = row['index']
            lr = row['l_r_no']
            iv = row['invoice_no']
            it = row['item']
            qa = row['quantity']
            fr = row['from']
            to = row['to']
            lrd = row['l_r_date']
            ivd = row['invoice_date']
            tn = row['truck_no']

            tree.insert("", 0, values=(index, lr, iv, it, qa, fr, to, lrd, ivd, tn))
    DELETE['state'] = DISABLED

# editing function

def edit():
    raise_frame(f1)

    got = tree.focus()
    dict = tree.item(got)
    new = list(dict.get('values'))

    m1.delete(0, END)
    m2.delete(0, END)
    m3.delete(0, END)
    m4.delete(0, END)
    m5.delete(0, END)
    m6.delete(0, END)
    m7.delete(0, END)
    m8.delete(0, END)
    m9.delete(0, END)
    # to clear entries in treeview
    for i in tree.get_children():
        tree.delete(i)

    m1.insert(INSERT, new[1])
    m2.insert(INSERT, new[2])
    m3.insert(INSERT, new[3])
    m4.insert(INSERT, new[4])
    m5.insert(INSERT, new[5])
    m6.insert(INSERT, new[6])
    m7.insert(INSERT, new[7])
    m8.insert(INSERT, new[8])
    m9.insert(INSERT, new[9])
    editButton['state'] = DISABLED
# replacing the new data in the csv file
    def insert():
        print('in insert')
        df = pd.read_csv('todays_entry.csv', index_col='index')
        # tn is to make the truck entry without space and all in uppercase
        tn = m9.get()
        tn = str(tn).upper()
        tn = "".join(tn.split())
        df.loc[new[0]] = [m1.get(), m2.get(), str(m3.get()).upper(), m4.get(), str(m5.get()).upper(), str(m6.get()).upper(), m7.get(), m8.get(), tn]
        print(df)
        df.to_csv('todays_entry.csv')
        '''e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e5.delete(0, END)
        e6.delete(0, END)
        e7.delete(0, END)
        e8.delete(0, END)
        e9.delete(0, END)'''
        # to clear entries in treeview
        for i in tree.get_children():
            tree.delete(i)
        # treeview feeder for csv file
        with open('todays_entry.csv') as f:
            reader = csv.DictReader(f, delimiter=',')

            for row in reader:
                index = row['index']
                lr = row['l_r_no']
                iv = row['invoice_no']
                it = row['item']
                qa = row['quantity']
                fr = row['from']
                to = row['to']
                lrd = row['l_r_date']
                ivd = row['invoice_date']
                tn = row['truck_no']

                tree.insert("", 0, values=(index, lr, iv, it, qa, fr, to, lrd, ivd, tn))

        return

    but = Button(f1, text='UPDATE', bg='green', fg='white', width=10, command=insert, font='Helvetica 10 bold')\
        .place(relx=0.86, rely=0.28, relwidth=0.04, relheight=0.1)

def raise_frame(frame):
    frame.tkraise()

def home_page():
    global frame
    frame = topframe
    topframe.tkraise()
    editButton['state'] = DISABLED
    DELETE['state'] = DISABLED
    DELETE_todays['state'] = DISABLED

def all_entries():
    global frame
    raise_frame(f3)
    frame = f3
    for i in tree.get_children():
        tree.delete(i)
    with open('three_years_entry.csv') as f:
        reader = csv.DictReader(f, delimiter=',')

        for row in reader:
            index = row['index']
            lr = row['l_r_no']
            iv = row['invoice_no']
            it = row['item']
            qa = row['quantity']
            fr = row['from']
            to = row['to']
            lrd = row['l_r_date']
            ivd = row['invoice_date']
            tn = row['truck_no']

            tree.insert("", 0, values=(index, lr, iv, it, qa, fr, to, lrd, ivd, tn))
    DELETE['state'] = DISABLED
    DELETE_todays['state'] = DISABLED
    select(event=True, clk=clickedAll, opt=options)
    return

def select(event, clk, opt):

    global xis
    global frame
    if clk.get() == opt[0]:
        ent = Entry(frame, borderwidth=3, bg='white')
        ent.place(relheight=0.1, relwidth=0.15, relx=0.25, rely=0.48)
        xis = ent
        print('lr')
    elif clk.get() == opt[1]:
        ent = AutocompleteEntry(Listofitem, frame, listboxLength=6, borderwidth=3, matchesFunction=matches, bg='white')
        ent.place(relheight=0.1, relwidth=0.15, relx=0.25, rely=0.48)
        xis = ent
        print('it')
    elif clk.get() == opt[2]:
        ent = AutocompleteEntry(Listoffrom, frame, listboxLength=6, borderwidth=3, matchesFunction=matches, bg='white')
        ent.place(relheight=0.1, relwidth=0.15, relx=0.25, rely=0.48)
        xis = ent
        print('fr')
    elif clk.get() == opt[3]:
        ent = AutocompleteEntry(Listofto, frame, listboxLength=6, borderwidth=3, matchesFunction=matches, bg='white')
        ent.place(relheight=0.1, relwidth=0.15, relx=0.25, rely=0.48)
        xis = ent
        print('to')
    else:
        ent = Entry(frame, borderwidth=3, bg='white')
        ent.place(relheight=0.1, relwidth=0.15, relx=0.25, rely=0.48)
        xis = ent


def Search(file, val):

    for i in tree.get_children():
        tree.delete(i)
    df = pd.read_csv(file)
    if val.get() == Options[0]:

        mf = df.loc[df['l_r_no'] == int(xis.get())]
    elif val.get() == Options[1]:
        iv = str(xis.get())
        print('inside'+iv+'nv')
        mf = df.loc[df['item'] == iv]
    elif val.get() == Options[2]:
        mf = df.loc[df['from'] == xis.get()]
    elif val.get() == Options[3]:
        mf = df.loc[df['to'] == xis.get()]

    mf.to_csv('TEMP.csv')
    print(mf)
    with open('TEMP.csv') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            index = row['index']
            lr = row['l_r_no']
            iv = row['invoice_no']
            it = row['item']
            qa = row['quantity']
            fr = row['from']
            to = row['to']
            lrd = row['l_r_date']
            ivd = row['invoice_date']
            tn = row['truck_no']

            tree.insert("", 0, values=(index, lr, iv, it, qa, fr, to, lrd, ivd, tn))

    return

'''def selction(event):
    if clickedAll.get()'''


def search(file, val):
    global xis
    for i in tree.get_children():
        tree.delete(i)
    df = pd.read_csv(file)
    if val.get() == Options[0]:
        mf = df.loc[df['l_r_no'] == int(xis.get())]
    elif val.get() == Options[1]:
        iv = str(xis.get())
        print('inside'+iv+'nv')
        mf = df.loc[df['item'] == iv]
    elif val.get() == Options[2]:
        mf = df.loc[df['from'] == xis.get()]
    elif val.get() == Options[3]:
        mf = df.loc[df['to'] == xis.get()]
    elif val.get() == options[4]:
        iv = str(xis.get())
        mf = df.loc[df['invoice_no'] == iv]
    elif val.get() == options[5]:
        mf = df.loc[df['l_r_date'] == xis.get()]
    elif val.get() == options[6]:
        mf = df.loc[df['invoice_date'] == xis.get()]
    elif val.get() == options[7]:
        tn = xis.get()
        tn = str(tn).upper()
        tn = "".join(tn.split())
        mf = df.loc[df['truck_no'] == tn]

    mf.to_csv('TEMP.csv')
    print(mf)
    with open('TEMP.csv') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            index = row['index']
            lr = row['l_r_no']
            iv = row['invoice_no']
            it = row['item']
            qa = row['quantity']
            fr = row['from']
            to = row['to']
            lrd = row['l_r_date']
            ivd = row['invoice_date']
            tn = row['truck_no']

            tree.insert("", 0, values=(index, lr, iv, it, qa, fr, to, lrd, ivd, tn))

    return

def enable(event):
    if editButton['state'] == DISABLED or DELETE['state'] == DISABLED or DELETE['state'] == DISABLED:
        editButton['state'] = NORMAL
        DELETE['state'] = NORMAL
        DELETE_todays['state'] = NORMAL

def disable(event):
    editButton['state'] = DISABLED
    DELETE_todays['state'] = DISABLED
    DELETE['state'] = DISABLED


def callback(event):
    if e1.get() != '' and e2.get() != '' and e3.get() != '' and e4.get() != '' and e5.get() != '' and e6.get() != '' \
            and e7.get() != '' and e8.get() != '' and e9.get() != '':
        add_button['state'] = NORMAL
        return True
    else:
        add_button['state'] = DISABLED
        return False

def addtolist(event):
    if e3.get() not in Listofitem and e3.get() != '':
        with open('item.dat', "a+") as file_object:
            # Move read cursor to the start of file.
            file_object.seek(0)
            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write("\n")
            # Append text at the end of file
            file_object.write(str(e3.get()).upper())
            itemlist.append(str(e3.get()).upper())

def addtolist1(event):
    if e5.get() not in Listoffrom and e5.get() != '':
        with open('supplier.dat', "a+") as file_object:
            # Move read cursor to the start of file.
            file_object.seek(0)
            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write("\n")
            # Append text at the end of file
            file_object.write(str(e5.get()).upper())
            fromlist.append(str(e5.get()).upper())


def addtolist2(event):
    if e6.get() not in Listofto and e6.get() != '':
        with open('customer.dat', "a+") as file_object:
            # Move read cursor to the start of file.
            file_object.seek(0)
            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write("\n")
            # Append text at the end of file
            file_object.write(str(e6.get()).upper())
            tolist.append(str(e6.get()).upper())
def conf(file):
    def destroy(file):
        con.destroy()
        delete(file)
    con = Tk()
    # Gets the requested values of the height and widht.
    windowWidth = con.winfo_reqwidth()
    windowHeight = con.winfo_reqheight()
    print("Width", windowWidth, "Height", windowHeight)

    # Gets both half the screen width/height and window width/height
    positionRight = int(con.winfo_screenwidth() / 2 - windowWidth / 2)
    positionDown = int(con.winfo_screenheight() / 2 - windowHeight / 2)

    # Positions the window in the center of the page.
    con.geometry("200x100+{}+{}".format(positionRight, positionDown))

    label = Label(con, text='Delete that entry?', font='Helvetica 10 bold').place(relx=0, rely=0, relwidth=1, relheight=0.5)
    yes = Button(con, text='Yes', bg='green', fg='white', command=lambda: destroy(file))
    yes.place(relx=0, rely=0.5, relheight=0.4, relwidth=0.5)

    No = Button(con, text='No', bg='red', fg='white', command=lambda: con.destroy()) \
        .place(relx=0.5, rely=0.5, relheight=0.4, relwidth=0.5)
    con.mainloop()

def delete(file):

    got = tree.focus()
    dict = tree.item(got)
    new = list(dict.get('values'))
    pf = pd.read_csv(file, index_col='index')
    pf = pf.drop(index=new[0])
    pf = pf.reset_index(drop=True)
    '''pf = pf.drop(columns='index')'''
    pf.index.name = 'index'
    pf.to_csv(file)

    for i in tree.get_children():
        tree.delete(i)
    with open(file) as f:
        reader = csv.DictReader(f, delimiter=',')

        for row in reader:
            index = row['index']
            lr = row['l_r_no']
            iv = row['invoice_no']
            it = row['item']
            qa = row['quantity']
            fr = row['from']
            to = row['to']
            lrd = row['l_r_date']
            ivd = row['invoice_date']
            tn = row['truck_no']

            tree.insert("", 0, values=(index, lr, iv, it, qa, fr, to, lrd, ivd, tn))
    DELETE_todays['state'] = DISABLED
    DELETE['state'] = DISABLED

    return

def clrsc():

    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    e5.delete(0, END)
    e6.delete(0, END)
    e7.delete(0, END)
    e8.delete(0, END)
    e9.delete(0, END)


def actadd(event):
    if callback(event):
        tempfile()

def searchAll(event):
    search('three_years_entry.csv', clickedAll)
    print('in search')


def doSomething():

    def popout():
        pop.destroy()
        root.destroy()



    pop = Tk()
    pop.title('WARNING')
    # Gets the requested values of the height and widht.
    windowWidth = pop.winfo_reqwidth()
    windowHeight = pop.winfo_reqheight()
    print("Width", windowWidth, "Height", windowHeight)

    # Gets both half the screen width/height and window width/height
    positionRight = int(pop.winfo_screenwidth() / 2 - windowWidth / 2)
    positionDown = int(pop.winfo_screenheight() / 2 - windowHeight / 2)

    # Positions the window in the center of the page.
    pop.geometry("200x100+{}+{}".format(positionRight, positionDown))

    label = Label(pop, text='Are you sure you want to quit?', font='Helvetica 10 bold').place(relx=0, rely=0, relheight=0.5, relwidth=1)
    b1 = Button(pop, text='Yes', bg='green', fg='white', command=popout)
    b1.place(relx=0.03, rely=0.60, relwidth=0.4, relheight=0.3)
    b2 = Button(pop, text='No', bg='red', fg='white', command=lambda: pop.destroy())
    b2.place(relx=0.55, rely=0.60, relwidth=0.4, relheight=0.3)
    pop.mainloop()
# front end
root = Tk()
root.title("Visahl Royal Roadlines")
# root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.configure(background='#6F02A2')

f1 = Frame(root) #edit frame
f1.place(relx=0.5, rely=0, relwidth=1, relheight=0.3, anchor='n')
f1.configure(background='white')

f2 = Frame(root)
f2.place(relx=0.5, rely=0, relwidth=1, relheight=0.3, anchor='n')

f3 = Frame(root) #allEntries frame
f3.place(relx=0.5, rely=0, relwidth=1, relheight=0.3, anchor='n')
f3.configure(background='white')

topframe = Frame(root) #home page
topframe.place(relx=0.5, rely=0, relwidth=1, relheight=0.3, anchor='n')
topframe.configure(background='white')

frame = topframe

TableMargin = Frame(root)
TableMargin.place(relx=0.5, rely=0.3, relheight=0.7, relwidth=1, anchor='n')


#ttk.Style().configure("Treeview", fieldbackground='#AEF3F3', background="#AEF3F3", foreground='red')
#style.configure("Combobox",fieldbackground='#AEF3F3')

# topframe (home page)..................................................................................................
l1 = Label(topframe, text='L.R.NO', font='helvetica 10 bold', bg='white').place(relx=0.03, rely=0.1, relwidth=0.04, relheight=0.1)
e1 = Entry(topframe, borderwidth=3, bg='white')
e1.place(relx=0.08, rely=0.1, relwidth=0.06, relheight=0.1)
e1.focus_set()

l2 = Label(topframe, text='INV.NO', font='helvetica 10 bold', bg='white').place(relx=0.18, rely=0.1, relwidth=0.04, relheight=0.1)
e2 = Entry(topframe, borderwidth=3, bg='white')
e2.place(relx=0.23, rely=0.1, relwidth=0.09, relheight=0.1)

l3 = Label(topframe, text='ITEM', font='helvetica 10 bold', anchor=W, justify=LEFT, background='white').place(relx=0.34, rely=0.1, relwidth=0.05, relheight=0.1)
e3 = AutocompleteEntry(Listofitem, topframe, listboxLength=10, width=32, borderwidth=3, matchesFunction=matches, background='white')
e3.place(relx=0.40, rely=0.1, relwidth=0.09, relheight=0.1)
e3.bind('<FocusOut>', addtolist)

l4 = Label(topframe, text='QUANTITY', font='helvetica 10 bold', background='white').place(relx=0.52, rely=0.1, relwidth=0.05, relheight=0.1)
e4 = Entry(topframe, borderwidth=3, background='white')
e4.place(relx=0.58, rely=0.1, relwidth=0.09, relheight=0.1)

l5 = Label(topframe, text='FROM', font='helvetica 10 bold', anchor=W, justify=LEFT, background='white').place(relx=0.69, rely=0.1, relwidth=0.05, relheight=0.1)
e5 = AutocompleteEntry(Listoffrom, topframe, listboxLength=10, width=32, borderwidth=3, matchesFunction=matches, background='white')
e5.place(relx=0.75, rely=0.1, relwidth=0.22, relheight=0.1)
e5.bind('<FocusOut>', addtolist1)

l6 = Label(topframe, text=' TO', font='helvetica 10 bold', anchor=W, justify=LEFT, background='white').place(relx=0.03, rely=0.28, relwidth=0.04, relheight=0.1)
e6 = AutocompleteEntry(Listofto, topframe, listboxLength=10, width=32, borderwidth=3, matchesFunction=matches, background='white')
e6.place(relx=0.08, rely=0.28, relwidth=0.24, relheight=0.1)
e6.bind('<FocusOut>', addtolist2)

l7 = Label(topframe, text='L.R.DATE', font='helvetica 10 bold', anchor=W, justify=LEFT, background='white').place(relx=0.34, rely=0.28, relwidth=0.05, relheight=0.1)
e7 = Entry(topframe, borderwidth=3, background='white')
e7.place(relx=0.40, rely=0.28, relwidth=0.09, relheight=0.1)

l8 = Label(topframe, text='INV.DATE', font='helvetica 10 bold', background='white').place(relx=0.52, rely=0.28, relwidth=0.05, relheight=0.1)
e8 = Entry(topframe, borderwidth=3, background='white')
e8.place(relx=0.58, rely=0.28, relwidth=0.09, relheight=0.1)

l9 = Label(topframe, text='TRUCK.No', font='helvetica 10 bold', anchor=W, justify=LEFT, background='white').place(relx=0.69, rely=0.28, relwidth=0.05, relheight=0.1)
e9 = Entry(topframe, borderwidth=3, background='white')
e9.place(relx=0.75, rely=0.28, relwidth=0.09, relheight=0.1)
e9.bind('<Key>', callback)

add_button = Button(topframe, text='ADD', background='black', fg='white', width=10, command=tempfile, font='helvetica 8 bold', state=DISABLED)
add_button.place(relx=0.86, rely=0.28, relwidth=0.04, relheight=0.1)
add_button.bind('<Button-1>', callback)
add_button.bind('<Enter>', callback)
add_button.bind('<Return>', actadd)

done = Button(topframe, text='Done', background='black', fg='white', width=10, command=append, font='helvetica 8 bold')\
        .place(relx=0.92, rely=0.48, relwidth=0.04, relheight=0.1)

editButton = Button(topframe, text='EDIT', background='black', fg='white', width=10, command=edit, font='helvetica 8 bold', state='disabled')
editButton.place(relx=0.86, rely=0.48, relwidth=0.04, relheight=0.1)

check_todays_entry = Button(topframe, text='CHECK', background='black', fg='white', command=lambda: check_entry('todays_entry.csv'), font='helvetica 8 bold', width=10)\
        .place(relx=0.92, rely=0.28, relwidth=0.04, relheight=0.1)

allEntries = Button(topframe, text='ALL ENTRIES', background='black', fg='white', width=15, command=all_entries, font='helvetica 8 bold')
allEntries.place(relx=0.67, rely=0.48, relwidth=0.1, relheight=0.1)
#allEntries.bind('<FocusOut>', lambda event:select(event, clk=clickedAll, opt=options))
search_todays = Button(topframe, text='SEARCH', background='black', fg='white', width=10, command=lambda: Search('todays_entry.csv', clicked), font='helvetica 8 bold')
search_todays.place(relx=0.41, rely=0.48, relheight=0.1, relwidth=0.04)

DELETE_todays = Button(topframe, text='DELETE', background='red', fg='white', width=10, command=lambda: conf('todays_entry.csv'), font='helvetica 8 bold', state='disabled')
DELETE_todays.place(relx=0.79, rely=0.48, relheight=0.1, relwidth=0.05)



topframe.bind("<Button-1>", callback)


# drop down box for searching the entire entries........................................................................
options = ['l.r.no', 'item', 'from', 'to', 'invoice no', 'l.r.date', 'invoice.date', 'truck no']
Options = ['l.r.no', 'item', 'from', 'to']
clickedAll = ted.Combobox(f3, value=options)
clickedAll.configure(background='#AEF3F3')
clickedAll.current(0)
clickedAll.bind('<<ComboboxSelected>>', lambda event:select(event, clk=clickedAll, opt=options))
clickedAll.place(relheight=0.1, relwidth=0.1, relx=0.11, rely=0.48)
clicked = ted.Combobox(topframe, value=Options)
clicked.current(0)
clicked.bind('<<ComboboxSelected>>', lambda event: select(event, clk=clicked, opt=Options))

clicked.place(relheight=0.1, relwidth=0.05, relx=0.18, rely=0.48)
select(event=True, clk=clicked, opt=Options)

'''ent = Entry(topframe, borderwidth=3)
ent.place(relheight=0.1, relwidth=0.15, relx=0.25, rely=0.48)
'''


# all entries frame.....................................................................................................
dl = Label(f3, text='Search by', font='helvetica 12 bold', anchor=W, justify=LEFT, background='white').place(relheight=0.1, relwidth=0.06, relx=0.05, rely=0.48)

check_main_entries = Button(f3, text='CHECK',  command=lambda: check_entry('three_years_entry.csv'), font='helvetica 8 bold', width=10, bg='black', fg='white')\
        .place(relx=0.51, rely=0.48, relwidth=0.04, relheight=0.1)

doneAllentries = Button(f3, text='Back', fg='white', bg='black', width=10, command=home_page, font='helvetica 8 bold')\
        .place(relx=0.46, rely=0.48, relwidth=0.04, relheight=0.1)

serch = Button(f3, text='SEARCH', width=10, command=lambda: search('three_years_entry.csv', clickedAll), font='helvetica 8 bold', bg='black', fg='white')
serch.place(relx=0.41, rely=0.48, relheight=0.1, relwidth=0.04)

DELETE = Button(f3, text='DELETE', bg='red', fg='white', width=10, command=lambda: conf('three_years_entry.csv'), font='helvetica 8 bold', state='disabled')
DELETE.place(relx=0.56, rely=0.48, relheight=0.1, relwidth=0.05)

'''entAll = Entry(f3, borderwidth=3)
entAll.place(relheight=0.1, relwidth=0.15, relx=0.25, rely=0.1)'''
# entTd = Entry(topframe, borderwidth=3)
# entTd.place(relheight=0.1, relwidth=0.15, relx=0.25, rely=0.48)



#frame f1 (editing frame)...............................................................................................
n1 = Label(f1, text='L.R.NO', font='helvetica 10 bold', background='white').place(relx=0.03, rely=0.1, relwidth=0.04, relheight=0.1)
m1 = Entry(f1, borderwidth=3, background='white')
m1.place(relx=0.08, rely=0.1, relwidth=0.06, relheight=0.1)

n2 = Label(f1, text='Inv.No', font='helvetica 10 bold', background='white').place(relx=0.18, rely=0.1, relwidth=0.04, relheight=0.1)
m2 = Entry(f1, borderwidth=3, background='white')
m2.place(relx=0.23, rely=0.1, relwidth=0.09, relheight=0.1)

n3 = Label(f1, text='Item', font='helvetica 10 bold', background='white').place(relx=0.35, rely=0.1, relwidth=0.04, relheight=0.1)
m3 = AutocompleteEntry(Listofitem, f1, listboxLength=10, width=32, borderwidth=3, matchesFunction=matches, background='white')
m3.place(relx=0.40, rely=0.1, relwidth=0.09, relheight=0.1)

n4 = Label(f1, text='Quantity', font='helvetica 10 bold', background='white').place(relx=0.52, rely=0.1, relwidth=0.05, relheight=0.1)
m4 = Entry(f1, borderwidth=3, background='white')
m4.place(relx=0.58, rely=0.1, relwidth=0.09, relheight=0.1)

n5 = Label(f1, text='From', font='helvetica 10 bold', background='white').place(relx=0.70, rely=0.1, relwidth=0.04, relheight=0.1)
m5 = AutocompleteEntry(Listoffrom, f1, listboxLength=10, width=32, borderwidth=3, matchesFunction=matches, background='white')
m5.place(relx=0.75, rely=0.1, relwidth=0.22, relheight=0.1)

n6 = Label(f1, text='To', font='helvetica 10 bold', anchor=W, justify=LEFT, background='white').place(relx=0.03, rely=0.28, relwidth=0.03, relheight=0.1)
m6 = AutocompleteEntry(Listofto, f1, listboxLength=10, width=32, borderwidth=3, matchesFunction=matches, background='white')
m6.place(relx=0.08, rely=0.28, relwidth=0.24, relheight=0.1)

n7 = Label(f1, text='L.r.Date', font='helvetica 10 bold', background='white').place(relx=0.34, rely=0.28, relwidth=0.05, relheight=0.1)
m7 = Entry(f1, borderwidth=3, background='white')
m7.place(relx=0.40, rely=0.28, relwidth=0.09, relheight=0.1)

n8 = Label(f1, text='Inv.Date', font='helvetica 10 bold', background='white').place(relx=0.52, rely=0.28, relwidth=0.05, relheight=0.1)
m8 = Entry(f1, borderwidth=3, background='white')
m8.place(relx=0.58, rely=0.28, relwidth=0.09, relheight=0.1)

n9 = Label(f1, text='Truck.No', font='helvetica 10 bold', background='white').place(relx=0.69, rely=0.28, relwidth=0.05, relheight=0.1)
m9 = Entry(f1, borderwidth=3, background='white')
m9.place(relx=0.75, rely=0.28, relwidth=0.09, relheight=0.1)

done1 = Button(f1, text='Back', fg='white', bg='black', width=10, command=home_page, font='Helvetica 8 bold')\
        .place(relx=0.92, rely=0.28, relwidth=0.04, relheight=0.1)
editButton1 = Button(f1, text='EDIT', fg='white', bg='black', width=10, command=edit, font='helvetica 8 bold')
editButton1.place(relx=0.86, rely=0.48, relwidth=0.04, relheight=0.1)
#.......................................................................................................................
# scroll bar widget
scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL, bg='black',)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL, bg='black', )

# treeview widget
tree = ttk.Treeview(TableMargin, columns=('index', "l.r.no", "invoice", "item", 'quantity', 'from', 'to', 'L.r.date', 'Invoice date', 'Truckno'), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
tree.bind('<<TreeviewSelect>>', enable)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
scrollbary.configure(background='white')
TableMargin.configure(background='white')

tree.heading('index', text='INDEX', anchor=W)
tree.heading('l.r.no', text="L.R.NO", anchor=W)
tree.heading('invoice', text="INVOICE NO", anchor=W)
tree.heading('item', text="ITEM", anchor=W)
tree.heading('quantity', text='QUANTITY', anchor=W)
tree.heading('from', text="FROM", anchor=W)
tree.heading('to', text='TO', anchor=W)
tree.heading('L.r.date', text='L.R.DATE', anchor=W)
tree.heading('Invoice date', text='INVOICE DATE', anchor=W)
tree.heading('Truckno', text='TRUCK NO', anchor=W)

tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=50)
tree.column('#2', stretch=NO, minwidth=0, width=100)
tree.column('#3', stretch=NO, minwidth=0, width=150)
tree.column('#4', stretch=YES, minwidth=0, width=150)
tree.column('#5', stretch=NO, minwidth=0, width=150)
tree.column('#6', stretch=YES, minwidth=0, width=150)
tree.column('#7', stretch=NO, minwidth=0, width=365)
tree.column('#8', stretch=NO, minwidth=0, width=100)
tree.column('#9', stretch=NO, minwidth=0, width=100)
tree.column('#10', stretch=NO, minwidth=0, width=100)


tree.pack(fill=X, padx=50)
root.protocol('WM_DELETE_WINDOW', doSomething)
root.bind('<Return>', actadd)


root.mainloop()

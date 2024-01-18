from tkinter import Tk, ttk, Label, StringVar, Entry, Spinbox
import tkinter as tk

def menuHighscores(tab3):
    def tostr(x):
        s = str(x)
        if len(s)==1:
            s = ' '+s
        return s
    def show(event):
        fp = open('highscore/classic/level'+blevel.get()+".num",'r+')
        r = fp.readlines()
        for i in range(0,10):
            s = tostr(i+1)
            lab = v[i]
            lab.config(text=s+' - '+(r[i].split('\n'))[0])
        
    lab_classic = Label(tab3,text="Level : ")
    lv = StringVar()
    blevel = Spinbox(tab3, justify = tk.CENTER, from_=1, to=5, state = 'readonly', textvariable=lv)
    bshow = ttk.Button(tab3,text="show")
    
    lab_classic.grid(row=0,column=0)
    blevel.grid(row=0,column=1)
    bshow.grid(row=0,column=2)
    
    
    v = []
    for i in range(1,11):
        s = tostr(i)
        lab = Label(tab3,text=s+' - ')
        lab.grid(row=i,column=0)
        v.append(lab)
    
    bshow.bind('<Button 1>', show)
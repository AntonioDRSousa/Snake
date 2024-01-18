from tkinter import Tk, ttk, Label, StringVar, Entry, Spinbox
import tkinter as tk
from Snake import Game
from Settings import load_cfg, toTuple

def menuNewGame(tab1):

    def classic_game(event):
        colors = toTuple(load_cfg())
        vel = int(in_vel.get())
        lv = int(blevel.get())
        Game('classic',colors,lv,vel)
        
    bng_classic = ttk.Button(tab1,text="classic")

    lab_classic = Label(tab1,text="Level : ")
    
    lv = StringVar()
    blevel = Spinbox(tab1, justify = tk.CENTER, from_=1, to=5, state = 'readonly', textvariable=lv)

    lab_vel = Label(tab1,text="velocity")
    vel = StringVar()
    in_vel = Spinbox(tab1, justify = tk.CENTER, from_=1, to=100, state = 'readonly', textvariable=vel)

    bng_classic.grid(row=1,column=0)
    lab_classic.grid(row=1,column=1)
    blevel.grid(row=1,column=2)
    
    lab_vel.grid(row=4,column=0)
    in_vel.grid(row=4,column=1)
    
    bng_classic.bind('<Button 1>',classic_game)
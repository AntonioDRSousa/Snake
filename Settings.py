import tkinter as tk
from tkinter import ttk

def menuGraphic(tab2):
    def setComponent(string,y):
        label = tk.Label(tab2,font=f,text=string)
        var = tk.StringVar(value=str(colors[string]))
        entry = tk.Entry(tab2,justify = tk.CENTER,textvariable=var)
        label.grid(row=y,column=0)
        entry.grid(row=y,column=1)
        return entry
        
    def checkTuple(s):
        if (s[0]=='(') and (s[-1]==')'):
            f = (s[1:-1]).split(',')
            for i in f:
                if not i.isdigit():
                    raise
            t=tuple(s)
            for i in range(3):
                if not (t[i] in range(0,256)):
                    raise
            return t
            
    def b1_event(event):
        print('reset')
        
    def b2_event(event):
        fp = open('Settings.cfg','w')
        w = []
        for i in range(len(c)):
            w.append(v[i]+':'+(c[i]).get()+'\n')
        fp.writelines(w)
        fp.close()
            
    colors = load_cfg()
    
    b1 = ttk.Button(tab2,text='Reset')
    b2 = ttk.Button(tab2,text='Save')
    b1.grid(row=0,column=2)
    b2.grid(row=1,column=2)
    
    b1.bind('<Button 1>',b1_event)
    b2.bind('<Button 1>',b2_event)
    
    f = ('Helvetica',10,'bold')
    
    c = []
    
    v = ['void',
         'text',
         'snake',
         'food',
         'field',
         'bord',
         'head',
         'shape_food',
         'shape_snake',
         'shape_block',
         'shape_bonus',
         'block']
    for i in range(len(v)):
        c.append(setComponent(v[i],i))
    
    
    
def load_cfg():
    colors = dict()
    fp = open('Settings.cfg','r')
    v = fp.readlines()
    for i in range(len(v)):
        x = (v[i].split('\n'))[0]
        t = x.split(':')
        colors[t[0]] = t[1]
    fp.close()
    return colors
    
def toTuple(c):
    def tup(s):
        t = (s[1:-1]).split(',')
        return (int(t[0]),int(t[1]),int(t[2]))
    v = dict()
    for i in list(c.keys()):
        v[i] = tup(c[i])
    return v
    
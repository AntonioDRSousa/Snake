from tkinter import Tk, ttk

from Menu import menuNewGame
from Settings import menuGraphic
from Highscores import menuHighscores

def main():
    win = Tk()
    win.geometry("600x600")
    win.title("SNAKE")
    tabcontrol = ttk.Notebook(win)
    tab1 = ttk.Frame(tabcontrol)
    tab2 = ttk.Frame(tabcontrol)
    tab3 = ttk.Frame(tabcontrol)
    tabcontrol.add(tab1,text="New Game")
    tabcontrol.add(tab2,text="Graphics Settings")
    tabcontrol.add(tab3,text="Highscores")
    tabcontrol.pack(expand=1,fill="both")
    
    menuNewGame(tab1)
    menuGraphic(tab2)
    menuHighscores(tab3)
    
    win.mainloop()

if __name__=="__main__":    
    main()
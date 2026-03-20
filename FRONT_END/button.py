import tkinter as tk

class CellButton:
    def __init__(self, master, row, col, command):
        self.row = row
        self.col = col
        self.revealed = False
        self.flagged = False

        self.button = tk.Button(
            master,
            width=3,
            height=1,
            command=command
        )

    def grid(self, row, col):
        self.button.grid(row=row, column=col)

    def reveal(self, value):
        self.revealed = True
        self.button.config(text=str(value), state="disabled")

    def show_mine(self):
        self.button.config(text="💣", bg="red")
    

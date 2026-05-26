from tkinter import *
from tkinter import ttk
import os
import sys

def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Screen:

    def __init__(
        self,
        rows,
        cols,
        mines,

        left_click,
        right_click,

        restart_callback,
        difficulty_callback,
        personalized_callback
    ):

        self.rows = rows
        self.cols = cols
        self.mines = mines

        self.left_click = left_click
        self.right_click = right_click

        self.restart_callback = restart_callback
        self.difficulty_callback = difficulty_callback
        self.personalized_callback = personalized_callback

        self.window = Tk()
        self.window.title("MINESWEEPER")
        self.window.geometry("600x400")
        self.window.configure(bg="#8da193")
        self.window.resizable(True, True)

        self.root_frame = Frame(self.window, bg="#8da193")
        self.root_frame.pack()
        
        icon = PhotoImage(file=resource_path("FRONT_END/LOGO.png"))
        self.window.iconphoto(True, icon)

        self.create_top_buttons()
        self.create_timer()
        self.create_matrix()

    # =========================
    # MAIN LOOP
    # =========================

    def run(self):

        self.window.mainloop()

    # =========================
    # TOP BUTTONS
    # =========================

    def create_top_buttons(self):

        top_frame = Frame(self.root_frame, bg="#8da193")
        top_frame.pack(pady=10)

        # START

        start_button = Button(
            top_frame,
            text="START",
            width=10,
            command=self.toggle_difficulty
        )

        start_button.pack(side=LEFT, padx=10)

        # RESTART

        restart_button = Button(
            top_frame,
            text="RESTART",
            width=10,
            command=self.restart_callback
        )

        restart_button.pack(side=LEFT, padx=10)

        # EXIT

        exit_button = Button(
            top_frame,
            text="EXIT",
            width=10,
            command=self.window.destroy
        )

        exit_button.pack(side=LEFT, padx=10)

        # COMBOBOX

        self.difficulty_combo = ttk.Combobox(
            top_frame,
            values=["Fácil", "Medio", "Difícil", "Personalizado"],
            state="readonly",
            width=10
        )

        self.difficulty_combo.current(0)
        
        self.flag_counter = Label(
            top_frame,
            text=f"Flags: 0/{self.mines}",
            bg="#8da193",
            font=("Arial", 12) 
        )
        self.flag_counter.pack(side=LEFT, padx=10)

    # =========================
    # DIFFICULTY
    # =========================

    def toggle_difficulty(self):

        if not self.difficulty_combo.winfo_ismapped():

            self.difficulty_combo.pack(
                side=LEFT,
                padx=10
            )

        else:

            difficulty = self.difficulty_combo.get()

            self.difficulty_combo.pack_forget()

            self.difficulty_callback(
                difficulty
            )

    # =========================
    # MATRIX
    # =========================

    def create_matrix(self):

        self.matrix_frame = Frame(self.root_frame, bg="#8da193")
        self.matrix_frame.pack()

        self.buttons = []

        for r in range(self.rows):

            row_buttons = []

            for c in range(self.cols):

                button = Button(
                    self.matrix_frame,
                    width=3,
                    height=1
                )

                button.bind(
                    "<Button-1>",
                    lambda e, r=r, c=c:
                    self.left_click(r, c)
                )

                button.bind(
                    "<Button-3>",
                    lambda e, r=r, c=c:
                    self.right_click(r, c)
                )

                button.grid(row=r, column=c)

                row_buttons.append(button)

            self.buttons.append(row_buttons)

    # =========================
    # RESET
    # =========================

    def reset_board(self):

        self.matrix_frame.destroy()

        self.create_matrix()

    def rebuild_board(self, rows, cols):

        self.rows = rows
        self.cols = cols

        self.reset_board()

    # =========================
    # UPDATE UI
    # =========================

    def reveal_cell(self, r, c, value):

        button = self.buttons[r][c]

        if value == 0:

            button.config(
                text="",
                relief=SUNKEN,
                state=DISABLED
            )

        else:

            button.config(
                text=str(value),
                relief=SUNKEN,
                state=DISABLED
            )

    def update_flag(self, r, c, flagged):

        button = self.buttons[r][c]

        if flagged:
            button.config(text="🚩")
        else:
            button.config(text="")

    def show_mine(self, r, c):

        button = self.buttons[r][c]

        button.config(
            text="💣",
            bg="red"
        )

    def show_game_over(self):

        game_over = Toplevel(self.window)

        game_over.title("GAME OVER")

        Label(
            game_over,
            text="💣 GAME OVER 💣",
            font=("Arial", 20)
        ).pack(padx=20, pady=20)
        
    def show_win(self):
        win = Toplevel(self.window)

        win.title("YOU WIN!")

        Label(
            win,
            text="🎉 YOU WIN! 🎉",
            font=("Arial", 20)
        ).pack(padx=20, pady=20)
        
    def update_flag_counter(self, flagged_count, total_mines):
        self.flag_counter.config(text=f"Flags: {flagged_count}/{total_mines}")
        
    def create_timer(self):
        self.timer_label = Label(
            self.root_frame,
            text="Tiempo: 0",
            bg="#8da193",
            font=("Arial", 12)
        )
        self.timer_label.pack(pady=5)

    def update_timer(self, seconds):
        self.timer_label.config(text=f"Tiempo: {seconds}")
    
    def window_personalized(self):
        personalized_window = Toplevel(self.window)
        personalized_window.title("Personalizado")

        Label(personalized_window, text="Filas:").grid(row=0, column=0, padx=5, pady=5)
        rows_entry = Entry(personalized_window)
        rows_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(personalized_window, text="Columnas:").grid(row=1, column=0, padx=5, pady=5)
        cols_entry = Entry(personalized_window)
        cols_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(personalized_window, text="Minas:").grid(row=2, column=0, padx=5, pady=5)
        mines_entry = Entry(personalized_window)
        mines_entry.grid(row=2, column=1, padx=5, pady=5)
        
        submit_btn = Button(personalized_window, text="Submit",command=lambda: self.submit_personalized(
            rows_entry,
            cols_entry,
            mines_entry,
            personalized_window
        ))
        submit_btn.grid(row=3, column=0, columnspan=2, pady=10)
    
    def submit_personalized(self, rows_entry, cols_entry, mines_entry, window):

        rows = int(rows_entry.get())
        cols = int(cols_entry.get())
        mines = int(mines_entry.get())

        self.personalized_callback(
            rows,
            cols,
            mines
        )

        window.destroy()

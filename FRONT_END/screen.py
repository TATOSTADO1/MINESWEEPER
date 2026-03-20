from logging import root
from tkinter import *
from tkinter import ttk


from BACK_END.board import Board

class Screen:
    def __init__(self, rows, cols, board=None):
        self.first_click = TRUE
        self.rows = rows
        self.cols = cols
        self.board = board
    
        # ---------------- VENTANA PRINCIPAL ----------------
        self.window = Tk()
        self.window.title("MINESWEEPER")
        self.window.geometry("600x400")
        self.window.configure(bg="#8da193")
        self.window.resizable(True, True)
    
        icon = PhotoImage(file="FRONT_END/LOGO.png")
        self.window.iconphoto(True, icon)
    
        # ---------------- CONTENEDOR CON GRID ----------------
        self.container = Frame(self.window, bg="#8da193")
        self.container.pack(fill=BOTH, expand=True)
    
        # ---------------- CANVAS Y SCROLLBARS ----------------
        self.canvas = Canvas(self.container, bg="#8da193", highlightthickness=0)
    
        self.v_scroll = Scrollbar(
            self.container,
            orient=VERTICAL,
            command=self.canvas.yview
        )
    
        self.h_scroll = Scrollbar(
            self.container,
            orient=HORIZONTAL,
            command=self.canvas.xview
        )
    
        self.canvas.configure(
            yscrollcommand=self.v_scroll.set,
            xscrollcommand=self.h_scroll.set
        )
    
        # ---------------- POSICIÓN CON GRID ----------------
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll.grid(row=1, column=0, sticky="ew")
    
        # Permitir expansión
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
    
        # ---------------- FRAME INTERNO DEL CANVAS ----------------
        self.root_frame = Frame(self.canvas, bg="#8da193")
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.root_frame,
            anchor="n"
        )
    
        # Centrar contenido cuando cambie tamaño
        self.canvas.bind("<Configure>", self.center_content) 
    
        # ---------------- CONSTRUIR UI ----------------
        self.create_title()
        self.create_buttons_start()
        self.create_matrix()
    
        # Ajustar región de scroll
        self.root_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
        # Scroll con mouse
        self.enable_mouse_scroll()
    
        self.window.mainloop()
    
    
    def enable_mouse_scroll(self):
        self.canvas.bind_all(
        "<MouseWheel>",
        lambda e: self.canvas.yview_scroll(-1 * (e.delta // 120), "units")
    )

        
    def create_title(self):
        title_frame = Frame(self.root_frame, bg="#8da193")
        title_frame.pack(pady=10)

        title_label = Label(
            title_frame,
            text="MINESWEEPER",
            font=("Arial", 24),
            bg="#8da193",
            relief="raised",
            bd=2,
            fg="white"
        )
        title_label.pack(pady=10)

    def create_matrix(self):
        self.matrix_frame = Frame(self.root_frame, bg="#8da193")
        self.matrix_frame.pack(pady=10)

        self.buttons = []
        for r in range(self.rows):
            row_buttons = []
            for c in range(self.cols):
            
                button = Button(
                self.matrix_frame,
                width=3,
                height=1,
                )
                
                button.bind("<Button-1>", lambda e, r=r, c=c: self.handle_click(r, c))  # izquierdo
                button.bind("<Button-3>", lambda e, r=r, c=c: self.flag_cell(r, c))     # derecho
                button.grid(row=r, column=c)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        self.root_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        return self.buttons
    
    def flag_cell(self, r, c):
        button = self.buttons[r][c]

        # No permitir marcar si ya está revelado
        if button['state'] == DISABLED:
            return

        # Alternar bandera
        if button['text'] == "🚩":
            button.config(text="")
        else:
            button.config(text="🚩")
    
    def handle_click(self, r, c):
        if self.first_click:
            self.first_click = False
            self.first_pushed_cell(r, c)
        else:
            self.reveal_cell(r, c)
    
    def reveal_cell(self, r, c):
        value = self.board.grid[r][c]

        button = self.buttons[r][c]

        if value == -1:
            button.config(text="💣", bg="red")
            self.window_destroy()
        elif value == 0:
            button.config(text="", relief=SUNKEN)
        else:
            button.config(text=str(value), relief=SUNKEN)

        button.config(state=DISABLED)
        
    def window_destroy(self):
        game_over = Toplevel(self.window)
        game_over.title("Game Over")
        game_over.geometry("350x250")
        game_over.configure(bg="#2c3e50")
        game_over.resizable(False, False)

        # Hacer que aparezca centrada
        game_over.transient(self.window)
        game_over.grab_set()

        # Frame principal
        main_frame = Frame(game_over, bg="#2c3e50")
        main_frame.pack(expand=True, fill=BOTH, padx=20, pady=20)

        # Icono (emoji bomba)
        icon_label = Label(
            main_frame,
            text="💣",
            font=("Arial", 40),
            bg="#2c3e50",
            fg="white"
        )
        icon_label.pack(pady=(0, 10))

        # Texto principal
        title_label = Label(
            main_frame,
            text="GAME OVER",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="#e74c3c"
        )
        title_label.pack()

        # Texto secundario
        subtitle = Label(
            main_frame,
            text="Has pisado una mina",
            font=("Arial", 11),
            bg="#2c3e50",
            fg="white"
        )
        subtitle.pack(pady=5)

        # Botón cerrar
        close_button = Button(
            main_frame,
            text="Cerrar",
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            relief=FLAT,
            width=12,
            command=game_over.destroy
        )
        close_button.pack(pady=15)
        
        

    def create_buttons_start(self):
        self.button_frame = Frame(self.root_frame, bg="#8da193")
        self.button_frame.pack(pady=10)

        # START
        start_button = Button(
            self.button_frame,
            text="START",
            width=10,
            command=self.toggle_difficulty
        )
        start_button.pack(side=LEFT, padx=10)

        # RESTART
        restart_button = Button(
            self.button_frame,
            text="RESTART",
            width=10,
            command=self.restart
        )
        restart_button.pack(side=LEFT, padx=10)

        # EXIT
        exit_button = Button(
            self.button_frame,
            text="EXIT",
            width=10,
            command=self.window.destroy
        )
        exit_button.pack(side=LEFT, padx=10)

        # Combobox dentro del MISMO frame
        self.scroll_frame = Frame(self.root_frame, bg="#8da193")
        self.scroll_frame.pack(pady=10)
        self.difficulty_combo = ttk.Combobox(
            self.scroll_frame,
            values=["Fácil", "Medio", "Difícil"],
            state="readonly",
            width=10
        )
        self.difficulty_combo.current(0)
        
    def restart(self):
        # Destruir matriz anterior si existe
        if hasattr(self, "matrix_frame"):
            self.matrix_frame.destroy()

        # Crear nueva matriz visual
        self.create_matrix()
        self.first_click=TRUE
        
    def toggle_difficulty(self):
        if not self.difficulty_combo.winfo_ismapped():
            self.difficulty_combo.pack(side=LEFT, padx=10)
        else:
            self.difficulty_combo.pack_forget()
            valor = self.difficulty_combo.get()
    
            rows, cols, mines = Board.get_difficulty_config(valor)

            # Guardamos nueva configuración
            self.rows = rows
            self.cols = cols

            # Creamos el tablero lógico
            self.board = Board(rows, cols, mines)

            # Destruir matriz anterior si existe
            if hasattr(self, "matrix_frame"):
                self.matrix_frame.destroy()

            # Crear nueva matriz visual
            self.create_matrix()
            
            self.first_click = True  # Reiniciar estado del primer click
            
        # Actualizar scrollregion
        self.root_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
    
    def center_content(self, event=None):
        canvas_width = self.canvas.winfo_width()
        content_width = self.root_frame.winfo_reqwidth()

        x = max((canvas_width - content_width) // 2, 0)

        self.canvas.coords(self.canvas_window, x, 0)
        
    def first_pushed_cell(self, r, c):
        button = self.buttons[r][c]

        # 🛑 Evitar repetir
        if button['state'] == DISABLED:
            return

        value = self.board.grid[r][c]

        # 🔒 Marcar como visitado
        button.config(state=DISABLED, relief=SUNKEN)

        if value == -1:
            button.config(text="💣", bg="red")
            self.window_destroy()
            self.first_click = True
            return

        elif value > 0:
            # 🔢 Mostrar número y NO expandir
            button.config(text=str(value))
            self.first_click = True

            return

        else:  # value == 0
            button.config(text="")

            adyacentes = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1),          (0, 1),
                (1, -1),  (1, 0), (1, 1)
            ]

            for dr, dc in adyacentes:
                nr, nc = r + dr, c + dc

                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    self.first_pushed_cell(nr, nc)

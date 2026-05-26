from BACK_END.board import Board
from FRONT_END.screen import Screen


class Game:

    def __init__(self):

        self.rows = 10
        self.cols = 10
        self.mines = 20
        self.seconds = 0
        self.timer_job = None
        self.timer_running = False

        self.board = Board(self.rows, self.cols, self.mines)

        self.screen = Screen(
            self.rows,
            self.cols,
            self.mines,
            left_click=self.left_click,
            right_click=self.right_click,
            restart_callback=self.restart,
            difficulty_callback=self.change_difficulty,
            personalized_callback=self.personalized_settings,
        )

        self.screen.run()

    # ===================================
    # TIMER
    # ===================================

    def update_timer(self):
        self.seconds += 1
        self.screen.update_timer(self.seconds)
        self.timer_job = self.screen.window.after(1000, self.update_timer)

    def start_timer(self):
        self.stop_timer()
        self.seconds = 0
        self.screen.update_timer(0)
        self.timer_running = True
        self.timer_job = self.screen.window.after(1000, self.update_timer)

    def stop_timer(self):
        if self.timer_job is not None:
            self.screen.window.after_cancel(self.timer_job)
            self.timer_job = None
        self.timer_running = False

    # ===================================
    # CLICKS
    # ===================================

    def left_click(self, r, c):

        if not self.timer_running:
            self.start_timer()

        if self.board.flagged[r][c]:
            return

        # CASO 1: chord en celda ya revelada
        if self.board.revealed[r][c]:

            value = self.board.grid[r][c]

            if value <= 0:
                return

            if self.board.count_adjacent_flags(r, c) != value:
                return

            revealed, hit_mine = self.board.chord_reveal(r, c)

            for row, col in revealed:
                cell_value = self.board.grid[row][col]
                if cell_value == -1:
                    self.screen.show_mine(row, col)
                else:
                    self.screen.reveal_cell(row, col, cell_value)

            if hit_mine:
                self.stop_timer()
                self.screen.show_game_over()
                return

            self.all_cells_revealed()
            return

        # CASO 2: mina
        if self.board.grid[r][c] == -1:
            self.screen.show_mine(r, c)
            self.stop_timer()
            self.screen.show_game_over()
            return

        # CASO 3: celda normal
        revealed = self.board.reveal(r, c)

        for row, col in revealed:
            self.screen.reveal_cell(row, col, self.board.grid[row][col])

        self.all_cells_revealed()

    def right_click(self, r, c):

        if self.board.revealed[r][c]:
            return

        self.board.toggle_flag(r, c)

        self.screen.update_flag(r, c, self.board.flagged[r][c])
        self.update_flag_counter()
        self.all_cells_revealed()

    # ===================================
    # RESTART
    # ===================================

    def restart(self):
        self.stop_timer()
        self.seconds = 0
        self.screen.update_timer(0)

        self.board = Board(self.rows, self.cols, self.mines)
        self.update_flag_counter()
        self.screen.reset_board()

    # ===================================
    # DIFFICULTY
    # ===================================

    def change_difficulty(self, difficulty):

        rows, cols, mines = Board.get_difficulty_config(difficulty)
        
        if (rows, cols, mines) == (0, 0, 0):
            self.screen.window_personalized()
        
        self.rows = rows
        self.cols = cols
        self.mines = mines

        self.stop_timer()
        self.seconds = 0
        self.screen.update_timer(0)

        self.board = Board(rows, cols, mines)
        self.screen.rebuild_board(rows, cols)
        self.update_flag_counter()
    
    def personalized_settings(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines

        self.stop_timer()
        self.seconds = 0
        self.screen.update_timer(0)

        self.board = Board(rows, cols, mines)
        self.screen.rebuild_board(rows, cols)
        self.update_flag_counter()

    # ===================================
    # WIN CHECK
    # ===================================

    def all_cells_revealed(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.board.revealed[r][c] and self.board.grid[r][c] != -1:
                    return
        self.stop_timer()
        self.screen.show_win()

    # ===================================
    # FLAG COUNTER
    # ===================================

    def update_flag_counter(self):
        flagged_count = sum(
            self.board.flagged[r][c]
            for r in range(self.rows)
            for c in range(self.cols)
        )
        self.screen.update_flag_counter(flagged_count, self.mines)
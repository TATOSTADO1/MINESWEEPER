from BACK_END.board import Board
from FRONT_END.screen import Screen


class Game:

    def __init__(self):

        self.rows = 10
        self.cols = 10
        self.mines = 20

        self.board = Board(
            self.rows,
            self.cols,
            self.mines
        )

        self.screen = Screen(
            self.rows,
            self.cols,

            left_click=self.left_click,
            right_click=self.right_click,

            restart_callback=self.restart,
            difficulty_callback=self.change_difficulty
        )

        self.screen.run()

# ===================================
# CLICKS
# ===================================

    def left_click(self, r, c):

        if self.board.flagged[r][c]:
            return

        # === CASO 1: clic en celda YA revelada con número (chord) ===
        if self.board.revealed[r][c]:

            value = self.board.grid[r][c]

            # Solo actúa si es un número (1-8)
            if value <= 0:
                return

            flags_around = self.board.count_adjacent_flags(r, c)

            # Solo actúa si las banderas coinciden con el número
            if flags_around != value:
                return

            revealed, hit_mine = self.board.chord_reveal(r, c)

            for row, col in revealed:

                cell_value = self.board.grid[row][col]

                if cell_value == -1:
                    self.screen.show_mine(row, col)
                else:
                    self.screen.reveal_cell(row, col, cell_value)

            if hit_mine:
                self.screen.show_game_over()

            return

        # === CASO 2: clic en mina ===
        value = self.board.grid[r][c]

        if value == -1:
            self.screen.show_mine(r, c)
            self.screen.show_game_over()
            return

        # === CASO 3: clic normal ===
        revealed = self.board.reveal(r, c)

        for row, col in revealed:

            value = self.board.grid[row][col]
            self.screen.reveal_cell(row, col, value)


    def right_click(self, r, c):

        if self.board.revealed[r][c]:
            return

        self.board.toggle_flag(r, c)

        flagged = self.board.flagged[r][c]

        self.screen.update_flag(
           r,
           c,
           flagged
        )
        
# ===================================
# RESTART
# ===================================

    def restart(self):

        self.board = Board(
            self.rows,
            self.cols,
            self.mines
        )

        self.screen.reset_board()

# ===================================
# DIFFICULTY
# ===================================

    def change_difficulty(self, difficulty):

        rows, cols, mines = Board.get_difficulty_config(
            difficulty
        )

        self.rows = rows
        self.cols = cols
        self.mines = mines

        self.board = Board(
            rows,
            cols,
            mines
        )

        self.screen.rebuild_board(
            rows,
            cols
        )
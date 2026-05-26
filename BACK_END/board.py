import random


class Board:

    def __init__(self, rows, cols, mines):

        self.rows = rows
        self.cols = cols
        self.mines = mines

        self.grid = [
            [0 for _ in range(cols)]
            for _ in range(rows)
        ]

        self.revealed = [
            [False for _ in range(cols)]
            for _ in range(rows)
        ]

        self.flagged = [
            [False for _ in range(cols)]
            for _ in range(rows)
        ]

        self.place_mines()
        self.fill_numbers()

    # ==========================
    # MINAS
    # ==========================

    def place_mines(self):

        mines_positions = set()

        while len(mines_positions) < self.mines:

            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)

            mines_positions.add((r, c))

        for r, c in mines_positions:

            self.grid[r][c] = -1

    # ==========================
    # NUMEROS
    # ==========================

    def count_neighbors(self, row, col):

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1),  (1, 0), (1, 1)
        ]

        count = 0

        for dr, dc in directions:

            nr = row + dr
            nc = col + dc

            if 0 <= nr < self.rows and 0 <= nc < self.cols:

                if self.grid[nr][nc] == -1:
                    count += 1

        return count

    def fill_numbers(self):

        for r in range(self.rows):

            for c in range(self.cols):

                if self.grid[r][c] != -1:

                    self.grid[r][c] = self.count_neighbors(r, c)

    # ==========================
    # REVEAL
    # ==========================

    def reveal(self, r, c):

        if self.revealed[r][c]:
            return []

        self.revealed[r][c] = True

        revealed_cells = [(r, c)]

        if self.grid[r][c] == 0:

            directions = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1),          (0, 1),
                (1, -1),  (1, 0), (1, 1)
            ]

            for dr, dc in directions:

                nr = r + dr
                nc = c + dc

                if 0 <= nr < self.rows and 0 <= nc < self.cols:

                    if not self.revealed[nr][nc]:

                        revealed_cells.extend(
                            self.reveal(nr, nc)
                        )

        return revealed_cells
    
    

    def count_adjacent_flags(self, r, c):

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

        count = 0

        for dr, dc in directions:

            nr = r + dr
            nc = c + dc

            if 0 <= nr < self.rows and 0 <= nc < self.cols:

                if self.flagged[nr][nc]:
                    count += 1

        return count


    def chord_reveal(self, r, c):
        """
        Devuelve (celdas_reveladas, hubo_mina).
        Se llama cuando se hace clic en una celda numerada ya revelada.
        """

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

        revealed_cells = []
        hit_mine = False

        for dr, dc in directions:

            nr = r + dr
            nc = c + dc

            if 0 <= nr < self.rows and 0 <= nc < self.cols:

                if not self.flagged[nr][nc] and not self.revealed[nr][nc]:

                    if self.grid[nr][nc] == -1:
                        hit_mine = True
                        revealed_cells.append((nr, nc))  # para mostrar la mina

                    else:
                        revealed_cells.extend(self.reveal(nr, nc))

        return revealed_cells, hit_mine

    # ==========================
    # FLAGS
    # ==========================

    def toggle_flag(self, r, c):

        self.flagged[r][c] = not self.flagged[r][c]

    # ==========================
    # DIFFICULTY
    # ==========================

    @staticmethod
    def get_difficulty_config(difficulty):

        if difficulty == "Fácil":
            return 10, 10, 20

        elif difficulty == "Medio":
            return 15, 15, 45

        elif difficulty == "Difícil":
            return 20, 20, 80
        elif difficulty == "Personalizado":
            return 0, 0, 0
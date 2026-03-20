import random

class Board:
    def __init__(self, rows: int, cols: int, num_mines: int):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines

        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

        self._place_mines()
        self._fill_numbers()
        
    def _place_mines(self):
        rows = self.rows
        columns = self.cols
        num_mines = self.num_mines
        mines = set()
        
        while len(mines) < num_mines:
        
            r=random.randint(0,self.rows-1)
            c=random.randint(0,self.cols-1)
        
            mines.add((r,c))
        
        for r,c in mines:
            self.grid[r][c]=-1
        

    def _count_neighbors(self  , row, col):
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1),  (1, 0), (1, 1)
        ]

        count = 0
        for dr, dc in directions:
            r = row + dr
            c = col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols:
                if self.grid[r][c] == -1:
                    count += 1
        return count

    def _fill_numbers(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] != -1:
                    self.grid[r][c] = self._count_neighbors(r, c)
    
    @staticmethod
    def get_difficulty_config(difficulty):
        if difficulty == "Fácil":
            return 10, 10, 20
        elif difficulty == "Medio":
            return 15, 15, 45
        elif difficulty == "Difícil":
            return 20, 20, 80
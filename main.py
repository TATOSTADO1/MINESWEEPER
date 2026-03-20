'''minesweeper game settings'''
from BACK_END import board
from BACK_END.board import Board
from FRONT_END.screen import Screen 

def on_cell_click(row, col):
    print(f"Click en celda ({row}, {col})")


def main():

    rows = 10
    columns = 10
    num_mines = 15

    board = Board(rows, columns, num_mines)
    Screen(rows, columns, on_cell_click, board)
    
if __name__ == "__main__":
    main()

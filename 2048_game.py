"""
2048 Game Implementation with GUI
A functional programming approach to the classic 2048 game
"""

import tkinter as tk
from tkinter import messagebox
import random
from typing import List, Tuple, Optional
from copy import deepcopy


def create_board(size: int = 4) -> List[List[int]]:
    """Create an empty board of given size."""
    return [[0 for _ in range(size)] for _ in range(size)]

def get_empty_cells(board: List[List[int]]) -> List[Tuple[int, int]]:
    """Return list of coordinates of empty cells."""
    return [(i, j) for i in range(len(board)) 
            for j in range(len(board[0])) if board[i][j] == 0]

def add_random_tile(board: List[List[int]]) -> List[List[int]]:
    """Add a random tile (2 or 4) to an empty cell. Returns new board."""
    new_board = deepcopy(board)
    empty_cells = get_empty_cells(new_board)
    
    if empty_cells:
        i, j = random.choice(empty_cells)
        new_board[i][j] = 2 if random.random() < 0.9 else 4
    
    return new_board

def initialize_game(size: int = 4) -> List[List[int]]:
    """Initialize a new game board with two random tiles."""
    board = create_board(size)
    board = add_random_tile(board)
    board = add_random_tile(board)
    return board

def compress(row: List[int]) -> Tuple[List[int], int]:
    """
    Compress a row by moving all non-zero elements to the left.
    Returns compressed row and score gained.
    """
    new_row = [num for num in row if num != 0]
    score = 0
    
    # Merge adjacent equal numbers
    i = 0
    while i < len(new_row) - 1:
        if new_row[i] == new_row[i + 1]:
            new_row[i] *= 2
            score += new_row[i]
            new_row.pop(i + 1)
        i += 1
    
    # Pad with zeros
    new_row.extend([0] * (len(row) - len(new_row)))
    
    return new_row, score

def move_left(board: List[List[int]]) -> Tuple[List[List[int]], int]:
    """Move all tiles left. Returns new board and score gained."""
    new_board = []
    total_score = 0
    
    for row in board:
        new_row, score = compress(row)
        new_board.append(new_row)
        total_score += score
    
    return new_board, total_score

def transpose(board: List[List[int]]) -> List[List[int]]:
    """Transpose the board (swap rows and columns)."""
    return [list(row) for row in zip(*board)]

def reverse_rows(board: List[List[int]]) -> List[List[int]]:
    """Reverse each row in the board."""
    return [row[::-1] for row in board]

def move_right(board: List[List[int]]) -> Tuple[List[List[int]], int]:
    """Move all tiles right. Returns new board and score gained."""
    board = reverse_rows(board)
    board, score = move_left(board)
    board = reverse_rows(board)
    return board, score

def move_up(board: List[List[int]]) -> Tuple[List[List[int]], int]:
    """Move all tiles up. Returns new board and score gained."""
    board = transpose(board)
    board, score = move_left(board)
    board = transpose(board)
    return board, score

def move_down(board: List[List[int]]) -> Tuple[List[List[int]], int]:
    """Move all tiles down. Returns new board and score gained."""
    board = transpose(board)
    board, score = move_right(board)
    board = transpose(board)
    return board, score

def boards_equal(board1: List[List[int]], board2: List[List[int]]) -> bool:
    """Check if two boards are equal."""
    return board1 == board2

def can_move(board: List[List[int]]) -> bool:
    """Check if any move is possible."""
    # Check for empty cells
    if get_empty_cells(board):
        return True
    
    # Check for possible merges horizontally
    for row in board:
        for i in range(len(row) - 1):
            if row[i] == row[i + 1]:
                return True
    
    # Check for possible merges vertically
    for col in range(len(board[0])):
        for row in range(len(board) - 1):
            if board[row][col] == board[row + 1][col]:
                return True
    
    return False

def has_won(board: List[List[int]], target: int = 2048) -> bool:
    """Check if the player has reached the target value."""
    return any(target in row for row in board)

def game_over(board: List[List[int]]) -> bool:
    """Check if the game is over (no moves possible)."""
    return not can_move(board)


class Game2048:
    """2048 Game with Tkinter GUI"""
    
    # Color schemes
    COLORS = {
        0: "#CDC1B4",
        2: "#EEE4DA",
        4: "#EDE0C8",
        8: "#F2B179",
        16: "#F59563",
        32: "#F67C5F",
        64: "#F65E3B",
        128: "#EDCF72",
        256: "#EDCC61",
        512: "#EDC850",
        1024: "#EDC53F",
        2048: "#EDC22E",
        4096: "#3C3A32",
        8192: "#3C3A32"
    }
    
    TEXT_COLORS = {
        0: "#CDC1B4",
        2: "#776E65",
        4: "#776E65",
        8: "#F9F6F2",
        16: "#F9F6F2"
    }
    
    def __init__(self, master: tk.Tk, size: int = 4):
        self.master = master
        self.size = size
        self.board = initialize_game(size)
        self.score = 0
        self.game_won = False
        
        self.setup_ui()
        self.update_ui()
        
        # Bind keyboard events
        self.master.bind("<Key>", self.handle_keypress)
    
    def setup_ui(self):
        """Setup the user interface."""
        self.master.title("2048 Game")
        self.master.configure(bg="#FAF8EF")
        
        # Header frame
        header_frame = tk.Frame(self.master, bg="#FAF8EF")
        header_frame.pack(pady=20)
        
        # Title
        title = tk.Label(
            header_frame,
            text="2048",
            font=("Helvetica", 48, "bold"),
            bg="#FAF8EF",
            fg="#776E65"
        )
        title.pack(side=tk.LEFT, padx=20)
        
        # Score display
        score_frame = tk.Frame(header_frame, bg="#BBADA0", padx=20, pady=10)
        score_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(
            score_frame,
            text="SCORE",
            font=("Helvetica", 12, "bold"),
            bg="#BBADA0",
            fg="#EEE4DA"
        ).pack()
        
        self.score_label = tk.Label(
            score_frame,
            text="0",
            font=("Helvetica", 24, "bold"),
            bg="#BBADA0",
            fg="#FFFFFF"
        )
        self.score_label.pack()
        
        # New game button
        new_game_btn = tk.Button(
            header_frame,
            text="New Game",
            font=("Helvetica", 12, "bold"),
            bg="#8F7A66",
            fg="#F9F6F2",
            command=self.restart_game,
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2"
        )
        new_game_btn.pack(side=tk.LEFT, padx=10)
        
        # Game board frame
        self.board_frame = tk.Frame(
            self.master,
            bg="#BBADA0",
            padx=10,
            pady=10
        )
        self.board_frame.pack()
        
        # Create grid cells
        self.cells = []
        cell_size = 100
        cell_padding = 10
        
        for i in range(self.size):
            row = []
            for j in range(self.size):
                cell_frame = tk.Frame(
                    self.board_frame,
                    bg="#CDC1B4",
                    width=cell_size,
                    height=cell_size
                )
                cell_frame.grid(
                    row=i,
                    column=j,
                    padx=cell_padding,
                    pady=cell_padding
                )
                cell_frame.pack_propagate(False)
                
                cell_label = tk.Label(
                    cell_frame,
                    text="",
                    font=("Helvetica", 32, "bold"),
                    bg="#CDC1B4",
                    fg="#CDC1B4"
                )
                cell_label.pack(expand=True)
                
                row.append(cell_label)
            self.cells.append(row)
        
        # Instructions
        instructions = tk.Label(
            self.master,
            text="Use Arrow Keys or WASD to play",
            font=("Helvetica", 10),
            bg="#FAF8EF",
            fg="#776E65"
        )
        instructions.pack(pady=10)
    
    def update_ui(self):
        """Update the UI to reflect current board state."""
        for i in range(self.size):
            for j in range(self.size):
                value = self.board[i][j]
                
                if value == 0:
                    self.cells[i][j].config(
                        text="",
                        bg=self.COLORS[0],
                        fg=self.COLORS[0]
                    )
                else:
                    self.cells[i][j].config(
                        text=str(value),
                        bg=self.COLORS.get(value, "#3C3A32"),
                        fg=self.TEXT_COLORS.get(value, "#F9F6F2")
                    )
        
        self.score_label.config(text=str(self.score))
    
    def handle_keypress(self, event):
        """Handle keyboard input."""
        key = event.keysym.lower()
        
        move_functions = {
            'up': move_up,
            'w': move_up,
            'down': move_down,
            's': move_down,
            'left': move_left,
            'a': move_left,
            'right': move_right,
            'd': move_right
        }
        
        if key in move_functions:
            self.make_move(move_functions[key])
    
    def make_move(self, move_function):
        """Execute a move and update game state."""
        old_board = deepcopy(self.board)
        new_board, score_gained = move_function(self.board)
        
        # Only update if board changed
        if not boards_equal(old_board, new_board):
            self.board = new_board
            self.score += score_gained
            self.board = add_random_tile(self.board)
            self.update_ui()
            
            # Check win condition
            if not self.game_won and has_won(self.board):
                self.game_won = True
                response = messagebox.askyesno(
                    "You Win!",
                    f"Congratulations! You reached 2048!\nScore: {self.score}\n\nContinue playing?"
                )
                if not response:
                    self.restart_game()
            
            # Check game over
            elif game_over(self.board):
                response = messagebox.askyesno(
                    "Game Over",
                    f"No more moves possible!\nFinal Score: {self.score}\n\nPlay again?"
                )
                if response:
                    self.restart_game()
    
    def restart_game(self):
        """Restart the game."""
        self.board = initialize_game(self.size)
        self.score = 0
        self.game_won = False
        self.update_ui()


def main():
    """Main function to run the game."""
    root = tk.Tk()
    root.resizable(False, False)
    
    # Allow custom board size (default 4x4)
    board_size = 4  # Change this to configure board size
    
    game = Game2048(root, size=board_size)
    root.mainloop()


if __name__ == "__main__":
    main()
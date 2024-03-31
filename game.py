import numpy as np
import random

class Game2048:
    def __init__(self):
        self.grid = np.zeros((4, 4), dtype=int)
        self.add_number()
        self.add_number()

    def add_number(self):
        available_positions = list(zip(*np.where(self.grid == 0)))
        if available_positions:
            row, col = random.choice(available_positions)
            self.grid[row, col] = random.choice([2, 4])

    def move(self, direction):
        original_grid = self.grid.copy()
        if direction == 'l':
            self.move_left()
        elif direction == 'r':
            self.move_right()
        elif direction == 'u':
            self.move_up()
        elif direction == 'd':
            self.move_down()
        
        if not np.array_equal(original_grid, self.grid):
            self.add_number()

    def compress(self, row):
        new_row = [i for i in row if i != 0]
        new_row += [0] * (4 - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(3):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                row[i + 1] = 0
        return row

    def move_left(self):
        for i in range(4):
            self.grid[i] = self.merge(self.compress(self.grid[i]))

    def move_right(self):
        for i in range(4):
            self.grid[i] = self.grid[i][::-1]
            self.grid[i] = self.merge(self.compress(self.grid[i]))
            self.grid[i] = self.grid[i][::-1]

    def move_up(self):
        self.grid = self.grid.T
        self.move_left()
        self.grid = self.grid.T

    def move_down(self):
        self.grid = self.grid.T
        self.move_right()
        self.grid = self.grid.T

    def game_over(self):
        if 0 in self.grid:
            return False
        for direction in ['l', 'r', 'u', 'd']:
            grid_copy = self.grid.copy()
            self.move(direction)
            if not np.array_equal(grid_copy, self.grid):
                self.grid = grid_copy
                return False
            self.grid = grid_copy
        return True

    def display(self):
        print(self.grid)

    def play(self, player):
        if player == 'query_player':
            while not self.game_over():
                self.display()
                move = input("Your move (l, r, u, d): ").strip().lower()
                if move in ['l', 'r', 'u', 'd']:
                    self.move(move)
                else:
                    print("Invalid move. Please enter 'l', 'r', 'u', or 'd'.")
        elif hasattr(player, '__call__'):  # Check if player is a callable function (agent)
            while not self.game_over():
                self.display()
                move = player(self.grid)
                if move in ['l', 'r', 'u', 'd']:
                    print(f"Agent's move: {move.upper()}")
                    self.move(move)
                else:
                    print("Agent made an invalid move.")
        else:
            print("Invalid player type.")

def simple_random_agent(grid):
    moves = ['l', 'r', 'u', 'd']
    return random.choice(moves)

game = Game2048()
game.play(simple_random_agent)

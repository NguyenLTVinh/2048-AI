import numpy as np
import random
from copy import deepcopy

class DFS_Agent:
    def __init__(self, depth_limit=6):
        self.depth_limit = depth_limit
        self.best_move = 'l'
        self.directions = ['l', 'r', 'u', 'd']

    def heuristic(self, grid):
        """
        Heuristic function to evaluate the game state.
        Prioritizes states with high-value tiles and more free tiles.
        """
        empty_tiles = len(grid[grid == 0])
        max_tile = np.max(grid)
        return empty_tiles + np.log2(max_tile)

    def dfs(self, grid, depth=0):
        """
        Depth-first search algorithm to explore game states and choose the best move.
        """
        if depth == self.depth_limit or Game2048(grid=grid).game_over():
            return self.heuristic(grid)

        max_score = float('-inf')
        for direction in self.directions:
            new_grid = deepcopy(grid)
            game = Game2048(grid=new_grid)
            game.move(direction)
            if not np.array_equal(new_grid, game.grid):  # If the move changes the grid
                score = self.dfs(game.grid, depth + 1)
                if score > max_score:
                    max_score = score
                    if depth == 0:
                        self.best_move = direction

        return max_score

    def get_move(self, grid):
        """
        Determines the best move based on DFS exploration.
        """
        self.dfs(grid)
        return self.best_move

class Game2048:
    def __init__(self, grid=None):
        if grid is None:
            self.grid = np.zeros((4, 4), dtype=int)
            self.add_number()
            self.add_number()
        else:
            self.grid = grid

    def add_number(self):
        available_positions = list(zip(*np.where(self.grid == 0)))
        if available_positions:
            row, col = random.choice(available_positions)
            self.grid[row, col] = random.choice([2, 4])

    # Include the rest of the Game2048 class implementation as provided...

def dfs_agent(grid):
    agent = DFS_Agent()
    return agent.get_move(grid)

# To play the game with the DFS-based agent:
game = Game2048()
game.play(dfs_agent)

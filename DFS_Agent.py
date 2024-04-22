import numpy as np
from game import Game2048
from copy import deepcopy

class DFS_Agent:
    def __init__(self, depth_limit=6):
        self.depth_limit = depth_limit
        self.best_move = 'l'
        self.directions = ['l', 'r', 'u', 'd']

    def heuristic(self, grid):
        empty_tiles = len(grid[grid == 0])
        max_tile = np.max(grid)
        return empty_tiles + np.log2(max_tile)

    def dfs(self, game, depth=0):
        if depth == self.depth_limit or game.game_over():
            return self.heuristic(game.grid)

        max_score = float('-inf')
        original_grid = game.grid.copy()
        for direction in self.directions:
            game.grid = original_grid.copy()
            game.move(direction)
            if not np.array_equal(original_grid, game.grid):
                score = self.dfs(Game2048(grid=game.grid.copy()), depth + 1)
                if score > max_score:
                    max_score = score
                    if depth == 0:
                        self.best_move = direction
        game.grid = original_grid
        return max_score
    
    def get_move(self, grid):
        self.dfs(Game2048(grid=grid.copy()))
        return self.best_move
    
def dfs_agent(grid):
    agent = DFS_Agent()
    return agent.get_move(grid)

game = Game2048()
game.play(dfs_agent)

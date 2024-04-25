import numpy as np
import random
from game import Game2048
from math import log, sqrt

class MCTSNode:
    def __init__(self, game, parent=None, move=None):
        self.game = game
        self.parent = parent
        self.move = move
        self.wins = 0
        self.visits = 0
        self.children = []
        self.untried_moves = game.get_possible_moves()
        if move is not None:
            self.game.move(move, add_new=False)  # Make move without adding a new number

    def select_child(self):
        # UCB1 formula
        log_total_visits = log(self.visits)
        return max(self.children, key=lambda child: child.wins / child.visits + sqrt(2 * log_total_visits / child.visits))

    def expand(self):
        move = self.untried_moves.pop()
        new_game = Game2048(self.game.grid.copy())
        child = MCTSNode(new_game, parent=self, move=move)
        self.children.append(child)
        return child

    def update(self, result):
        self.visits += 1
        self.wins += result

    def simulate(self):
        simulation_game = Game2048(self.game.grid.copy())
        while not simulation_game.game_over():
            possible_moves = simulation_game.get_possible_moves()
            move = self.choose_heuristic_move(simulation_game, possible_moves)
            simulation_game.move(move, add_new=True)
        return simulation_game.get_score()

    def choose_heuristic_move(self, game, possible_moves):
        best_move = None
        best_score = -1
        for move in possible_moves:
            game_copy = Game2048(game.grid.copy())
            game_copy.move(move, add_new=False)
            score = game_copy.get_score()
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

class MCTSAgent:
    def __init__(self, iterations=100):
        self.iterations = iterations

    def get_move(self, game):
        root = MCTSNode(Game2048(game.grid.copy()))

        for _ in range(self.iterations):
            node = root
            # Selection
            while node.children and node.untried_moves == []:
                node = node.select_child()

            # Expansion
            if node.untried_moves:
                node = node.expand()

            # Simulation
            score = node.simulate()

            # Backpropagation
            while node:
                node.update(score)
                node = node.parent

        return max(root.children, key=lambda c: c.visits).move

def mcts_agent(grid):
    game_instance = Game2048(grid=grid.copy())
    agent = MCTSAgent()
    return agent.get_move(game_instance)

# game = Game2048()
# game.play(mcts_agent)

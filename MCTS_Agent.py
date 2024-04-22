import numpy as np
import random
from game import Game2048
from copy import deepcopy

class MCTSNode:
    def __init__(self, game, parent=None, move=None):
        self.game = deepcopy(game)
        if move is not None:
            self.game.move(move)
        self.parent = parent
        self.move = move
        self.wins = 0
        self.visits = 0
        self.children = []
        self.untried_moves = game.get_possible_moves()

    def select_child(self):
        # UCB1 formula
        from math import log, sqrt
        log_total_visits = log(self.visits)
        return max(self.children, key=lambda child: child.wins / child.visits + sqrt(2 * log_total_visits / child.visits))

    def expand(self):
        move = self.untried_moves.pop()
        child = MCTSNode(self.game, parent=self, move=move)
        self.children.append(child)
        return child

    def update(self, result):
        self.visits += 1
        self.wins += result

    def simulate(self):
        temp_game = deepcopy(self.game)
        while not temp_game.game_over():
            possible_moves = temp_game.get_possible_moves()
            move = random.choice(possible_moves)
            temp_game.move(move)
        return temp_game.get_score()

class MCTSAgent:
    def __init__(self, iterations=100):
        self.iterations = iterations

    def get_move(self, game):
        root = MCTSNode(game)

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

        # Return the move of the child with the highest score
        return max(root.children, key=lambda c: c.visits).move

def mcts_agent(grid):
    game_instance = Game2048(grid=grid.copy())
    agent = MCTSAgent()
    return agent.get_move(game_instance)

game = Game2048()
game.play(mcts_agent)

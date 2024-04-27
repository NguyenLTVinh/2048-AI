import numpy as np
#import matplotlib.pyplot as plt
from game import Game2048
from DFS_Agent import dfs_agent
from MCTS_Agent import mcts_agent
from game import simple_random_agent
import csv
import time

def simulate_game(agent, csv_name, num_simulations=500):
    with open(csv_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Run Number", "Score", "Move Count", "Max Tile", "Win"])
    scores = []
    moves_counts = []
    max_tiles = []
    wins = 0

    for i in range(num_simulations):
        print(f"Running simulation {i + 1}/{num_simulations}...")
        game = Game2048()
        move_count = 0
        win = False
        while not game.game_over():
            grid_copy = game.grid.copy()
            move = agent(grid_copy)
            game.move(move)
            move_count += 1
            if np.max(game.grid) == 2048:
                win = True
                wins += 1
                break
        scores.append(game.get_score())
        moves_counts.append(move_count)
        max_tiles.append(np.max(game.grid))
        with open(csv_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([i + 1, game.get_score(), move_count, np.max(game.grid), win])

    return {
        "average_score": np.mean(scores),
        "win_rate": wins / num_simulations,
        "average_moves": np.mean(moves_counts),
        "max_tile_distribution": np.unique(max_tiles, return_counts=True)
    }

# def plot_results(results, agents):
#     fig, axs = plt.subplots(2, 2, figsize=(10, 10))
#     fig.suptitle("2048 Game AI Agent Evaluation")

#     # Plot average scores
#     scores = [result["average_score"] for result in results]
#     axs[0, 0].bar(agents, scores)
#     axs[0, 0].set_title("Average Score")

#     # Plot win rates
#     win_rates = [result["win_rate"] for result in results]
#     axs[0, 1].bar(agents, win_rates)
#     axs[0, 1].set_title("Win Rate")

#     # Plot average moves
#     moves = [result["average_moves"] for result in results]
#     axs[1, 0].bar(agents, moves)
#     axs[1, 0].set_title("Average Moves Per Game")

#     # Plot max tile distributions
#     colors = ['green', 'red', 'blue']
#     for idx, result in enumerate(results):
#         tiles, counts = result["max_tile_distribution"]
#         axs[1, 1].bar(tiles + 0.2 * (idx - 1), counts, width=0.2, label=f"{agents[idx]}", color=colors[idx])
#     axs[1, 1].set_title("Max Tile Distribution")
#     axs[1, 1].legend()

#     plt.tight_layout(rect=[0, 0.03, 1, 0.95])
#     plt.savefig("2048_AI_Evaluation.png")
#     plt.close()

def main():
    runtimes = []
    agents = ["SRA", "DFS", "MCTS"]
    results = []

    for agent, filename in zip([simple_random_agent, dfs_agent, mcts_agent], ['sra_result.csv', 'dfs_result.csv', 'mcts_result.csv']):
        start_time = time.time()
        result = simulate_game(agent, filename)
        end_time = time.time()
        runtimes.append(end_time - start_time)
        results.append(result)

    for agent, runtime in zip(agents, runtimes):
        print(f"{agent} took {runtime:.2f} seconds.")

    #plot_results(results, agents) will do this after all csv files are run. We will run 250 iterations each on each computer.

if __name__ == "__main__":
    main()

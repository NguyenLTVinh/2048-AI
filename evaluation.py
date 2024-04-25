import numpy as np
import matplotlib.pyplot as plt
from game import Game2048
from DFS_Agent import dfs_agent
from MCTS_Agent import mcts_agent
from game import simple_random_agent

def simulate_game(agent, num_simulations=1000):
    scores = []
    moves_counts = []
    max_tiles = []
    wins = 0

    for i in range(num_simulations):
        print(f"Running simulation {i + 1}/{num_simulations}...")
        game = Game2048()
        move_count = 0
        while not game.game_over():
            grid_copy = game.grid.copy()
            move = agent(grid_copy)
            game.move(move)
            move_count += 1
            if np.max(game.grid) == 2048:
                wins += 1
                break
        scores.append(game.get_score())
        moves_counts.append(move_count)
        max_tiles.append(np.max(game.grid))

    return {
        "average_score": np.mean(scores),
        "win_rate": wins / num_simulations,
        "average_moves": np.mean(moves_counts),
        "max_tile_distribution": np.unique(max_tiles, return_counts=True)
    }

def plot_results(results, agents):
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    fig.suptitle("2048 Game AI Agent Evaluation")

    # Plot average scores
    scores = [result["average_score"] for result in results]
    axs[0, 0].bar(agents, scores)
    axs[0, 0].set_title("Average Score")

    # Plot win rates
    win_rates = [result["win_rate"] for result in results]
    axs[0, 1].bar(agents, win_rates)
    axs[0, 1].set_title("Win Rate")

    # Plot average moves
    moves = [result["average_moves"] for result in results]
    axs[1, 0].bar(agents, moves)
    axs[1, 0].set_title("Average Moves Per Game")

    # Plot max tile distributions
    colors = ['green', 'red']
    for idx, result in enumerate(results):
        tiles, counts = result["max_tile_distribution"]
        axs[1, 1].bar(tiles + 0.2 * (idx - 1), counts, width=0.2, label=f"{agents[idx]}", color=colors[idx])
    axs[1, 1].set_title("Max Tile Distribution")
    axs[1, 1].legend()

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("2048_AI_Evaluation.png")
    plt.close()

def main():
    dfs_results = simulate_game(dfs_agent)
    mcts_results = simulate_game(mcts_agent)
    sra_results = simulate_game(simple_random_agent)

    results = [sra_results, dfs_results, mcts_results]
    agents = ["DFS", "MCTS"]
    plot_results(results, agents)

if __name__ == "__main__":
    main()

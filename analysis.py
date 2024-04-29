import pandas as pd
import glob
import scipy.stats as stats
import os

def add_algorithm_column(file_path):
    df = pd.read_csv(file_path)
    algorithm_name = os.path.basename(file_path).split('_')[0]
    df['algorithm'] = algorithm_name
    return df

file_path_pattern = './results/*_result*.csv'

all_files = glob.glob(file_path_pattern)

if not all_files:
    raise ValueError("No CSV files found. Check your file path and permissions.")

combined_csv = pd.concat([add_algorithm_column(f) for f in all_files])

max_tile_value = combined_csv['Max Tile'].max()
bins = [2**x for x in range(1, 12)]
combined_csv['Max Tile Bin'] = pd.cut(combined_csv['Max Tile'], bins + [float('inf')], right=False, labels=bins)
tile_distribution = combined_csv.groupby(['algorithm', 'Max Tile Bin']).size().unstack(fill_value=0)
print(tile_distribution)

grouped_data = combined_csv.groupby('algorithm')['Score']
mean_values = grouped_data.mean()
std_dev_values = grouped_data.std()

if 'DFS_Agent' in combined_csv['algorithm'].unique() and 'MCTS_Agent' in combined_csv['algorithm'].unique():
    t_stat, p_value = stats.ttest_ind(
        combined_csv[combined_csv['algorithm'] == 'DFS_Agent']['Score'],
        combined_csv[combined_csv['algorithm'] == 'MCTS_Agent']['Score']
    )
    print("\nT-test between dfs and mcts for 'Score': T-statistic =", t_stat, ", P-value =", p_value)

print("\nMeans for 'Score':\n", mean_values)
print("\nStandard Deviations for 'Score':\n", std_dev_values)

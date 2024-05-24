from modules.environment.simulation import Simulation
import matplotlib.pyplot as plt
import pygame
import os

# Set the window position before initializing Pygame
x, y = 50, 100   # Set the desired window position
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"

def run_n_simulations(n_sims, strategies, render=None):
    i = 0
    first_catch_arr = []
    num_catches_arr = []
    prey_caught_count = []
    s = Simulation(adv_strategy=strategies[0], ag_strategy=strategies[1], render=render)
    while i < n_sims:
        print('Simulation:', i)
        first_catch, total_adv_reward, num_catches = s.run()
        first_catch_arr.append(first_catch)
        num_catches_arr.append(num_catches)
        if first_catch != -1:
            prey_caught_count.append(1)
        else:
            prey_caught_count.append(0)
        s.reset()
        i += 1
        print('First catch:', first_catch,'Total reward:', total_adv_reward, 'Number of catches:', num_catches)
    return first_catch_arr, num_catches_arr, prey_caught_count

def boxplot(datasets: list[list[int]], title: str, xlabels: list[str]):
    fig, ax = plt.subplots()
    ax.boxplot(datasets)
    ax.set_xticklabels(xlabels)
    plt.title(title)
    plt.show()

def bar_chart_percentage(datasets: list[list[int]], title: str, xlabels: list[str]):
    percentages = [(sum(data) / len(data)) * 100 for data in datasets]
    sorted_data = sorted(zip(percentages, xlabels), reverse=True)
    sorted_percentages, sorted_xlabels = zip(*sorted_data)
    fig, ax = plt.subplots()
    ax.barh(sorted_xlabels, sorted_percentages)
    ax.set_xlabel('Percentage of Games Prey Caught (%)')
    ax.set_title(title)
    plt.show()

def run_n_simulation_strategies_with_boxplots(n_sims: int, strategies_list: list[tuple[str]]):
    first_catch_dataset = []
    num_catches_dataset = []
    prey_caught_count_dataset = []
    for strategies in strategies_list:
        fc, nc, prey_caught_count = run_n_simulations(n_sims, strategies)
        first_catch_dataset.append(fc)
        num_catches_dataset.append(nc)
        prey_caught_count_dataset.append(prey_caught_count)
    xlabels = [f"{strategies[0]}+{strategies[1]}" for strategies in strategies_list]
    boxplot(first_catch_dataset, f"Number of steps until first catch N={n_sims}", xlabels)
    boxplot(num_catches_dataset, f"Number of catches, N={n_sims}", xlabels)
    bar_chart_percentage(prey_caught_count_dataset, f"Percentage of Games Prey Caught, N={n_sims}", xlabels)

if __name__ == "__main__":
    pygame.display.set_mode((50, 50))
    # run_n_simulations(10, ('greedy', 'bounded'), render='human')
    run_n_simulation_strategies_with_boxplots(100, [('random','bounded'), ('greedy','bounded'),('surround','bounded'),('intercept','bounded'), ('distract_pursue','bounded'), ('q_learning','bounded')])

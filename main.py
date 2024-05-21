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
    s = Simulation(adv_strategy=strategies[0], ag_strategy=strategies[1], render=render)
    while i < n_sims:
        first_catch, num_catches = s.run()
        first_catch_arr.append(first_catch)
        num_catches_arr.append(num_catches)
        s.reset()
        i += 1
    return first_catch_arr, num_catches_arr


def boxplot(datasets: list[list[int]], title: str, xlabels: list[str]):
    fig, ax = plt.subplots()
    ax.boxplot(datasets)
    ax.set_xticklabels(xlabels)
    plt.title(title)
    plt.show()


def run_n_simulation_strategies_with_boxplots(n_sims: int, strategies_list: list[tuple[str]]):
    first_catch_dataset = []
    num_catches_dataset = []
    for strategies in strategies_list:
        fc, nc = run_n_simulations(n_sims, strategies)
        first_catch_dataset.append(fc)
        num_catches_dataset.append(nc)
    xlabels = strategies[0] + '+' + strategies[1]
    boxplot(first_catch_dataset, f"Number of steps until first catch N={n_sims}", strategies_list)
    boxplot(num_catches_dataset, f"Number of catches, N={n_sims}", strategies_list)


if __name__ == "__main__":    
    pygame.display.set_mode((50, 50))
    run_n_simulations(1, ('greedy', 'bounded'), render='human')
    # run_n_simulation_strategies_with_boxplots(50, [('greedy','bounded'),('surround','bounded'),('intercept','bounded')])
    
    



from modules.environment.simulation import Simulation
import pygame
import os
# Set the window position before initializing Pygame
x, y = 50, 100   # Set the desired window position
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"
if __name__ == "__main__":    
    N_SIMS = 1
    i = 0
    s = Simulation(adv_strategy='greedy', ag_strategy='bounded', render='human')
    pygame.display.set_mode((100, 100))
    while i < N_SIMS:
        print(f"Simulation {i}/{N_SIMS}")
        first_catch, num_catches = s.run()
        print(f'first_catch:{first_catch}\nnum_catches: {num_catches}')
        s.reset()
        i += 1



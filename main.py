from modules.environment.simulation import Simulation
if __name__ == "__main__":    
    N_SIMS = 1
    i = 0
    s = Simulation(strategy='greedy', render='human')
    while i < N_SIMS:
        print(f"Simulation {i}/{N_SIMS}")
        first_catch, num_catches = s.run()
        print(f'first_catch:{first_catch}\nnum_catches: {num_catches}')
        s.reset()
        i += 1



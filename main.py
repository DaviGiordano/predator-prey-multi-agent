from modules.simulation import Simulation
if __name__ == "__main__":    
    N_SIMS = 10
    i = 0
    s = Simulation(strategy='random')
    while i < N_SIMS:
        print(f"Simulation {i}/{N_SIMS}")
        print(s.run())
        s.reset()
        i += 1



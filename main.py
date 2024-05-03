from modules.simulation import Simulation

N_SIMS = 10
i = 0
s = Simulation(strategy='random')
while i < N_SIMS:
    print(f"Simulation {i}/{N_SIMS}")
    print(s.run())
    s.reset()
    i += 1


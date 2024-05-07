from modules.actors.agents import BaseAgent
from modules.actors.constants import action_codes as act
import math

class ClosestAgent(BaseAgent):
    def __init__(self, id, initial_observation):
        super().__init__(id, initial_observation)

    def get_action(self):

        xb = self.last_observation['adv0_relpos_x']
        yb = self.last_observation['adv0_relpos_y']
        
        best_dist = math.sqrt(xb**2 + yb**2)

        #find closest adversary
        for i in range(1, 3):
            xi = self.last_observation[f'adv{i}_relpos_x']
            yi = self.last_observation[f'adv{i}_relpos_y']

            #compare adversary i with best
            dist_i = math.sqrt(xi**2 + yi**2)
            if dist_i < best_dist:
                best_dist = dist_i
                xb = xi
                yb = yi
        
        #now move furthest away from closest adversary
        if abs(xb) < abs(yb): # Horizontal distance is smaller
            if xb < 0:  # Adv is to the left
                action = act['move_right']
            elif xb > 0:  # Adv is to the right
                action = act['move_left']
        else:
            if yb < 0:  # Adv is below
                action = act['move_up']
            elif yb > 0:  # Adv is above
                action = act['move_down']
        return action
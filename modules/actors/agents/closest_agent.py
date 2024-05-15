from modules.actors.agents import BaseAgent
from modules.actors.utils import action_codes as act

class ClosestAgent(BaseAgent):
    def __init__(self, id, initial_observation):
        super().__init__(id, initial_observation)

    def get_action(self):
        
        print("self.last_observation['pos_x']",self.last_observation['pos_x'])
        print("self.last_observation['pos_y']",self.last_observation['pos_y'])
        print("sum(self.reward_history)",sum(self.reward_history))

        xb = self.last_observation['adv0_relpos_x']
        yb = self.last_observation['adv0_relpos_y']
        best_dist = abs(xb) + abs(yb)



        #find closest adversary
        for i in range(1, 3):
            xi = self.last_observation[f'adv{i}_relpos_x']
            yi = self.last_observation[f'adv{i}_relpos_y']

            #compare adversary i with best
            dist_i = abs(xi) + abs(yi)
            
            if dist_i < best_dist:
                best_dist = dist_i
                xb = xi
                yb = yi
        
        #now move furthest away from closest adversary
        if abs(xb) > abs(yb): # Horizontal distance is smaller
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
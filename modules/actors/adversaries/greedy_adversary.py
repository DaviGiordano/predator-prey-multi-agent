from modules.actors.adversaries import BaseAdversary
from modules.actors.constants import action_codes as act
class GreedyAdversary(BaseAdversary):
    ''' ... '''
    def __init__(self, id, initial_observation):
        super().__init__(id, initial_observation)

    def get_action(self):
        # Calculate distance from prey using last observations
        # Choose action of direction that minimizes the distance

        dx = self.last_observation['ag_relpos_x']
        dy = self.last_observation['ag_relpos_y']
        action = act['no_action']

        if abs(dx) > abs(dy): # Horizontal distance is bigger
            if dx < 0:  # Prey is to the left
                action = act['move_left']
            elif dx > 0:  # Prey is to the right
                action = act['move_right']
        else:
            if dy < 0:  # Prey is below
                action = act['move_down']
            elif dy > 0:  # Prey is above
                action = act['move_up']
        if abs(dx) < 0. and abs(dy) < 0.1:
            action = act['no_action']
        return action
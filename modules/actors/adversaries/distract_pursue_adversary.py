from modules.actors.adversaries import BaseAdversary
from modules.actors.utils import action_codes as act
import math
from random import randint

class DistractPursueAdversary(BaseAdversary):

    def __init__(self, id, initial_observation):
        super().__init__(id, initial_observation)
        self.role = None


    def get_distance(self, x: tuple[int,int], y: tuple[int,int]): 
        return math.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)


    def get_role(self):
        prey = self.get_absolute_position('prey')
        adv = ['self', 'advA', 'advB']
        prey = self.get_absolute_position('prey')
        adv.sort(key=lambda x: self.get_distance(prey, self.get_absolute_position(x)))
        if adv[0] == 'self':
            self.role = 'Pursuer'
        else:
            self.role = 'Distractor'


    def get_action(self):
        if self.role == None:
            self.get_role()

        total_dist = self.get_distance(self.get_absolute_position('prey'), self.get_absolute_position('self'))

        if self.role == 'Distractor' and total_dist < 0.3:
            self.role = 'Random'

        if self.role == 'Random':
            if total_dist > 0.6:
                self.role = 'Distractor'
            else:
                return randint(0,4)
        

        dx = self.last_observation['ag_relpos_x']
        dy = self.last_observation['ag_relpos_y']
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
    

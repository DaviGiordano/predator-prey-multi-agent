from modules.actors.adversaries import BaseAdversary
from modules.actors.utils import action_codes as act
import math

class InterceptAdversary(BaseAdversary):

    def __init__(self, id, initial_observation, intercept_mult):
        super().__init__(id, initial_observation)
        self.intercept_range = None
        self.intercept_mult = intercept_mult


    def get_distance(self, x: tuple[int,int], y: tuple[int,int]): 
        return math.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)


    def get_prey_absolute_velocity(self):
        my_x = self.last_observation['vel_x']
        my_y = self.last_observation['vel_y']
        prey_x = self.last_observation['ag_relvel_x'] + my_x
        prey_y = self.last_observation['ag_relvel_y'] + my_y
        return (prey_x, prey_y)


    def get_intercept_range(self):
        adv = ['self', 'advA', 'advB']
        prey = self.get_absolute_position('prey')
        adv.sort(key=lambda x: self.get_distance(prey, self.get_absolute_position(x)))
        self.intercept_range = adv.index('self') * self.intercept_mult * 0.1


    def get_intercept_position(self): # eta=0.1
        prey_pos = self.last_observation['ag_relpos_x'], self.last_observation['ag_relpos_y']
        prey_vel = self.last_observation['ag_relvel_x'], self.last_observation['ag_relvel_y']
        return (prey_pos[0] + prey_vel[0] * self.intercept_range, prey_pos[1] + prey_vel[1] * self.intercept_range)


    def get_action(self):
        if self.intercept_range == None:
            self.get_intercept_range()

        dx, dy = self.get_intercept_position()
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

from modules.actors.agents import BaseAgent
from modules.actors.utils import action_codes as act
import numpy as np
import random
import math

class BoundedAgent(BaseAgent):
    def __init__(self, id, initial_observation):
        super().__init__(id, initial_observation)

        # In this class, numpy arrays always have the following structure:
        # UP, DOWN, LEFT, RIGHT

    def get_legal_moves(self):
        # Returns a dictionary of moves and 
        # whether they are legal (True) or not (False)
       
        x = self.last_observation['pos_x']
        y = self.last_observation['pos_y']

        return {
            'up': y < 0.9,
            'down': y > -0.9,
            'left': x > -0.9,
            'right': x < 0.9
        }	

    def get_distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def get_adv_direction(self, rel_x, rel_y):
        vertical_direction = 'up' if rel_y >= 0 else 'up'
        horizontal_direction = 'right' if rel_x >- 0 else 'left'
        return vertical_direction, horizontal_direction

    def get_nearest_agent_by_direction(self, distance_to_adv, direction_of_adv):
        pass        

    def get_action(self):
        
        move_legality = self.get_legal_moves()

        distance_to_adv = {
            'adv0': None,
            'adv1': None,
            'adv2': None
        }

        directions_of_adv = {
            'adv0': None,
            'adv1': None,
            'adv2': None
        }

        for i in range(3):
            distance_to_adv[f'adv{i}'] = self.get_distance(
                self.last_observation['pos_x'], self.last_observation['pos_y'],
                self.last_observation[f'adv{i}_relpos_x'], self.last_observation[f'adv{i}_relpos_y']
            )
        
            directions_of_adv[f'adv{i}'] = self.get_adv_direction(
                self.last_observation[f'adv{i}_relpos_x'],
                self.last_observation[f'adv{i}_relpos_y']
            )

        min_distances = {
            'up': 2, # 2 is the maximum distance (extension of the board)
            'down': 2,
            'left': 2,
            'right': 2
        }

        for i in range(3):
            if 'up' in directions_of_adv[f'adv{i}'] and distance_to_adv[f'adv{i}'] < min_distances['up']:
                min_distances['up'] = distance_to_adv[f'adv{i}']
            elif 'down' in directions_of_adv[f'adv{i}'] and distance_to_adv[f'adv{i}'] < min_distances['down']:
                min_distances['down'] = distance_to_adv[f'adv{i}']

            if 'left' in directions_of_adv[f'adv{i}'] and distance_to_adv[f'adv{i}'] < min_distances['left']:
                min_distances['left'] = distance_to_adv[f'adv{i}']
            elif 'right' in directions_of_adv[f'adv{i}'] and distance_to_adv[f'adv{i}'] < min_distances['right']:
                min_distances['right'] = distance_to_adv[f'adv{i}']
        
        print(move_legality, directions_of_adv, distance_to_adv, min_distances)

        distances = np.array([min_distances['up'], min_distances['down'], min_distances['left'], min_distances['right']])
        valid = np.array([move_legality['up'], move_legality['down'], move_legality['left'], move_legality['right']])

        masked_distances = np.where(valid, distances, 0)
        exp_distances = np.exp(masked_distances)

        # Normalize probabilities
        total = exp_distances.sum()
        if total > 0:
            act_prob = exp_distances / total
        else:
            act_prob = np.zeros_like(exp_distances)

        return random.choices([act['move_up'], act['move_down'], act['move_left'], act['move_right']], act_prob)[0]

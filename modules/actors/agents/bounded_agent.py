from modules.actors.agents import BaseAgent
from modules.actors.utils import action_codes as act
import random

class BoundedAgent(BaseAgent):
    def __init__(self, id, initial_observation):
        super().__init__(id, initial_observation)

    def get_action(self):
        
        x = self.last_observation['pos_x']
        y = self.last_observation['pos_y']
        print("sum(self.reward_history)", sum(self.reward_history))

        # Array of probabilities for each action
        p = [0.2 for _ in range(5)]

        # Dictionary of relative distances to closest adversaries in each direction
        min_distances = {
            'up': -1,
            'down': -1,
            'left': -1,
            'right': -1
        }

        # Check closest adversaries
        for i in range(3):  # Assuming there are 3 adversaries
            xi = self.last_observation[f'adv{i}_relpos_x']
            yi = self.last_observation[f'adv{i}_relpos_y']

            if yi > 0:  # Adversary is above
                if min_distances['up'] == -1 or yi < min_distances['up']:
                    min_distances['up'] = abs(yi)
            elif yi < 0:  # Adversary is below
                if min_distances['down'] == -1 or -yi < min_distances['down']:
                    min_distances['down'] = abs(yi)
            if xi < 0:  # Adversary is to the left
                if min_distances['left'] == -1 or -xi < min_distances['left']:
                    min_distances['left'] = abs(xi)
            elif xi > 0:  # Adversary is to the right
                if min_distances['right'] == -1 or xi < min_distances['right']:
                    min_distances['right'] = abs(xi)

        # Adjust probabilities based on the proximity of adversaries
        max_distance = 1.8

        p[act['move_down']] = max_distance if min_distances['down'] == -1 else min_distances['down']
        p[act['move_up']] = max_distance if min_distances['up'] == -1 else min_distances['up']
        p[act['move_right']] = max_distance if min_distances['right'] == -1 else min_distances['right']
        p[act['move_left']] = max_distance if min_distances['left'] == -1 else min_distances['left']

        # Check bounds
        if x > 0.9:
            p[act['move_right']] = 0
        elif x < -0.9:
            p[act['move_left']] = 0
        
        if y > 0.9:
            p[act['move_up']] = 0
        elif y < -0.9:
            p[act['move_down']] = 0

        # Normalize probabilities
        total_p = sum(p)
        if total_p > 0:
            p = [prob / total_p for prob in p]

        # Choose an action based on the probabilities
        action = random.choices([act['no_action'], act['move_left'], act['move_right'], act['move_down'], act['move_up']], p)[0]

        return action

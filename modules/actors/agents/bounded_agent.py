from modules.actors.agents import BaseAgent
from modules.actors.utils import action_codes as act
import random

class BoundedAgent(BaseAgent):
    def __init__(self, id, initial_observation):
        super().__init__(id, initial_observation)

    def get_action(self):
        
        x = self.last_observation['pos_x']
        y = self.last_observation['pos_y']
        print("sum(self.reward_history)",sum(self.reward_history))

        #array of probabilities for each action
        p = [0.2 for _ in range(5)]

        #arrys of relative distances to closest advsersaries in each direction
        adv = [0 for _ in range(4)]        

        # check closest adversaries
        for i in range(3):
            xi = self.last_observation[f'adv{i}_relpos_x']
            yi = self.last_observation[f'adv{i}_relpos_y']

            if yi > 0:  # Adversary is above
                if adv[0] == -1 or yi < adv[0]:
                    adv[0] = abs(yi)
            elif yi < 0:  # Adversary is below
                if adv[1] == -1 or -yi < adv[1]:
                    adv[1] = abs(yi)
            if xi < 0:  # Adversary is to the left
                if adv[2] == -1 or -xi < adv[2]:
                    adv[2] = abs(xi)
            elif xi > 0:  # Adversary is to the right
                if adv[3] == -1 or xi < adv[3]:
                    adv[3] = abs(xi)

        # Adjust probabilities based on the proximity of adversaries
        max_distance = 1.8

        if adv[0] != -1:  # Adversary above
            p[3] += (max_distance - adv[0]) / max_distance  # Increase prob of moving down
        if adv[1] != -1:  # Adversary below
            p[4] += (max_distance - adv[1]) / max_distance  # Increase prob of moving up
        if adv[2] != -1:  # Adversary to the left
            p[2] += (max_distance - adv[2]) / max_distance  # Increase prob of moving right
        if adv[3] != -1:  # Adversary to the right
            p[1] += (max_distance - adv[3]) / max_distance  # Increase prob of moving left

        #check bounds
        if x > 0.9:
            p[2] = 0
        elif x < -0.9:
            p[1] = 0
        
        if y > 0.9:
            p[4] = 0
        elif y < -0.9:
            p[3] = 0

        # Normalize probabilities
        total_p = sum(p)
        if total_p > 0:
            p = [prob / total_p for prob in p]

        # Choose an action based on the probabilities
        action = random.choices([act['no_action'], act['move_left'], act['move_right'], act['move_down'], act['move_up']], p)[0]

        return action
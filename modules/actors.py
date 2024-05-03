from modules.constants import action_codes
from random import randint

#################################################################

class DefaultActor:
    ''' Parent class for both predators and prey '''
    def __init__(self, id, initial_observation):
        self.id = id
        self.last_observation = None
        self.parse_observation(initial_observation)
        self.observation_history = []
        self.action_history = []
        self.reward_history = []


    def get_action(self):
        return action_codes['no_action']


    def update(self, observation, action, reward):
        self.parse_observation(observation)
        self.observation_history.append(self.last_observation)
        self.action_history.append(action) 
        self.reward_history.append(reward)


#################################################################
#                       AGENTS
#################################################################

class DefaultAgent(DefaultActor):
    ''' Default prey class '''
    def __init__(self, id, initial_observation):
        super().__init__(id, initial_observation)

    def parse_observation(self, observation):
        # Now properly overriding the parent class method
        self.last_observation = {
            'vel_x': observation[0],
            'vel_y': observation[1],
            'pos_x': observation[2],
            'pos_y': observation[3],
            'land1_relpos_x': observation[4],
            'land1_relpos_y': observation[5],
            'land2_relpos_x': observation[6],
            'land2_relpos_y': observation[7],
            'adv0_relpos_x': observation[8],
            'avd0_relpos_y': observation[9],
            'adv1_relpos_x': observation[10],
            'avd1_relpos_y': observation[11],
            'adv2_relpos_x': observation[12],
            'avd2_relpos_y': observation[13]
        }

#################################################################

class RandomAgent(DefaultAgent):
    ''' Prey walks randomly '''
    def __init__(self, id, initial_observation):
        super().__init__(id, initial_observation)

    def get_action(self):
        return randint(0,4)


#################################################################
#                      Adversaries
#################################################################

class DefaultAdversary(DefaultActor):
    ''' Default predator class'''
    def __init__(self, id, initial_observation):
        super().__init__(id, initial_observation)

    def parse_observation(self, observation):
        self.last_observation = {
            'vel_x': observation[0],
            'vel_y': observation[1],
            'pos_x': observation[2],
            'pos_y': observation[3],
            'land1_relpos_x': observation[4],
            'land1_relpos_y': observation[5],
            'land2_relpos_x': observation[6],
            'land2_relpos_y': observation[7],
            'advA_relpos_x': observation[8],
            'avdA_relpos_y': observation[9],
            'advB_relpos_x': observation[10],
            'avdB_relpos_y': observation[11],
            'ag_relpos_x': observation[12],
            'ag_relpos_y': observation[13],
            'ag_relvel_x': observation[14],
            'ag_relvel_y': observation[15],
        }

#################################################################

class RandomAdversary(DefaultAdversary):
    ''' Predator walks randomly '''
    def __init__(self, id, initial_observation):
        super().__init__(id, initial_observation)

    def get_action(self):
        return randint(0,4)

#################################################################

class GreedyAdversary(DefaultAdversary):
    ''' ... '''
    def __init__(self, id, initial_observation):
        super().__init__(id, initial_observation)

    def get_action(self):
        # Calculate distance from prey using last observations
        # Choose action of direction that minimizes the distance
        raise NotImplementedError



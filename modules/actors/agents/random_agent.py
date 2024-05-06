from modules.actors.agents import BaseAgent
from random import randint

class RandomAgent(BaseAgent):
    ''' Prey walks randomly '''
    def __init__(self, id, initial_observation):
        super().__init__(id, initial_observation)

    def get_action(self):
        return randint(0,4)

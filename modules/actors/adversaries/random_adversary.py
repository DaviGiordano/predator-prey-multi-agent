from modules.actors.adversaries import BaseAdversary
from random import randint

class RandomAdversary(BaseAdversary):
    ''' Predator walks randomly '''
    def __init__(self, id, initial_observation):
        super().__init__(id, initial_observation)

    def get_action(self):
        return randint(0,4)

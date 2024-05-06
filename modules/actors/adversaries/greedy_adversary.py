from modules.actors.adversaries import BaseAdversary

class GreedyAdversary(BaseAdversary):
    ''' ... '''
    def __init__(self, id, initial_observation):
        super().__init__(id, initial_observation)

    def get_action(self):
        # Calculate distance from prey using last observations
        # Choose action of direction that minimizes the distance
        raise NotImplementedError


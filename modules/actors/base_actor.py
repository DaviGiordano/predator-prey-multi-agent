from modules.actors.utils import action_codes

class BaseActor:
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

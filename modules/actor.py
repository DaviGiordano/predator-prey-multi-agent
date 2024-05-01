class Actor:
    def __init__(self, actor_id, initial_observation) -> None:
        self.agent_id = actor_id
        self.observation = None
        self.parse_observation(initial_observation)

    def parse_observation(self, observation):
        pass

    def get_action(self):
        pass    
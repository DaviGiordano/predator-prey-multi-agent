from modules.actor import Actor

class DefaultAgent(Actor):
    def __init__(self, actor_id, initial_observation):
        super().__init__(actor_id, initial_observation)

    def parse_observation(self, observation):
        # Now properly overriding the parent class method
        self.observation = {
            'vel_x': observation[0],
            'vel_y': observation[1],
            'pos_x': observation[2],
            'pos_y': observation[3],
            'land1_x': observation[4],
            'land1_y': observation[5],
            'land2_x': observation[6],
            'land2_y': observation[7],
            'adv1_relpos_x': observation[8],
            'avd2_relpos_y': observation[9],
            'adv1_relpos_x': observation[10],
            'avd2_relpos_y': observation[11],
            'adv1_relpos_x': observation[12],
            'avd2_relpos_y': observation[13]
        }

    def get_action(self):
        # Implement action logic based on self.observation
        pass

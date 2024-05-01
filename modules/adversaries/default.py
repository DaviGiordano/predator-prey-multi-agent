from modules.actor import Actor

class DefaultAdversary(Actor):
    def __init__(self, agent_id, initial_observation):
        super().__init__(agent_id, initial_observation)

    def parse_observation(self, observation):
        self.observation = {
            'vel_x': observation[0],
            'vel_y': observation[1],
            'pos_x': observation[2],
            'pos_y': observation[3],
            'land1_x': observation[4],
            'land1_y': observation[5],
            'land2_x': observation[6],
            'land2_y': observation[7],
            'advA_relpos_x': observation[8],
            'avdA_relpos_y': observation[9],
            'advB_relpos_x': observation[10],
            'avdB_relpos_y': observation[11],
            'ag_relpos_x': observation[12],
            'ag_relpos_y': observation[13],
            'ag_relvel_x': observation[14],
            'ag_relvel_y': observation[15],
        }

    def get_action(self):
        # Example: Decide action based on observations
        observations = self.parse_observation()
        if observations['vel_y'] > 0:
            return "Move Up"
        else:
            return "Move Down"
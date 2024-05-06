from modules.actors.base_actor import BaseActor


class BaseAgent(BaseActor):
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
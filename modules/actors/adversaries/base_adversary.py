from modules.actors.base_actor import BaseActor

class BaseAdversary(BaseActor):
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
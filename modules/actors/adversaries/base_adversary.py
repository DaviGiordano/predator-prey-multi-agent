from modules.actors.base_actor import BaseActor
import math

class BaseAdversary(BaseActor):
    ''' Default predator class'''
    def __init__(self, id, initial_observation):
        super().__init__(id, initial_observation)

    def parse_observation(self, observation):
        last_observation = {
            'vel_x': observation[0],
            'vel_y': observation[1],
            'pos_x': observation[2],
            'pos_y': observation[3],
            'land1_relpos_x': observation[4],
            'land1_relpos_y': observation[5],
            'land2_relpos_x': observation[6],
            'land2_relpos_y': observation[7],
            'advA_relpos_x': observation[8],
            'advA_relpos_y': observation[9],
            'advB_relpos_x': observation[10],
            'advB_relpos_y': observation[11],
            'ag_relpos_x': observation[12],
            'ag_relpos_y': observation[13],
            'ag_relvel_x': observation[14],
            'ag_relvel_y': observation[15],
        }
        return last_observation


    def get_absolute_position(self, actor):
        my_x = self.last_observation['pos_x']
        my_y = self.last_observation['pos_y']
        advA_x = self.last_observation['advA_relpos_x'] + my_x
        advA_y = self.last_observation['advA_relpos_y'] + my_y
        advB_x = self.last_observation['advB_relpos_x'] + my_x
        advB_y = self.last_observation['advB_relpos_y'] + my_y
        prey_x = self.last_observation['ag_relpos_x'] + my_x
        prey_y = self.last_observation['ag_relpos_y'] + my_y

        if actor == 'self':
            return my_x, my_y
        elif actor == 'advA':
            return advA_x, advA_y
        elif actor == 'advB':
            return advB_x, advB_y
        elif actor == 'prey':
            return prey_x, prey_y


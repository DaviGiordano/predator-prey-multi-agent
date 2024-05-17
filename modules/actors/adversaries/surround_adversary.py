from modules.actors.adversaries import BaseAdversary
from modules.actors.utils import action_codes as act
import logging
import numpy as np
import math

logging.basicConfig(filename='logfile.log', level=logging.INFO)

class SurroundAdversary(BaseAdversary):
    def __init__(self, id, initial_observation):
        super().__init__(id, initial_observation)
        self.roles = None

    def get_distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def get_triangle_vertices(self, follower_x, follower_y, prey_x, prey_y):
        """Given a first vertex (follower) and the centroid (prey),
        return the other two vertices of an equilateral triangle.

        Args:
        follower_x (float): x-coordinate of the known vertex.
        follower_y (float): y-coordinate of the known vertex.
        prey_x (float): x-coordinate of the centroid.
        prey_y (float): y-coordinate of the centroid.

        Returns:
        tuple: Contains two tuples, each representing the x and y coordinates of the other vertices.
        """
        # Cosine and sine of 60 degrees
        cos60 = 0.5
        sin60 = np.sqrt(3) / 2

        # Create rotation matrices for +60 and -60 degrees
        rotation_plus_60 = np.array([
            [cos60, -sin60],
            [sin60, cos60]
        ])
        rotation_minus_60 = np.array([
            [cos60, sin60],
            [-sin60, cos60]
        ])

        # Convert coordinates to numpy arrays
        follower = np.array([follower_x, follower_y])
        prey = np.array([prey_x, prey_y])

        # Calculate vector from centroid to the known vertex
        vector_ag = prey - follower

        # Apply rotations to find the other two vertices
        vertex_1 = prey + np.dot(rotation_plus_60, vector_ag)
        vertex_2 = prey + np.dot(rotation_minus_60, vector_ag)

        # Return the coordinates of the new vertices
        return (list(follower), list(vertex_1), list(vertex_2))

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


    def find_closest_to_target(self, target_x, target_y):
        distances_to_target = {'self': np.inf, 'advA': np.inf, 'advB': np.inf}
        
        distances_to_target['self'] = self.get_distance(
            self.last_observation['pos_x'], self.last_observation['pos_y'],
            target_x, target_y
            )

        advA_x = self.get_absolute_position('advA')[0]
        advA_y = self.get_absolute_position('advA')[1]
        distances_to_target['advA'] = self.get_distance(
            advA_x, advA_y,
            target_x, target_y
            )
        
        
        advB_x = self.get_absolute_position('advB')[0]
        advB_y = self.get_absolute_position('advB')[1]
        distances_to_target['advB'] = self.get_distance(
            advB_x, advB_y,
            target_x, target_y
            )
        return [k for k, v in sorted(distances_to_target.items(), key=lambda item: item[1])]

    def get_roles(self):
        roles = {'self': None, 'advA': None, 'advB': None}

        prey_x, prey_y = self.get_absolute_position('prey')

        closest_to_prey = self.find_closest_to_target(
            prey_x, prey_y
            )[0]
        roles[closest_to_prey] = 'prey'

        follower_x, follower_y = self.get_absolute_position(closest_to_prey)
        
        _, vertex_1, vertex_2 = self.get_triangle_vertices(
            follower_x, follower_y,
            prey_x, prey_y)
        
        order_closest_to_vertex_1 = self.find_closest_to_target(
            vertex_1[0], vertex_1[1]
            )
        
        order_closest_to_vertex_1.pop(order_closest_to_vertex_1.index(closest_to_prey))
        roles[order_closest_to_vertex_1[0]] = 'vertex_1'
        roles[order_closest_to_vertex_1[1]] = 'vertex_2'

        self.roles = roles

    def get_target(self):
        if self.roles['self'] == 'prey':
            return self.last_observation['ag_relpos_x'], self.last_observation['ag_relpos_y']
        else:
            # Recalculate vertices
            for adv, role in self.roles.items():
                if role == 'prey':
                    follower_x, follower_y = self.get_absolute_position(adv)
                    prey_x, prey_y = self.get_absolute_position('prey')
                    _, vertex_1, vertex_2 = self.get_triangle_vertices(
                    follower_x, follower_y,
                    prey_x, prey_y)
        if self.roles['self'] == 'vertex_1':
            return (vertex_1[0]-self.last_observation['pos_x']), (vertex_1[1]-self.last_observation['pos_y'])
        else:
            return (vertex_2[0]-self.last_observation['pos_x']), (vertex_2[1]-self.last_observation['pos_y'])


    def get_action(self):
        if self.roles == None:
            self.get_roles()

        dx, dy = self.get_target()

        logging.info(f"Adv w/ role {self.roles['self']} target:\n dx={dx}, dy={dy}\n{self.last_observation}")

        action = act['no_action']

        if abs(dx) > abs(dy): # Horizontal distance is bigger
            if dx < 0:  # Prey is to the left
                action = act['move_left']
            elif dx > 0:  # Prey is to the right
                action = act['move_right']
        else:
            if dy < 0:  # Prey is below
                action = act['move_down']
            elif dy > 0:  # Prey is above
                action = act['move_up']
        if abs(dx) < 0. and abs(dy) < 0.1:
            action = act['no_action']
        return action
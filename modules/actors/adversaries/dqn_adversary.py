from modules.actors.adversaries import BaseAdversary
from modules.actors.utils import action_codes
import numpy as np
import os
import torch
import torch.nn as nn
import torch.optim as optim
from random import randint, random

def get_distance_from_relpos(relpos_x, relpos_y):
    return np.sqrt(relpos_x**2 + relpos_y**2)

class QNetwork(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, output_dim)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

class DQNAdversary(BaseAdversary):
    ''' Predator learns using Q-learning'''
    def __init__(self, id, initial_observation, weights_path, alpha=0.001, gamma=0.99, epsilon=0.1):
        super().__init__(id, initial_observation)
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.num_actions = len(action_codes.values())
        self.input_dim = len(initial_observation)
        
        # Initialize Q-network and optimizer
        self.q_network = QNetwork(self.input_dim, self.num_actions)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=self.alpha)
        self.criterion = nn.MSELoss()

        # Create weights directory if it does not exist
        if not os.path.exists(weights_path):
            os.makedirs(weights_path)
        
        # Check for existing weights and load them if available
        self.weights_filepath = f"{weights_path}/weights_{id}.pth"
        if os.path.isfile(self.weights_filepath):
            self.load_weights(self.weights_filepath)

    def get_action(self):
        if random() < self.epsilon:
            return randint(0, self.num_actions - 1)
        state_tensor = torch.tensor([list(self.last_observation.values())], dtype=torch.float32)
        q_values = self.q_network(state_tensor)
        return torch.argmax(q_values).item()

    def update_q_network(self, state, action, reward, next_state):
        state_tensor = torch.tensor([list(state.values())], dtype=torch.float32)
        next_state_tensor = torch.tensor([list(next_state)], dtype=torch.float32)
        
        current_q_values = self.q_network(state_tensor)
        max_next_q_values = torch.max(self.q_network(next_state_tensor)).item()
        expected_q_values = current_q_values.clone()
        expected_q_values[0][action] = reward + self.gamma * max_next_q_values
        
        loss = self.criterion(current_q_values, expected_q_values)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def calculate_small_reward(self, observation, reward):
        previous_distance = get_distance_from_relpos(self.last_observation['ag_relpos_x'], self.last_observation['ag_relpos_y'])
        new_observation = self.parse_observation(observation)
        current_distance = get_distance_from_relpos(new_observation['ag_relpos_x'], new_observation['ag_relpos_y'])
        if (reward == 0) and (current_distance < previous_distance):
            reward = 1
        return reward
            

    def update(self, observation, action, reward):

        reward = self.calculate_small_reward(observation, reward)
        # print(f'New reward agent {self.id}: {reward}')
        self.update_q_network(self.last_observation, action, reward, observation)
        self.last_observation = self.parse_observation(observation)
        self.observation_history.append(self.last_observation)
        self.action_history.append(action)
        self.reward_history.append(reward)

    def save_weights(self, path):
        torch.save(self.q_network.state_dict(), path)
    
    def load_weights(self, path):
        self.q_network.load_state_dict(torch.load(path))
        self.q_network.eval()

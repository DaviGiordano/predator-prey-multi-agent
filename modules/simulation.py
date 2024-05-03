from pettingzoo.mpe import simple_tag_v3

from modules.actors import *

CYCLES = 25

class Simulation():

    def __init__(self, strategy='default', render=None):
        self.env = simple_tag_v3.parallel_env(num_good=1, num_adversaries=3, num_obstacles=2, max_cycles=CYCLES, continuous_actions=False, render_mode=render)
        self.observations, self.infos = self.env.reset()
        self.n_steps = 0

        if strategy == 'default':
            self.actors = {agent:DefaultAdversary(agent, self.observations[agent]) for agent in self.env.agents[:-1]}
            self.actors.update({'agent_0':DefaultAgent('agent_0', self.observations['agent_0'])})
        elif strategy == 'random':
            self.actors = {agent:RandomAdversary(agent, self.observations[agent]) for agent in self.env.agents[:-1]}
            self.actors.update({'agent_0':RandomAgent('agent_0', self.observations['agent_0'])})
#        elif strategy == 'greedy':
#            self.actors = {agent:GreedyAdversary(agent, self.observations[agent]) for agent in self.env.agents[:-1]}
#        ...
        else:
            raise NotImplementedError


    def reset(self):
        self.__init__()


    def total_reward_prey(self):
        return sum(self.actors['agent_0'].reward_history)


    def total_reward_predators(self):
        return sum(self.actors['adversary_0'].reward_history)


    def _step(self):
        actions = {actor: self.actors[actor].get_action() for actor in self.env.agents}
        observations, rewards, terminations, truncations, infos = self.env.step(actions)
        for actor in self.actors.keys():
            self.actors[actor].update(observations[actor], actions[actor], rewards[actor])
        self.n_steps += 1


    def run(self):
        while self.env.agents:
            self._step()
        self.env.close()
        if 10.0 in self['adversary_0'].reward_history:
            first_catch = self['adversary_0'].reward_history.index(10.0)
        else:
            first_catch = -1
        return (first_catch, self.total_reward_predators()/10)


    def __getitem__(self, name):
        return self.actors[name]



if __name__=='__main__':
    s = Simulation(strategy="random", render=None)
    while True:
        print(s.run())
        x = input('-')
        if x != "":
            exec(x)
        s.reset()

from pettingzoo.mpe import simple_tag_v3
import modules.actors.adversaries as adv
import modules.actors.agents as ag

CYCLES = 25

class Simulation:
    def __init__(self, adv_strategy='default', ag_strategy='default', render=None):
        self.adv_strategy = adv_strategy
        self.ag_strategy = ag_strategy
        self.render = render
        self.env = simple_tag_v3.parallel_env(num_good=1, num_adversaries=3, num_obstacles=2, max_cycles=CYCLES, continuous_actions=False, render_mode=render)
        self.observations, self.infos = self.env.reset()
        self.num_catches = 0
        self.n_steps = 0

        if adv_strategy == 'default':
            self.actors = {agent: adv.BaseAdversary(agent, self.observations[agent]) for agent in self.env.agents[:-1]}
        elif adv_strategy == 'random':
            self.actors = {agent: adv.RandomAdversary(agent, self.observations[agent]) for agent in self.env.agents[:-1]}
        elif adv_strategy == 'greedy':
            self.actors = {agent: adv.GreedyAdversary(agent, self.observations[agent]) for agent in self.env.agents[:-1]}
        elif adv_strategy == 'surround':
            self.actors = {agent: adv.SurroundAdversary(agent, self.observations[agent]) for agent in self.env.agents[:-1]}
        elif adv_strategy == 'intercept':
            self.actors = {agent: adv.InterceptAdversary(agent, self.observations[agent], 1.5) for agent in self.env.agents[:-1]}
        elif adv_strategy == 'distract_pursue':
            self.actors = {agent: adv.DistractPursueAdversary(agent, self.observations[agent]) for agent in self.env.agents[:-1]}
        elif adv_strategy == 'q_learning':
            self.actors = {agent: adv.DQNAdversary(agent, self.observations[agent], './dqn_weights') for agent in self.env.agents[:-1]}
        else:
            raise NotImplementedError

        if ag_strategy == 'default':
            self.actors.update({'agent_0': ag.BaseAgent('agent_0', self.observations['agent_0'])})
        elif ag_strategy == 'random':
            self.actors.update({'agent_0': ag.RandomAgent('agent_0', self.observations['agent_0'])})
        elif ag_strategy == 'greedy':
            self.actors.update({'agent_0': ag.ClosestAgent('agent_0', self.observations['agent_0'])})
        elif ag_strategy == 'bounded':
            self.actors.update({'agent_0': ag.BoundedAgent('agent_0', self.observations['agent_0'])})
        else:
            raise NotImplementedError

    def reset(self):
        self.__init__(self.adv_strategy, self.ag_strategy, self.render)

    def total_reward_prey(self):
        return sum(self.actors['agent_0'].reward_history)

    def total_reward_predators(self):
        return sum(self.actors['adversary_0'].reward_history)
    
    def update_num_catches(self, rewards):
        if rewards['adversary_0'] == 10:
            self.num_catches += 1

    def _step(self):
        actions = {actor: self.actors[actor].get_action() for actor in self.env.agents}
        observations, rewards, terminations, truncations, infos = self.env.step(actions)
        self.update_num_catches(rewards)
        for actor in self.actors.keys():
            self.actors[actor].update(observations[actor], actions[actor], rewards[actor])
        self.n_steps += 1

    def run(self):
        while self.env.agents:
            self._step()
        self.env.close()

        # Save weights for Q-learning adversaries
        self.save_weights()

        if 10.0 in self['adversary_0'].reward_history:
            first_catch = self['adversary_0'].reward_history.index(10.0)
        else:
            first_catch = -1
        return (first_catch, self.total_reward_predators(), self.num_catches)

    def save_weights(self):
        for actor in self.actors.values():
            if isinstance(actor, adv.DQNAdversary):
                actor.save_weights(actor.weights_filepath)

    def __getitem__(self, name):
        return self.actors[name]

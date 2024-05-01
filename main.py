from pettingzoo.mpe import simple_tag_v3
import json
env = simple_tag_v3.parallel_env(num_good=1, num_adversaries=1, num_obstacles=0, max_cycles=1, continuous_actions=False, render_mode=None)
observations, infos = env.reset()

while env.agents:
    # this is where you would insert your policy
    actions = {agent: env.action_space(agent).sample() for agent in env.agents}
    # It seems that the good agents have position and velocity information, while the adversaries do not
    observations, rewards, terminations, truncations, infos = env.step(actions)
    print(len(observations['adversary_0']))
    print((observations['adversary_0']))
env.close()
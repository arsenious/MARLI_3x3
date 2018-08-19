from environment import environment
from agent import agent
import numpy as np
from collections import defaultdict
import traci





# Q table implementation (env.observation_space.n, env.action_space.n)
agent_list = ["ag11", "ag21", "ag31"]
env = environment(agent_list)

ags = [agent(a_id) for a_id in agent_list ]


states_now = dict()
actions = dict()
rewards = dict()
states_next = dict()

ep_reward = 0


for episode in range(1, 31):
    done = False
    ep_reward, ep_counter = 0, 0

    # To render
    if episode < 21:
        sumoBinary = "sumo"
        states_now = env.reset(sumoBinary)
    else:
        sumoBinary = "sumo-gui"
        states_now = env.reset(sumoBinary)


    while done == False:

        # Agents taking actions with states now
        for i, a_id in enumerate(agent_list):
            if ags[i].agent_id == a_id:
                actions[a_id] = ags[i].choose_action(states_now[a_id])
        # Actions by all

        states_next, rewards, _, _ = env.step(actions) # Combined interface

        # Agents update Q tables
        for i, a_id in enumerate(agent_list):
            if ags[i].agent_id == a_id:
                ags[i].update_Q_table(states_now[a_id], actions[a_id], rewards[a_id], states_next[a_id])
        # Updated by all

        ep_reward += sum(rewards.values())
        ep_counter += 1
        states_now = states_next


        if ep_counter % 50 == 0:
            print('Episode {} counter: {} Total Reward: {} '.format(episode, ep_counter, ep_reward ))

        if ep_counter == 500:
            done = True
            env.close()



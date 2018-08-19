import numpy as np
from collections import defaultdict
import traci
import random

class agent():

    def __init__(self, agent_id):

        self.agent_id = agent_id

        self.GAMMA = 0.80
        self.epsilon = 1.00
        self.DECAY_RATE = 0.95

        self.Q = defaultdict(dict)
        ###
        self.Q["NSlow_EWlow"]["NSgreen"] = 0
        self.Q["NSlow_EWhigh"]["NSgreen"] = 0
        self.Q["NShigh_EWlow"]["NSgreen"] = 0
        self.Q["NShigh_EWhigh"]["NSgreen"] = 0

        self.Q["NSlow_EWlow"]["EWgreen"] = 0
        self.Q["NSlow_EWhigh"]["EWgreen"] = 0
        self.Q["NShigh_EWlow"]["EWgreen"] = 0
        self.Q["NShigh_EWhigh"]["EWgreen"] = 0
        ###

    def choose_action(self, state):

        ###
        def exploit(state):
            # Choose action with highest Q-value
            if self.Q[state]["NSgreen"] > self.Q[state]["EWgreen"]:
                action = "NSgreen"
            else:
                action = "EWgreen"

            return action
        ###

        def explore(state):
            # state not needed for e-greedy
            action = random.choice(["NSgreen", "EWgreen"])
            self.epsilon = self.epsilon * self.DECAY_RATE
            if self.epsilon < 0.10:
                self.epsilon = 0
            return action
        ###

        if random.random() > self.epsilon:
            return exploit(state)
        else:
            return explore(state)



    def update_Q_table(self, state_now, action, reward, state_next):

        self.Q[state_now][action] = (reward + (self.GAMMA * max(self.Q[state_next]["NSgreen"], self.Q[state_next]["EWgreen"])))

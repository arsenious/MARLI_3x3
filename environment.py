import numpy
import traci
import os, sys


class environment():

    def __init__(self, agent_list):

        self.agent_list = agent_list

        self.timestep = 0

        # Observations for all
        self.observations = dict()
        for ag in self.agent_list:
            self.observations[ag] = "NSlow_EWlow"
        ###

        # Rewards for all
        self.rewards = dict()
        for ag in self.agent_list:
            self.rewards[ag] = 0
        ###


        self.done = False
        self.info = ""

        self.sumoBinary = "sumo"

    def step(self, actions):

        print("Taking actions " + str(actions) + " at timestep " + str(self.timestep))

        ### ACTION

        for ag in self.agent_list:

            if actions[ag] == "NSgreen":
                traci.trafficlight.setRedYellowGreenState(ag, 'GGgrrrGGgrrr')
            elif actions[ag] == "EWgreen":
                traci.trafficlight.setRedYellowGreenState(ag, 'rrrGGgrrrGGg')
            else:
                print("Unknown action")

        # Perform action for 10 seconds
        for i in range(10):
            traci.simulationStep()
            self.timestep += 1


        ### STATE
        print("Getting Environment States for agents")

        for ag in self.agent_list:

            # NS Halted
            halt_N_i = traci.lane.getLastStepHaltingNumber(ag + "_N_i_0")
            halt_S_i = traci.lane.getLastStepHaltingNumber(ag + "_S_i_0")

            # EW Halted
            halt_E_i = traci.lane.getLastStepHaltingNumber(ag + "_E_i_0")
            halt_W_i = traci.lane.getLastStepHaltingNumber(ag + "_W_i_0")

            env_state = ""

            # NS State
            if (halt_N_i + halt_S_i) / 2.0 > 1:
                env_state = env_state + "NShigh"
            else:
                env_state = env_state + "NSlow"

            env_state = env_state + "_"
            # EW State
            if (halt_E_i + halt_W_i) / 2.0 > 1:
                env_state = env_state + "EWhigh"
            else:
                env_state = env_state + "EWlow"

            self.observations[ag] = env_state

        print("Observations are " + str(self.observations) + " at timestep " + str(self.timestep))

        #### REWARD
        print("Calculating Rewards...")

        for ag in self.agent_list:
            # NS Wait
            wait_N_i = traci.lane.getWaitingTime(ag + "_N_i_0")
            speed_N_i = traci.lane.getLastStepMeanSpeed(ag + "_N_i_0")
            wait_S_i = traci.lane.getWaitingTime(ag + "_S_i_0")
            speed_S_i  = traci.lane.getLastStepMeanSpeed(ag +"_S_i_0")


            # EW Wait
            wait_E_i = traci.lane.getWaitingTime(ag + "_E_i_0")
            speed_E_i = traci.lane.getLastStepMeanSpeed(ag + "_E_i_0")
            wait_W_i = traci.lane.getWaitingTime(ag + "_W_i_0")
            speed_W_i = traci.lane.getLastStepMeanSpeed(ag + "_W_i_0")


            env_reward = -1 * ((wait_N_i + wait_S_i + wait_E_i + wait_W_i)**2 / 10.0)
            #env_reward += (speed_N_i + speed_S_i + speed_E_i + speed_W_i) / 10.0

            self.rewards[ag] = env_reward

        print("Rewards are " + str(self.rewards) + " at timestep " + str(self.timestep))


        return self.observations, self.rewards, self.done, self.info


    def reset(self, sumoBinary):
        USE_GUI = True

        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
            print(tools)
        else:
            sys.exit("Please declare environment variable 'SUMO_HOME'")

        self.sumoBinary = sumoBinary
        sumoCmd = [self.sumoBinary, "-c", "3x3cross/3x3cross.sumocfg"]
        traci.start(sumoCmd)

        self.timestep = 0

        # Observations for all
        self.observations = dict()
        for ag in self.agent_list:
            self.observations[ag] = "NSlow_EWlow"
        ###

        # Rewards for all
        self.rewards = dict()
        for ag in self.agent_list:
            self.rewards[ag] = 0
        ###

        self.done = False
        self.info = ""

        return self.observations

    def close(self):
        traci.close()
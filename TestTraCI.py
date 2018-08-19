import os, sys
import traci

USE_GUI = True

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
    print(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

sumoBinary = "sumo-gui"
sumoCmd = [sumoBinary, "-c", "cross/cross.sumocfg"]


traci.start(sumoCmd)
step = 0


def flip_phase():

    #Phases noticed
    # 1 : NS Green
    # 4 : EW Green
    # Other numbers 0,2,3,5,6,7 are intermediate phases

    cur_state = traci.trafficlight.getRedYellowGreenState("0")

    if cur_state == 'GGgrrrGGgrrr':
        traci.trafficlight.setRedYellowGreenState("0", 'rrrGGgrrrGGg')
        return

    if cur_state == 'rrrGGgrrrGGg':
        traci.trafficlight.setRedYellowGreenState("0", 'GGgrrrGGgrrr')
        return

    print("Improper phase")
    return


def infer_state_from_occupancies():
    # NS Occupancy
    halt_Ag1_N_i = traci.lane.getLastStepHaltingNumber("Ag1_N_i_0")
    halt_Ag1_S_i = traci.lane.getLastStepHaltingNumber("Ag1_S_i_0")

    # EW Occupancy
    halt_Ag1_E_i = traci.lane.getLastStepHaltingNumber("Ag1_E_i_0")
    halt_Ag1_W_i = traci.lane.getLastStepHaltingNumber("Ag1_W_i_0")

    print("Getting lane occupancies")

    agent_state = ""

    if (halt_Ag1_N_i + halt_Ag1_S_i) / 2.0 > 1 :
        agent_state = agent_state + "NShigh"

    else:
        agent_state = agent_state + "NSlow"

    agent_state = agent_state + "_"

    if (halt_Ag1_E_i + halt_Ag1_W_i) / 2.0 > 1:
        agent_state = agent_state + "EWhigh"

    else:
        agent_state = agent_state + "EWlow"

    return agent_state


def infer_reward_from_waittimes():

    # NS Wait
    wait_Ag1_N_i = traci.lane.getWaitingTime("Ag1_N_i_0")
    wait_Ag1_S_i = traci.lane.getWaitingTime("Ag1_S_i_0")

    # EW Wait
    wait_Ag1_E_i = traci.lane.getWaitingTime("Ag1_E_i_0")
    wait_Ag1_W_i = traci.lane.getWaitingTime("Ag1_W_i_0")

    agent_reward = -1 * (wait_Ag1_N_i + wait_Ag1_S_i + wait_Ag1_E_i + wait_Ag1_W_i) / 10.0

    return agent_reward







"""
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    if traci.trafficlight.getPhase("0") == 2:
        # we are not already switching
        if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
            # there is a vehicle from the north, switch
            traci.trafficlight.setPhase("0", 3)
        else:
            # otherwise try to keep green for EW
            traci.trafficlight.setPhase("0", 2)
    step += 1
"""

traci.trafficlight.setRedYellowGreenState("0", 'GGgrrrGGgrrr')

while traci.simulation.getMinExpectedNumber() > 0:

    if step % 50 == 0:
        flip_phase()

    if step % 10 == 0:


        cur_agent_state = infer_state_from_occupancies()

        cur_agent_reward = infer_reward_from_waittimes()

        print("Agent state is " + cur_agent_state)
        print("Agent reward is " + str(cur_agent_reward))


    traci.simulationStep()
    step += 1


traci.close()
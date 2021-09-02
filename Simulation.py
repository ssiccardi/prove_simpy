import simpy
from agents import *
from AgentHandler import *


if __name__ == "__main__":
    agentHandler = AgentHandler()
    agentHandler.create_environment()
    #print(agentHandler)

    # parametri
    min_tel = 3  # minima durata telefonata voce
    max_tel = 900  # massima durata telefonata voce

    # preparare intervalli analoghi per le altre classi
    sms_prob_risposta = 7  # 7 volte su 10

    env = simpy.Environment()
    agentHandler.start_simulation(env, 9000)


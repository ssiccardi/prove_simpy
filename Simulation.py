from AgentHandler import *
import simpy

if __name__ == "__main__":
    agentHandler = AgentHandler()
    agentHandler.create_environment()
    #print(agentHandler)

    # parametri


    # preparare intervalli analoghi per le altre classi
    sms_prob_risposta = 7  # 7 volte su 10

    env = simpy.Environment()
    agentHandler.start_simulation(env, 9000)


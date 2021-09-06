import random
import simpy

class Persona:

    def __init__(self, id, agentHandler):
        self.id = id
        self.importatori = []
        self.spacciatori = []
        self.magazzinieri = []
        self.consumatoreControllato = []
        self.cella = random.randint(0, 7)
        self.agentHandler = agentHandler

    def __str__(self) -> str:
        return f"Sono una Persona Generica con ID={self.id}\n" \
               f"   Importatori: {[agent.get_id() for agent in self.importatori]}\n" \
               f"   Spacciatori: {[agent.get_id() for agent in self.spacciatori]}\n" \
               f"   Magazzinieri: {[agent.get_id() for agent in self.magazzinieri]}\n" \
               f"   Consumatori Controllati: {[agent.get_id() for agent in self.consumatoreControllato]}\n" \
               f"   E mi trovo nella cella {self.cella}\n"

    def enter_simulation_environment(self,importatori, spacciatori, magazzinieri, consumatoreControllato):
        self.importatori = importatori
        self.spacciatori = spacciatori
        self.magazzinieri = magazzinieri
        self.consumatoreControllato = consumatoreControllato

        self.min_interval_tel = 120  # minimo intervallo fra telefonate
        self.max_interval_tel = 1800  # massimo intervallo fra telefonate

        self.min_spostamento = 1800  # minimo intervallo fra spostamenti
        self.max_spostamento = 3600  # massimo intervallo fra spostamenti

    def get_id(self):
        return self.id

    def start_simulation(self, env):
        self.env = env
        self.action = env.process(self.run())

    def call_someone(self, is_chiamata, duration, receiver):
        self.agentHandler.handle_call(self, receiver, is_chiamata, duration, self.env.now)

    def run(self):
        while True:

            call_params = self.agentHandler.get_call_param(
                [self.importatori, self.spacciatori, self.magazzinieri, self.consumatoreControllato])

            self.call_someone(call_params[0], call_params[1], call_params[2])
            try:
                yield self.env.timeout(random.randint(self.min_interval_tel, self.max_interval_tel) + call_params[1])
            except simpy.Interrupt as interrupt:
                print(CRED + "Sono stato interrotto da qualcosa che non doveva interrompermi!" + CEND)

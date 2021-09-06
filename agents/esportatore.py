import random
import simpy

CRED = '\033[91m'
CEND = '\033[0m'
from agents import States

class Esportatore:

    def __init__(self, id, agentHandler):
        self.id = id
        self.camionisti = []
        self.importatori = []
        self.cella = random.randint(0, 7)
        self.agentHandler = agentHandler

    def __str__(self) -> str:
        return f"Sono un Esportatore con ID={self.id}\n" \
               f"   Camionisti: {[agent.get_id() for agent in self.camionisti]}\n" \
               f"   Importatori: {[agent.get_id() for agent in self.importatori]}\n" \
               f"   E mi trovo nella cella {self.cella}\n"

    def enter_simulation_environment(self, camionisti, importatori):
        self.camionisti = camionisti
        self.importatori = importatori
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
            state = self.agentHandler.get_state()
            if state != States.TRATTATIVA:
                call_params = self.agentHandler.get_call_param(
                    [self.importatori])

                self.call_someone(call_params[0], call_params[1], call_params[2])
                yield self.env.timeout(call_params[1])
            try:
                yield self.env.timeout(random.randint(self.min_interval_tel, self.max_interval_tel))
            except simpy.Interrupt as interrupt:
                cause = ''.join(x for x in str(interrupt.cause) if not x.isdigit())
                id = ''.join(x for x in str(interrupt.cause) if x.isdigit())

                causes1 = ["chiamata-importatore", "sms-importatore"]
                if cause in causes1:
                    call_params = self.agentHandler.get_call_param(
                        [self.camionisti])
                    self.call_someone(call_params[0], call_params[1], call_params[2])
                    yield self.env.timeout(call_params[1])
                else:
                    print(CRED + "Sono stato interrotto da qualcosa che non doveva interrompermi!" + CEND)

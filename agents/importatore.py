import random

import simpy
from agents import States

from agents import Consumatore


CRED = '\033[91m'
CEND = '\033[0m'


class Importatore:

    def __init__(self, id, agentHandler):
        self.id = id
        self.importatori = []
        self.esportatori = []
        self.spacciatori = []
        self.magazzinieri = []
        self.persone = []
        self.cella = random.randint(0, 7)
        self.agentHandler = agentHandler

    def __str__(self) -> str:
        return f"Sono un Importatore con ID={self.id}\n" \
               f"   Importatori: {[agent.get_id() for agent in self.importatori]}\n" \
               f"   Esportatori: {[agent.get_id() for agent in self.esportatori]}\n" \
               f"   Magazzinieri: {[agent.get_id() for agent in self.magazzinieri]}\n" \
               f"   Spacciatori: {[agent.get_id() for agent in self.spacciatori]}\n" \
               f"   Persone generiche: {[agent.get_id() for agent in self.persone]}\n" \
               f"   E mi trovo nella cella {self.cella}\n"

    def enter_simulation_environment(self, importatori, esportatori, spacciatori, magazzinieri, persone):
        self.esportatori = esportatori
        self.importatori = importatori
        self.spacciatori = spacciatori
        self.magazzinieri = magazzinieri
        self.persone = persone
        self.min_interval_tel = 120  # minimo intervallo fra telefonate per importatori
        self.max_interval_tel = 1800  # massimo intervallo fra telefonate per importatori

        self.min_spostamento = 1800  # minimo intervallo fra spostamenti per importatori
        self.max_spostamento = 3600  # massimo intervallo fra spostamenti per importatori

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Importatore):
            return o.get_id() == self.id
        return False

    def doIKnowPersonX(self, id):
        result = list(filter(lambda x: x.get_id() == id, self.persone))
        return self.id if len(result) != 0 else -1

    def get_id(self):
        return self.id

    def start_simulation(self, env):
        self.env = env
        self.action = env.process(self.run())

    def run(self):
        while True:
            state = self.agentHandler.get_state()
            interval = random.randint(self.min_interval_tel, self.max_interval_tel)
            if state == States.TRATTATIVA:
                call_params = self.agentHandler.get_call_param([self.esportatori])
                self.call_someone(call_params[0], call_params[1], call_params[2])
            else:
                call_params = self.agentHandler.get_call_param(
                    [self.esportatori, self.importatori, self.magazzinieri, self.persone, self.spacciatori])

                self.call_someone(call_params[0], call_params[1], call_params[2])

            try:
                yield self.env.timeout(interval + call_params[1])
            except simpy.Interrupt as interrupt:
                cause = ''.join(x for x in str(interrupt.cause) if not x.isdigit())
                id = ''.join(x for x in str(interrupt.cause) if x.isdigit())
                print(cause)
                causes1 = ["chiamata-spacciatore", "sms-spacciatore", "chiamata-magazziniere", "sms-magazziniere",
                           "chiamata-importatore", "sms-importatore"]
                causes2 = ["chiamata-camionista", "sms-camionista"]

                if cause in causes1:
                    # Quando riceve una chiamata o sms da uno spacciatore, da un magazziniere o da un altro importatore,
                    # chiama o manda sms a un esportatore con probabilità Y
                    will_call = bool(random.randint(0, 6))
                    if will_call:
                        call_params = self.agentHandler.get_call_param([self.esportatori])
                        self.call_someone(call_params[0], call_params[1], call_params[2])

                elif cause in causes2:
                    # Quando riceve una telefonata o un sms da un camionista gli risponde (o lo richiama dopo un tempo casuale fra
                    # T1 e T2) e poi chiama o manda sms a un importatore e a uno spacciatore
                    waiting = random.randint(self.min_interval_tel, self.max_interval_tel)
                    camionista = self.agentHandler.get_agent_by_id(id)
                    yield self.env.timeout(waiting)

                    call_params = self.agentHandler.get_call_param([])
                    self.call_someone(call_params[0], call_params[1], camionista)

                    call_params = self.agentHandler.get_call_param([self.importatori])
                    self.call_someone(call_params[0], call_params[1], call_params[2])

                    call_params = self.agentHandler.get_call_param([self.importatori])
                    self.call_someone(call_params[0], call_params[1], call_params[2])

                else:
                    print(CRED + "Sono stato interrotto da qualcosa che non doveva interrompermi!" + CEND)

    def call_someone(self, is_chiamata, duration, receiver):
        self.agentHandler.handle_call(self, receiver, is_chiamata, duration, self.env.now)
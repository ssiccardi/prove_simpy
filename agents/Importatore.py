import random
from agents.Camionista import *
from agents.Consumatore import *
from agents.Esportatore import *
from agents.Magazziniere import *
from agents.Persona import *
from agents.Importatore import *
from agents.Spacciatore import *

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
        t11_import = 120  # minimo intervallo fra telefonate per importatori
        t12_import = 1800  # massimo intervallo fra telefonate per importatori
        t21_import = 1800  # minimo intervallo fra spostamenti per importatori
        t22_import = 3600  # massimo intervallo fra spostamenti per importatori
        while True:
            is_chiamata = bool(random.randint(0,1))
            interval = random.randint(t11_import, t12_import)
            type_receiver = random.randint(0,3)
            receiver = None
            if type_receiver == 0:
                receiver = random.choice(self.importatori)
            elif type_receiver == 1:
                receiver = random.choice(self.esportatori)
            elif type_receiver ==2:
                receiver = random.choice(self.spacciatori)
            else:
                receiver = random.choice(self.magazzinieri)
            yield self.env.process(self.call_someone(is_chiamata, interval, receiver))

            yield self.env.timeout(500)

    def call_someone(self, is_chiamata, interval, receiver):

        self.agentHandler.register_event(self.get_id(), "S", receiver.get_id(), "S", self.env.now, "V" if is_chiamata else "S" , 666) #TODO fixaretamestamp
        yield self.env.timeout(interval)
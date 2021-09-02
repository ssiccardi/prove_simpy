import random
from agents.Camionista import *
from agents.Consumatore import *
from agents.Esportatore import *
from agents.Magazziniere import *
from agents.Persona import *
from agents.Importatore import *
from agents.Spacciatore import *
class Consumatore:

    def __init__(self, id):
        self.id = id
        self.spacciatore = None
        self.persone = []
        self.controllato = bool(random.randint(0,1))
        self.cella = random.randint(0, 7)


    def __str__(self) -> str:
        return f"Sono un Consumatore con ID={self.id}\n" \
               f"   Spacciatore: {self.spacciatore.get_id()}\n" \
               f"   Persone generiche: {[agent.get_id() for agent in self.persone]}\n" \
               f"   Sono controllato: {self.controllato}\n" \
               f"   E mi trovo nella cella {self.cella}\n"

    def enter_simulation_environment(self, spacciatore, persone):
        self.spacciatore = spacciatore
        self.persone = persone

    def doIKnowPersonX(self, id):
        result = list(filter(lambda x: x.get_id() == id, self.persone))
        return self.id if len(result)!=0 else -1

    def get_id(self):
        return self.id

    def is_controllato(self):
        return self.controllato
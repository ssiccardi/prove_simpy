from agents.Camionista import *
from agents.Consumatore import *
from agents.Esportatore import *
from agents.Magazziniere import *
from agents.Persona import *
from agents.Importatore import *
from agents.Spacciatore import *
import random
class Spacciatore:

    def __init__(self, id):
        self.id = id
        self.magazziniere=None
        self.consumatori=[]
        self.persone=[]
        self.qtadroga=random.randint(0, 3)
        self.cella=random.randint(0, 7)



    def __str__(self) -> str:
        return f"Sono uno Spacciatore con ID={self.id}\n" \
               f"   Magazziniere: {self.magazziniere.get_id()}\n" \
               f"   Consumatori: {[agent.get_id() for agent in self.consumatori]}\n" \
               f"   Persone: {[agent.get_id() for agent in self.persone]}\n" \
               f"   Ho {self.qtadroga} di droga\n" \
               f"   E mi trovo nella cella {self.cella}\n"

    def enter_simulation_environment(self, magazziniere, consumatori, persone):
        self.magazziniere = magazziniere
        self.consumatori = consumatori
        self.persone = persone

    def doIKnowPersonX(self, id):
        result = list(filter(lambda x: x.get_id() == id, self.persone))
        return self.id if len(result)!=0 else -1

    def get_id(self):
        return self.id

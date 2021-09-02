from agents.Camionista import *
from agents.Consumatore import *
from agents.Esportatore import *
from agents.Magazziniere import *
from agents.Persona import *
from agents.Importatore import *
from agents.Spacciatore import *
import random

class Esportatore:

    def __init__(self, id):
        self.id = id
        self.camionisti = []
        self.importatori = []
        self.cella = random.randint(0, 7)

    def __str__(self) -> str:
        return f"Sono un Esportatore con ID={self.id}\n" \
               f"   Camionisti: {[agent.get_id() for agent in self.camionisti]}\n" \
               f"   Importatori: {[agent.get_id() for agent in self.importatori]}\n" \
               f"   E mi trovo nella cella {self.cella}\n"


    def enter_simulation_environment(self, camionisti, importatori):
        self.camionisti=camionisti
        self.importatori=importatori

    def get_id(self):
        return self.id
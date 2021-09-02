from agents.Camionista import *
from agents.Consumatore import *
from agents.Esportatore import *
from agents.Magazziniere import *
from agents.Persona import *
from agents.Importatore import *
from agents.Spacciatore import *
import random


class Camionista:

    def __init__(self, id):
        self.id = id
        self.importatori = []
        self.esportatori = []
        self.magazzinieri = []
        self.cella = random.randint(0, 7)

    def __str__(self) -> str:
        return f"Sono un Camionista con ID={self.id}\n" \
               f"   Importatori: {[agent.get_id() for agent in self.importatori]}\n" \
               f"   Esportatori: {[agent.get_id() for agent in self.esportatori]}\n" \
               f"   Magazzinieri: {[agent.get_id() for agent in self.magazzinieri]}\n" \
               f"   E mi trovo nella cella {self.cella}\n"

    def enter_simulation_environment(self, importatori, esportatori, magazzinieri):
        self.importatori = importatori
        self.esportatori = esportatori
        self.magazzinieri = magazzinieri

    def get_id(self):
        return self.id
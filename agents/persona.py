import random

class Persona:

    def __init__(self, id):
        self.id = id
        self.importatori = []
        self.spacciatori = []
        self.magazzinieri = []
        self.consumatoreControllato = []
        self.cella = random.randint(0, 7)

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

    def get_id(self):
        return self.id

import random

class Magazziniere:

    def __init__(self, id):
        self.id = id
        self.importatori = []
        self.spacciatori = []
        self.persone = []
        self.qtadroga = random.randint(0, 3)
        self.celladroga = random.randint(0, 7)
        self.cella = random.randint(0, 7)

    def __str__(self) -> str:
        return f"Sono un Magazziniere con ID={self.id}\n" \
               f"   Importatori: {[agent.get_id() for agent in self.importatori]}\n" \
               f"   Spacciatori: {[agent.get_id() for agent in self.spacciatori]}\n" \
               f"   Persone Generiche: {[agent.get_id() for agent in self.persone]}\n" \
               f"   Ho {self.qtadroga} droga tenuta nella cella {self.celladroga}\n" \
               f"   E mi trovo nella cella {self.cella}\n"

    def enter_simulation_environment(self, importatori, spacciatori, persone):
        self.importatori = importatori
        self.spacciatori = spacciatori
        self.persone = persone

    def doIKnowPersonX(self, id):
        result = list(filter(lambda x: x.get_id() == id, self.persone))
        return self.id if len(result)!=0 else -1

    def get_id(self):
        return self.id
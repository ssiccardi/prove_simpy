import itertools
import random
from agents.Camionista import *
from agents.Consumatore import *
from agents.Esportatore import *
from agents.Magazziniere import *
from agents.Persona import *
from agents.Importatore import *
from agents.Spacciatore import *


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class AgentHandler:
    progressive_id = itertools.count()
    events=[]

    def __init__(self):
        self.camionisti = []
        self.consumatori = []
        self.esportatori = []
        self.magazzinieri = []
        self.spacciatori = []
        self.importatori = []
        self.persone = []

    def create_environment(self, n_camionisti=2, n_importatori=3, n_magazzinieri=2, n_esportatori=1, n_spacciatori=2,
                           n_consumatori=4, n_persone=2):

        self.camionisti = [Camionista(next(self.progressive_id)) for i in range(n_camionisti)]
        self.consumatori = [Consumatore(next(self.progressive_id)) for i in range(n_consumatori)]
        self.importatori = [Importatore(next(self.progressive_id), self) for i in range(n_importatori)]
        self.magazzinieri = [Magazziniere(next(self.progressive_id)) for i in range(n_magazzinieri)]
        self.esportatori = [Esportatore(next(self.progressive_id)) for i in range(n_esportatori)]
        self.spacciatori = [Spacciatore(next(self.progressive_id)) for i in range(n_spacciatori)]
        self.persone = [Persona(next(self.progressive_id)) for i in range(n_persone)]


        self.bind()

    def bind(self):
        for camionista in self.camionisti:
            camionista.enter_simulation_environment(random.sample(self.importatori, k=2),
                                                    random.sample(self.esportatori, k=1),
                                                    self.magazzinieri)

        for consumatore in self.consumatori:
            consumatore.enter_simulation_environment(random.choice(self.spacciatori), random.sample(self.persone, k=2))

        for esportatore in self.esportatori:
            esportatore.enter_simulation_environment(self.camionisti, self.importatori)

        for importatore in self.importatori:
            importatore.enter_simulation_environment(self.importatori, self.esportatori, self.spacciatori,
                                                     self.magazzinieri, random.sample(self.persone, k=2))

        for magazziniere in self.magazzinieri:
            magazziniere.enter_simulation_environment(self.importatori, random.sample(self.spacciatori, k=1),
                                                      random.sample(self.persone, k=2))

        for spacciatore in self.spacciatori:
            spacciatore.enter_simulation_environment(random.choice(self.magazzinieri),
                                                     random.sample(self.consumatori, k=2),
                                                     random.sample(self.persone, k=2))

        for persona in self.persone:
            id = persona.get_id()
            magazzinieri_per = list(filter(lambda x: x != -1,
                                           [agent.doIKnowPersonX(id) for agent in
                                            self.magazzinieri]))
            spacciatori_per = list(filter(lambda x: x != -1,
                                          [agent.doIKnowPersonX(id) for agent in
                                           self.spacciatori]))
            consumatori_per = list(filter(lambda x: x != -1,
                                          [agent.doIKnowPersonX(id) for agent in
                                           self.consumatori]))
            importatori_per = list(filter(lambda x: x != -1,
                                          [agent.doIKnowPersonX(id) for agent in
                                           self.importatori]))

            magazzinieri = list(filter(lambda agent: agent.get_id() in magazzinieri_per, self.magazzinieri))
            spacciatori = list(filter(lambda agent: agent.get_id() in spacciatori_per, self.spacciatori))
            consumatori = list(
                filter(lambda agent: (agent.get_id() in consumatori_per and agent.is_controllato()), self.consumatori))

            importatori = list(filter(lambda agent: agent.get_id() in importatori_per, self.importatori))
            persona.enter_simulation_environment(importatori, spacciatori, magazzinieri, consumatori)

    def __str__(self) -> str:
        return f"{''.join(str(agent) for agent in self.camionisti)}" \
               f"\n{''.join(str(agent) for agent in self.consumatori)}"\
               f"\n{''.join(str(agent) for agent in self.esportatori)}"\
               f"\n{''.join(str(agent) for agent in self.importatori)}"\
               f"\n{''.join(str(agent) for agent in self.magazzinieri)}"\
               f"\n{''.join(str(agent) for agent in self.persone)}"\
               f"\n{''.join(str(agent) for agent in self.spacciatori)}"

    def start_simulation(self, env, duration):
        for importatore in self.importatori:
            importatore.start_simulation(env)

        env.run(until=duration)


    def register_event(self, sender, sender_interc, receiver ,receiver_interc, timestamp, type, duration):
        print(timestamp, sender, sender_interc, receiver, receiver_interc, type, duration)
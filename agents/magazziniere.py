import random
import simpy
CRED = '\033[91m'
CEND = '\033[0m'
class Magazziniere:

    def __init__(self, id, agentHandler):
        self.id = id
        self.importatori = []
        self.spacciatori = []
        self.persone = []
        self.qtadroga = random.randint(0, 3)
        self.celladroga = random.randint(0, 7)
        self.cella = random.randint(0, 7)
        self.agentHandler = agentHandler

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
        self.min_interval_tel = 120  # minimo intervallo fra telefonate
        self.max_interval_tel = 1800  # massimo intervallo fra telefonate

        self.min_spostamento = 1800  # minimo intervallo fra spostamenti
        self.max_spostamento = 3600  # massimo intervallo fra spostamenti

    def start_simulation(self, env):
        self.env = env
        self.action = env.process(self.run())

    def doIKnowPersonX(self, id):
        result = list(filter(lambda x: x.get_id() == id, self.persone))
        return self.id if len(result)!=0 else -1

    def get_id(self):
        return self.id

    def call_someone(self, is_chiamata, duration, receiver):
        self.agentHandler.handle_call(self, receiver, is_chiamata, duration, self.env.now)


    def run(self):
        while True:
            state = self.agentHandler.get_state()

            call_params = self.agentHandler.get_call_param(
                [self.spacciatori, self.importatori, self.persone])

            self.call_someone(call_params[0], call_params[1], call_params[2])
            try:
                yield self.env.timeout(random.randint(self.min_interval_tel, self.max_interval_tel) + call_params[1])
            except simpy.Interrupt as interrupt:
                cause = ''.join(x for x in str(interrupt.cause) if not x.isdigit())
                id = ''.join(x for x in str(interrupt.cause) if x.isdigit())

                causes1 = ["chiamata-camionista", "sms-camionista"]
                if cause in causes1:
                    pass
                else:
                    print(CRED + "Sono stato interrotto da qualcosa che non doveva interrompermi!" + CEND)
import random
CRED = '\033[91m'
CEND = '\033[0m'
import simpy

class Spacciatore:

    def __init__(self, id, agentHandler):
        self.id = id
        self.magazziniere = None
        self.consumatori = []
        self.persone = []
        self.qtadroga = random.randint(0, 3)
        self.cella = random.randint(0, 7)
        self.agentHandler=agentHandler

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
        self.min_interval_tel = 120  # minimo intervallo fra telefonate
        self.max_interval_tel = 1800  # massimo intervallo fra telefonate

        self.min_spostamento = 1800  # minimo intervallo fra spostamenti
        self.max_spostamento = 3600  # massimo intervallo fra spostamenti

    def doIKnowPersonX(self, id):
        result = list(filter(lambda x: x.get_id() == id, self.persone))
        return self.id if len(result) != 0 else -1

    def get_id(self):
        return self.id

    def start_simulation(self, env):
        self.env = env
        self.action = env.process(self.run())

    def call_someone(self, is_chiamata, duration, receiver):
        self.agentHandler.handle_call(self, receiver, is_chiamata, duration, self.env.now)

    def run(self):
        while True:
            state = self.agentHandler.get_state()

            call_params = self.agentHandler.get_call_param(
                [[self.magazziniere], self.consumatori, self.persone])
            self.call_someone(call_params[0], call_params[1], call_params[2])

            try:
                yield self.env.timeout(random.randint(self.min_interval_tel, self.max_interval_tel) + call_params[1])
            except simpy.Interrupt as interrupt:
                cause = ''.join(x for x in str(interrupt.cause) if not x.isdigit())
                id = ''.join(x for x in str(interrupt.cause) if x.isdigit())

                causes1 = ["chiamata-consumatore", "sms-consumatore"]
                causes2 = ["poca-droga"]
                causes3 = ["magazziniere-poca-drog"]
                if cause in causes1:
                    pass
                elif cause in causes2:
                    pass
                elif cause in causes3:
                    pass
                else:
                    print(CRED + "Sono stato interrotto da qualcosa che non doveva interrompermi!" + CEND)
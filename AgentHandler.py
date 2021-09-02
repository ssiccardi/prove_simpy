def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class AgentFactory:
    progressive_id = 0

    def __init__(self):
        self.camionisti = []
        self.consumatori = []
        self.esportatori = []
        self.magazzinieri = []
        self.spacciatori = []
        self.persone = []

    def create

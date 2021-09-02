class Esportatore:

    def __init__(self, id):
        self.id = id
        self.camionisti = []
        self.importatori = []
        self.cella = random.randint(0, 7)

    def __str__(self) -> str:
        return f"Esportatore, ID={self.id}"


    def enter_simulation_environment(self, camionisti, importatori):
        self.camionisti=camionisti
        self.importatori=importatori
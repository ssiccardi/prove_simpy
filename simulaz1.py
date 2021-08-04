import simpy
import random

# prova per vedere se i meccanismi fondamentali di simpy sono sufficienti per quello che vogliamo fare
# per ora ho implementato solo le chiamate base degli importatori e la risposta agli sms (sarebbe da migliorare)
# fa delle print, da sostituire con scrittura csv
# ha delle tabelle fisse di importatori ecc., da sostituire o con lettura di csv o con generazione di tabelle da programma

# dati degli agenti (processi simpy): come descritti nell'analisi, tranne "ultimo_mov" per gestire gli spostamenti (cambi di celle)
#  e sms_from per rispondere agli sms

importatori = [
{'id': 1, 'importatori': [1,2], 'esportatori': [0], 'spacciatori': [0,1], 'magazzinieri': [0,1], 'generici': [0], 'cella': 0, 'ultimo_mov': 0, 'sms_from': []},
{'id': 2,'importatori': [0,2], 'esportatori': [0], 'spacciatori': [0,1], 'magazzinieri': [0,1], 'generici': [0,1], 'cella': 1, 'ultimo_mov': 0, 'sms_from': []},
{'id': 3,'importatori': [0,1], 'esportatori': [0], 'spacciatori': [0,1], 'magazzinieri': [0,1], 'generici': [1], 'cella': 2, 'ultimo_mov': 0, 'sms_from': []},
]
importatori_linked = ['importatori','spacciatori','magazzinieri','generici'] # tabella ausiliaria delle entita' che un importatore puo chiamare

camionisti = [
{'id': 4,'importatori': [0,1], 'esportatori': [0], 'magazzinieri': [0,1], 'cella': 0, 'ultimo_mov': 0, 'sms_from': []},
{'id': 5,'importatori': [1,2], 'esportatori': [0], 'magazzinieri': [0,1], 'cella': 3, 'ultimo_mov': 0, 'sms_from': []},
]
magazzinieri = [
{'id': 6,'importatori': [0,1,2], 'spacciatori': [0], 'generici': [0,1], 'cella': 1, 'base':2, 'quantita': 3, 'ultimo_mov': 0, 'sms_from': []},
{'id': 7,'importatori': [0,1,2], 'spacciatori': [1], 'generici': [0,1], 'cella': 1, 'base':1, 'quantita': 1, 'ultimo_mov': 0, 'sms_from': []},
]
esportatori = [
{'id': 8,'importatori': [0,1,2], 'camionisti': [0,1], 'cella': 7, 'sms_from': []},
]
spacciatori = [
{'id': 9,'magazziniere': 0, 'consumatori': [0,1], 'generici': [0,1], 'cella': 1, 'quantita': 0.5, 'ultimo_mov': 0, 'sms_from': []},
{'id': 10,'magazziniere': 1, 'consumatori': [2], 'generici': [0,1], 'cella': 3, 'quantita': 0.7, 'ultimo_mov': 0, 'sms_from': []},
]
consumatori = [
{'id': 11,'spacciatore': 0, 'generici': [0,1], 'cella': 1, 'controllato': True, 'ultimo_mov': 0, 'sms_from': []},
{'id': 12,'spacciatore': 0, 'generici': [0,1], 'cella': 2, 'controllato': False, 'ultimo_mov': 0, 'sms_from': []},
{'id': 13,'spacciatore': 1, 'generici': [0,1], 'cella': 3, 'controllato': True, 'ultimo_mov': 0, 'sms_from': []}
]
generici = [
{'id': 14,'importatori': [0,1], 'consumatori': [0,1], 'spacciatori': [0,1], 'magazzinieri': [0,1], 'cella': 0, 'ultimo_mov': 0, 'sms_from': []},
{'id': 15,'importatori': [1,2], 'consumatori': [1], 'spacciatori': [0,1], 'magazzinieri': [0,1], 'cella': 0, 'ultimo_mov': 0, 'sms_from': []},
]

celle = [
(45.81027, 9.24048),
(45.80027, 9.22048),
(45.81349, 9.25467),
(45.81027, 9.20032),
(45.82035, 9.30490),
(45.80005, 9.29098),
(45.82356, 9.27654),
(40.64380, -2.18530),
]

stato = ""  # tutti i cambiamenti di stato del sistema devono ancora essere gestiti...

# parametri
min_tel = 3  # minima durata telefonata voce
max_tel = 900  # massima durata telefonata voce
t11_import = 120 # minimo intervallo fra telefonate per importatori
t12_import = 1800 # massimo intervallo fra telefonate per importatori
t21_import = 1800 # minimo intervallo fra spostamenti per importatori
t22_import = 3600 # massimo intervallo fra spostamenti per importatori
# preparare intervalli analoghi per le altre classi
sms_prob_risposta = 7 # 7 volte su 10
# NB: distinguere fra giorno e notte?

class importatore(object):
    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.action = env.process(self.run(name))

    def run(self, name):
        while True:
        # Ad intervalli casuali fra T11 e T12 chiama o manda sms a una delle persone di uno dei vettori elencati
        #   esclusi gli spacciatori
            while True:
                a_che_tipo = random.randint(0,len(importatori_linked)-1)
                a_chi = random.randint(0,len(importatori[self.name][importatori_linked[a_che_tipo]])-1)
                # mi assicuro che il chiamante non sia uguale a se stesso:
                if a_che_tipo != 0:
                    break
                if a_chi != self.name:
                    break
            cosa = ['S','V'][random.randint(0,1)]
            if cosa == 'S':
                durata = 0
            else:
                durata = random.randint(5,900)
            if importatori_linked[a_che_tipo] == "generici":
                ric_interc = 'N'
            else:
                ric_interc = 'S'
            esito = 0 # sempre a buon fine per adesso...
            cella_chiamata = eval(importatori_linked[a_che_tipo]+'['+str(a_chi)+']["cella"]')
            a_chi_id = eval(importatori_linked[a_che_tipo]+'['+str(a_chi)+']["id"]')
            print(self.env.now,
               durata,
               importatori[self.name]['id'],
               'S',
               importatori[self.name]['cella'],
               importatori[self.name]['cella'],
               a_chi_id,
               ric_interc,
               cella_chiamata,
               cella_chiamata,
               esito,
               cosa)
            if cosa == 'S':
            # sms: interrompo l'altro processo per farmi rispondere
                if importatori_linked[a_che_tipo] == 'importatori':
                # per ora ho implementato solo il processo degli importatori...
                    importatori[a_chi]['sms_from'] = ['importatori', self.name]
                    importatori_procs[a_chi].action.interrupt()
                    print("interrompo")
            if importatori[self.name]['ultimo_mov'] <= self.env.now:
            #  spostamento di cella
                importatori[self.name]['cella'] = random.randint(0,len(celle)-2)  # NON uso l'ultima cella che e' quella degli esportatori esteri
                importatori[self.name]['ultimo_mov'] = self.env.now + random.randint(t21_import, t22_import)
            prossima = random.randint(t11_import, t12_import)+durata
            try:
                yield self.env.timeout(prossima)
            except simpy.Interrupt:
            # ho ricevuto un sms, rispondo con una certa probabilita 
                if random.randint(1,10) >= sms_prob_risposta:
                    print("gestisco interruzione")
                    if importatori[self.name]['sms_from']:
                        ric_interc = 'N'
                        a_che_tipo = importatori[self.name]['sms_from'][0]
                        a_chi = importatori[self.name]['sms_from'][1]
                        if a_che_tipo in ('importatori','esportatori', 'spacciatori'):
                            ric_interc = 'S'
                        elif a_che_tipo == 'consumatori':
                            if consumatori[a_chi]['controllato']:
                                ric_interc = 'S' 
                        a_chi_id = eval(a_che_tipo+'['+str(a_chi)+']["id"]')
                        cella_chiamata = eval(a_che_tipo+'['+str(a_chi)+']["cella"]')
                        esito = 0 # sempre a buon fine per adesso...
                        print(self.env.now,
                           0,
                           importatori[self.name]['id'],
                           'S',
                           importatori[self.name]['cella'],
                           importatori[self.name]['cella'],
                           a_chi_id,
                           ric_interc,
                           cella_chiamata,
                           cella_chiamata,
                           esito,
                           'S*')  # aggiungo * provvisoriamente per debug
                        importatori[a_chi]['sms_from'] = ['importatori', self.name]
                        importatori_procs[a_chi].action.interrupt()
                        prossima = random.randint(t11_import, t12_import)+durata
                        # eventualmente vedere come gestire interruzioni successive
                        try:
                            yield self.env.timeout(prossima)
                        except simpy.Interrupt:
                            print("seconda interruzione", self.name)


importatori_procs = []
env = simpy.Environment()
for i in range(len(importatori)):
    importatori_procs.append(importatore(env, i))
env.run(until=9000)
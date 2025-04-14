from datetime import datetime

class Mesure:
    def __init__(self, dateHeureMesure, dataMesure, type_capteur="Mouvement"):
        self.dateHeureMesure = dateHeureMesure
        self.dataMesure = dataMesure
        self.type_capteur = type_capteur

    def __repr__(self):
        return f"Mesure({self.dateHeureMesure}, {self.dataMesure}, {self.type_capteur})"

    def afficherMesure(self):
        return f"Date et Heure de la mesure : {self.dateHeureMesure.strftime('%Y-%m-%d %H:%M:%S')}\n" \
               f"Données de la mesure : {self.dataMesure}"

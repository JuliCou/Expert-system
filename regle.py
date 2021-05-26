class Regle(object):
    """Classe mère Règle implémentée dans système expert"""
    def __init__(self, numero, definition, base_faits):
        self.numero = numero
        self.definition = definition
        self.base_faits = base_faits

    def application(self):
        pass

    def get_base_faits(self):
        return self.base_faits


# Règle 1:
class Regle1(Regle):
    """Classe fille de Regle pour la transformation des données issues des capteurs
    en faits ou prémisses."""
    def __init__(self, base_faits, donnees):
        Regle.__init__(self, 1, "Transformations données en faits", base_faits)
        self.donnees = donnees

    def application(self):
        # Présence
        self.base_faits["mvt"] = True
        if self.donnees["mvt_vie"] == 1 :
            self.base_faits["presence"] = "vie"
        elif self.donnees["mvt_sdb"] == 1 :
            self.base_faits["presence"] = "sdb"
        elif self.donnees["mvt_couloir"] == 1 :
            self.base_faits["presence"] = "couloir"
        elif self.donnees["mvt_cuisine"] == 1 :
            self.base_faits["presence"] = "cuisine"
        else:
            self.base_faits["mvt"] = False
        # Porte
        if self.donnees["porte"] == 1:
            self.base_faits["porte"] = True
        else:
            self.base_faits["porte"] = False
        # Fenêtre
        if self.donnees["fenetre"] == 1:
            self.base_faits["fenetre"] = True
        else:
            self.base_faits["fenetre"] = False
        # Temperature
        self.base_faits["temperature"] = self.donnees["temperature"]
        # Temps
        if self.base_faits["presence"] == "sdb":
            self.base_faits["dureeSDB"] += 2
        else:
            self.base_faits["dureeSDB"] = 0
        if self.base_faits["presence"] == "cuisine":
            self.base_faits["dureeCuisine"] += 2
        else:
            self.base_faits["dureeCuisine"] = 0
        if self.base_faits["temperature"] > 25:
            self.base_faits["dureeTsup25"] += 2
        else:
            self.base_faits["dureeTsup25"] = 0


# Règle 2:
class Regle2(Regle):
    """Classe fille de Regle pour remonter alerte si temps supérieur à 5 min dans la sdb"""
    def __init__(self, base_faits):
        Regle.__init__(self, 2, "Pas plus de 5 min dans la salle de bain", base_faits)

    def application(self):
        if self.base_faits["dureeSDB"] > 5 * 60 : 
            self.base_faits["alerte"] = True
            self.base_faits["messageAlerte"] = "Présence supérieure à 5 minutes dans la SDB"

# Règle 3:
class Regle3(Regle):
    """Classe fille de Regle pour remonter alerte si temps supérieur à 10 min dans la cuisine"""
    def __init__(self, base_faits):
        Regle.__init__(self, 3, "Pas plus de 10 min dans la cuisine", base_faits)

    def application(self):
        if self.base_faits["dureeCuisine"] > 10 * 60 : 
            self.base_faits["alerte"] = True
            self.base_faits["messageAlerte"] = "Présence supérieure à 10 minutes dans la cuisine"


# Règle 4:
class Regle4(Regle):
    """Classe fille de Regle pour remonter alerte si temperature inférieure à 16°C"""
    def __init__(self, base_faits):
        Regle.__init__(self, 4, "Température inférieure à 16°C", base_faits)

    def application(self):
        if self.base_faits["temperature"] < 16 : 
            self.base_faits["alerte"] = True
            if self.base_faits["fenetre"]:
                self.base_faits["messageAlerte"] = "Température inférieure à 16°C avec fenêtre ouverte."
            else:
                self.base_faits["messageAlerte"] = "Température inférieure à 16°C avec fenêtre fermée."


# Règle 5:
class Regle5(Regle):
    """Classe fille de Regle pour remonter alerte si temperature supérieure à 25°C"""
    def __init__(self, base_faits):
        Regle.__init__(self, 5, "Température supérieure à 25°C", base_faits)

    def application(self):
        if self.base_faits["dureeTsup25"] > 5 * 60 : 
            self.base_faits["alerte"] = True
            self.base_faits["messageAlerte"] = "Température supérieure à 25°C."


# Règle 6:
class Regle6(Regle):
    """Classe fille de Regle pour remonter alerte si la personne sort avec présence dans couloir."""
    def __init__(self, base_faits):
        Regle.__init__(self, 6, "La personne sort.", base_faits)

    def application(self):
        if self.base_faits["presence"] == "couloir" and self.base_faits["porte"] : 
            self.base_faits["alerte"] = True
            self.base_faits["messageAlerte"] = "La personne sort."


# Règle 7:
class Regle7(Regle):
    """Classe fille de Regle pour remonter alerte si il y a une intrusion."""
    def __init__(self, base_faits):
        Regle.__init__(self, 7, "Il y a une intrusion", base_faits)

    def application(self):
        if self.base_faits["presence"] != "couloir" and self.base_faits["porte"] : 
            self.base_faits["alerte"] = True
            self.base_faits["messageAlerte"] = "Il y a une intrusion."



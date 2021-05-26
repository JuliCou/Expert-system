import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import regle 


# Importation des données
data = pd.read_excel(io="simulation.xlsx",
                     header=None,
                     index_col=False).T
data.columns = ["mvt_vie", "mvt_sdb", "mvt_couloir", "mvt_cuisine", "porte", "fenetre", "temperature"]


## FAITS ou PREMISSES
# initialisation de la base de faits
base_faits = {}
base_faits["mvt"] = False
base_faits["dureeSDB"] = 0
base_faits["dureeCuisine"] = 0
base_faits["dureeTsup25"] = 0
base_faits["presence"] = "vie"
base_faits["alerte"] = False
base_faits["messageAlerte"] = ""

## Chainage avant - moteur d'inférence
i = 0

while not(base_faits["alerte"]) and i < data.shape[0]:
    print("Temps : ", str(2*i), " secondes")
    donnees = data.iloc[i]
    i += 1
    # Transformation données en faits
    regleBF = regle.Regle1(base_faits, donnees)
    regleBF.application()
    base_faits = regleBF.get_base_faits()
    # Base de règles
    rg = []
    rg.append(regle.Regle2(base_faits))
    rg.append(regle.Regle3(base_faits))
    rg.append(regle.Regle4(base_faits))
    rg.append(regle.Regle5(base_faits))
    rg.append(regle.Regle6(base_faits))
    rg.append(regle.Regle7(base_faits))
    # Application des règles
    while not(base_faits["alerte"]) and rg != []:
        rg[0].application()
        base_faits = rg[0].get_base_faits()
        rg.pop(0)
        if base_faits["alerte"]:
            print(base_faits["messageAlerte"])
            break
        # else:
        #    log("Pas d'alerte")
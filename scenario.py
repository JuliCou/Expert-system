import xlsxwriter
import numpy as np


# Duree de simulation 15 mn
TIME_STEP = 2
Duree = 15*60
N = int(Duree/TIME_STEP)
Mesure = np.zeros([7,N])

# Un scénario tout simple
# La personne va au bout de 20s à la SDB, y reste 2 mn puis revient dans la chambre de vie
# La personne va au bout de 4mn à la cuisine, y reste 6 mn puis revient dans la chambre de vie
# La tempréature à partir de 8mn passe à 28 degre
# La fenetre est détectée ouverte à partir de 7mn

# Vie
periode_Vie = [[120, 121], [310,312]]

# SDB
periode_SDB = [[30, 31]]

# Couloir
periode_Couloir = [[300, 302]]

# Cuisine
periode_Cuisine  =[]

# Porte
periode_porte = []

#Fenêtre
Mesure[5,int(7*60/TIME_STEP):N]=1

#Temperature
Mesure[6,:] = 20
Mesure[6,int(8*60/TIME_STEP):N] = 15



for b in range(len(periode_Vie)):
    Mesure[0,int(periode_Vie[b][0]/TIME_STEP):int(periode_Vie[b][1]/TIME_STEP)]=1

for b in range(len(periode_SDB)):
    Mesure[1,int(periode_SDB[b][0]/TIME_STEP):int(periode_SDB[b][1]/TIME_STEP)]=1

for b in range(len(periode_Couloir)):
    Mesure[2,int(periode_Couloir[b][0]/TIME_STEP):int(periode_Couloir[b][1]/TIME_STEP)]=1

for b in range(len(periode_Cuisine)):
    Mesure[3,int(periode_Cuisine[b][0]/TIME_STEP):int(periode_Cuisine[b][1]/TIME_STEP)]=1

for b in range(len(periode_porte)):
    Mesure[4,int(periode_porte[b][0]/TIME_STEP):int(periode_porte[b][1]/TIME_STEP)]=1

 

Mesure_Global=('simulation.xlsx')

workbook = xlsxwriter.Workbook(Mesure_Global)

worksheet = workbook.add_worksheet('Mesure')
for temps in range(N):
    for ind_cap in range(7):
        worksheet.write(ind_cap,temps,Mesure[ind_cap,temps])
   

workbook.close()

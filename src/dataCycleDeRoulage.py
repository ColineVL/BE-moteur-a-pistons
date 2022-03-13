from openpyxl import load_workbook

"""
On charge les données du cycle de roulage.
"""

wb = load_workbook("tp_pistons.xlsx")
sheet = wb[wb.sheetnames[0]]


def cleanValue(value):
    return float(value)


def cleanValueInt(value):
    return int(value)


# [s] Temps
t = [cleanValue(cell.value) for cell in sheet["A"][1:]]
# [km/h] Vitesse du véhicule
v_veh = [cleanValue(cell.value) for cell in sheet["B"][1:]]
# [°] Pente de la route
pente = [cleanValue(cell.value) for cell in sheet["C"][1:]]
# [-] Rapport de boite engagé
rapport = [cleanValueInt(cell.value) for cell in sheet["D"][1:]]
# [mg/cp] Débit de carburant (mg/cp : milligrammes par coup, masse de carburant injectée par cylindre pour 1 cycle thermodynamique)
q_carb_mgcp = [cleanValue(cell.value) for cell in sheet["E"][1:]]

# delta_t [s] Ecart entre deux prises de mesures
delta_t = t[1] - t[0]

assert len(t) == len(v_veh) == len(pente) == len(rapport) == len(q_carb_mgcp)

nbEtapes = len(t)
print(f"Chargé {nbEtapes} lignes du fichier")

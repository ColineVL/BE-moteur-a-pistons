dict_valeursGlobales = {
    # Rapport des régimes de rotation moteur/roue, pour chacun des rapports de transmission
    "r_moteur_roue": {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
    },
    # Rendement effectif du moteur
    "rend_e": 0,
    # Consommation en carburant sur ce cycle C [L/100km]
    "C": 0,
    # Energie introduite sous forme de carburant E_carb [kW.h]
    "E_carb": 0,
    # Emission de CO2 du véhicule sur ce cycle CO2 [g/km]
    "CO2": 0,
    # Energie de traction lorsque le conducteur demande un couple positif en kW.h
    "E_traction_ap": 0,
    # Energie de traction lorsque le conducteur demande un couple négatif en kW.h
    "E_traction_an": 0,
    # Energie disponible à la roue si l’intégralité de E_traction_an est récupérée (en kW.h)
    "E_traction_elec": 0,
    # Energie de traction restant à fournir par le moteur thermique, en kW.h
    "E_traction_therm": 0,
    # Rendement de traction thermique
    "rend_traction_therm": 0,
    # Energie à introduire sous forme de carburant en kW.h
    "E_carb_hyb": 0,
    # Economie en énergie introduite sous forme de carburant en kW.h
    "eco_E_carb": 0,
    # Réduction de consommation de carburant en L
    "eco_V_carb": 0,
    # Réduction de consommation en L/100km
    "eco_C": 0,
}


def printAll():
    for key, value in dict_valeursGlobales.items():
        print(f"{key} : {value}")


# Quelques valeurs réutilisées entre les questions
M = []
F_tot = []
F_resistif = []
N_mot = []
Pe_mot = []
P_traction = []
distance_totale = 0

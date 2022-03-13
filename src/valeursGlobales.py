"""
On stocke les valeurs globales dans un dictionnaire.
Une fonction pour les afficher toutes dans la console.
"""

dict_valeursGlobales = {
    # [-] Rapport des régimes de rotation moteur/roue, pour chacun des rapports de transmission
    "r_moteur_roue": {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
    },
    # [-] Rendement effectif du moteur
    "rend_e": 0,
    # [L/100km] Consommation en carburant sur ce cycle
    "C": 0,
    # [kW.h] Energie introduite sous forme de carburant
    "E_carb": 0,
    # [g/km] Emission de CO2 du véhicule sur ce cycle
    "CO2": 0,
    # [kW.h] Energie de traction lorsque le conducteur demande un couple positif
    "E_traction_ap": 0,
    # [kW.h] Energie de traction lorsque le conducteur demande un couple négatif
    "E_traction_an": 0,
    # [kW.h] Energie disponible à la roue si l’intégralité de E_traction_an est récupérée
    "E_traction_elec": 0,
    # [kW.h] Energie de traction restant à fournir par le moteur thermique
    "E_traction_therm": 0,
    # [-] Rendement de traction thermique
    "rend_traction_therm": 0,
    # [kW.h] Energie à introduire sous forme de carburant
    "E_carb_hyb": 0,
    # [kW.h] Economie en énergie introduite sous forme de carburant
    "eco_E_carb": 0,
    # [L] Réduction de consommation de carburant
    "eco_V_carb": 0,
    # [L/100km] Réduction de consommation
    "eco_C": 0,
}


def printAll():
    for key, value in dict_valeursGlobales.items():
        print(f"{key} : {value}")

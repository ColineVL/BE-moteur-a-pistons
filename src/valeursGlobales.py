# Rapport des régimes de rotation moteur/roue, pour chacun des rapports de transmission
r_moteur_roue = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
}


# Consommation en carburant sur ce cycle C [L/100km]
C = 0
# Energie introduite sous forme de carburant E_carb [kW.h]
E_carb = 0
# Emission de CO2 du véhicule sur ce cycle CO2 [g/km]
CO2 = 0


# Energie de traction lorsque le conducteur demande un couple positif en kW.h
E_traction_ap = 0
# Energie de traction lorsque le conducteur demande un couple négatif en kW.h
E_traction_an = 0

# Energie à introduire sous forme de carburant en kW.h
E_carb_hyb = 0
# En supposant que le moteur thermique n’a plus qu’à fournir l’énergie E_traction_therm en kW.h
E_traction_therm = 0

# Economie en énergie introduite sous forme de carburant en kW.h
eco_E_carb = 0
# Réduction de consommation de carburant en L
eco_V_carb = 0
# Réduction de consommation en L/100km
eco_C = 0

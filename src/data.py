"""
Constantes du problème
"""

""" Véhicule """
# MVODM (masse à vide en ordre de mission) en kg
M_veh = 1420
# SCx en m²
SCx = 0.712
# Coeff de résistance au roulement des pneus en kg/t
Crr = 6.2
# Rayon de roue en m
R_roue = 0.3067

""" Transmission - moteur """
# Force résistante mécanique en N
F_meca_cte = 50
# Inertie des masses en rotation en kg.m²
I = 0.16
# Rendement de transmission
rend_trans = 0.8
# Régime de ralenti en tr/min
N_ralenti = 850

""" Boite de vitesse """
# V1000 1ère en kmh/h par 1000tr/min
V1000_1 = 8.71
# V1000 2ème en kmh/h par 1000tr/min
V1000_2 = 14.91
# V1000 3ème en kmh/h par 1000tr/min
V1000_3 = 23.30
# V1000 4ème en kmh/h par 1000tr/min
V1000_4 = 33.29
# V1000 5ème en kmh/h par 1000tr/min
V1000_5 = 44.36
# V1000 6ème en kmh/h par 1000tr/min
V1000_6 = 57.96
# On regroupe les vitesses dans un tableau pour simplifier
dict_V1000 = {
    0: 0,
    1: V1000_1,
    2: V1000_2,
    3: V1000_3,
    4: V1000_4,
    5: V1000_5,
    6: V1000_6,
}

""" Autres """
# Constante de gravitation en m/s²
g = 9.81
# Densité de l'air en kg/m3
rho_air = 1.2
# Pouvoir calorifique du carburant en MJ/kg
PCI = 42.72
# Densité du carburant en kg/m3
rho_carb = 834
# Fraction molaire d'hydrogène du carburant
Y = 2.052
# Masse molaire de l'hydrogène en g/mol
M_H = 1
# Masse molaire du carbone en g/mol
M_C = 12
# Masse molaire de l'oxygène en g/mol
M_O = 16
# Nombre de cylindres du moteur
n_cyl = 4


""" Pleine charge """
# N en tr/min
# C en N.m
# dict_pleine_charge[N] = C
dict_pleine_charge = {
    750: 100,
    1000: 122,
    1250: 175,
    1500: 236,
    1750: 265,
    2000: 274,
    2250: 273,
    2500: 272,
    2750: 262,
    3000: 253,
    3250: 223,
    3500: 221,
    3750: 216,
    4000: 210,
    4250: 199,
    4500: 166,
    4750: 137,
    5000: 125,
}

"""
Constantes du problème.
"""

""" Véhicule """
# [kg] MVODM (masse à vide en ordre de mission)
M_veh = 1420
# [m²] SCx
SCx = 0.712
# [kg/t] Coeff de résistance au roulement des pneus
Crr = 6.2
# [m] Rayon de roue
R_roue = 0.3067

""" Transmission - moteur """
# [N] Force résistante mécanique
F_meca_cte = 50
# [kg.m²] Inertie des masses en rotation
I = 0.16
# [-] Rendement de transmission
rend_trans = 0.8
# [tr/min] Régime de ralenti
N_ralenti = 850

""" Boite de vitesse """
# [kmh/h par 1000tr/min] V1000 1ère
V1000_1 = 8.71
# [kmh/h par 1000tr/min] V1000 2ème
V1000_2 = 14.91
# [kmh/h par 1000tr/min] V1000 3ème
V1000_3 = 23.30
# [kmh/h par 1000tr/min] V1000 4ème
V1000_4 = 33.29
# [kmh/h par 1000tr/min] V1000 5ème
V1000_5 = 44.36
# [kmh/h par 1000tr/min] V1000 6ème
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
# [m/s²] Constante de gravitation
g = 9.81
# [kg/m3] Densité de l'air
rho_air = 1.2
# [MJ/kg] Pouvoir calorifique du carburant
PCI = 42.72
# [kg/m3] Densité du carburant
rho_carb = 834
# [-] Fraction molaire d'hydrogène du carburant
Y = 2.052
# [g/mol] Masse molaire de l'hydrogène
M_H = 1
# [g/mol] Masse molaire du carbone
M_C = 12
# [g/mol] Masse molaire de l'oxygène
M_O = 16
# [-] Nombre de cylindres du moteur
n_cyl = 4


""" Pleine charge """
# [tr/min] N
# [N.m] C
# On aura dict_pleine_charge[N] = C
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

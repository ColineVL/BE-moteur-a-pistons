from math import pi, sin, cos

import valeursGlobales
from data import (
    M_veh,
    SCx,
    Crr,
    R_roue,
    F_meca_cte,
    I,
    rend_trans,
    N_ralenti,
    dict_V1000,
    g,
    rho_air,
    PCI,
    rho_carb,
    Y,
    M_H,
    M_C,
    M_O,
    n_cyl,
    dict_pleine_charge,
)
from dataCycleDeRoulage import t, v_veh, pente, rapport, q_carb, nbEtapes
from fonctions import *

# Quelques valeurs réutilisées entre les questions
M = []
F_tot = []
F_resistif = []
N_mot = []


def calculRegimeMoteur():
    """1. Calcul régime moteur"""
    print("Question 1")
    for rap, V1000 in dict_V1000.items():
        valeursGlobales.r_moteur_roue[rap] = (
            (2 * pi * 60 * R_roue) / V1000 if V1000 != 0 else 0
        )

    N_mot = [
        max(1000 * v_veh[i] / dict_V1000[rapport[i]], N_ralenti)
        if rapport[i] != 0
        else N_ralenti
        for i in range(nbEtapes)
    ]

    plot(N_mot, "N_mot", 1)


def calculEffortsResistifs():
    """2. Calcul des efforts résistifs"""
    print("Question 2")
    # theta angle de la pente en radian
    theta = [conversionDegreToRadian(pente[i]) for i in range(nbEtapes)]

    F_rr = [
        M_veh * g * cos(theta[i]) * Crr[i] if v_veh[i] != 0 else 0
        for i in range(nbEtapes)
    ]
    F_meca = [F_meca_cte if v_veh[i] != 0 else 0 for i in range(nbEtapes)]
    F_pente = [M_veh * g * sin(theta[i]) for i in range(nbEtapes)]
    F_aero = [
        0.5 * rho_air * conversionKmhToMs(v_veh[i]) ** 2 * SCx for i in range(nbEtapes)
    ]
    F_resistif = [F_pente[i] + F_aero[i] + F_rr[i] + F_meca[i] for i in range(nbEtapes)]

    plot(F_pente, "F_pente", 2)
    plot(F_aero, "F_aero", 2)
    plot(F_meca, "F_meca", 2)
    plot(F_rr, "F_rr", 2)
    plot(F_resistif, "F_resistif", 2)


def calculMasses():
    """3. Calcul des masses"""
    print("Question 3")
    M_eq = [
        I * rend_trans * (valeursGlobales.r_moteur_roue[rapport[i]] / R_roue) ** 2
        for i in range(nbEtapes)
    ]
    M = [M_veh + M_eq[i] for i in range(nbEtapes)]

    plot(M_eq, "M_eq", 3)
    plot(M, "M", 3)


def calculEffortTotal():
    """4. Calcul de l'effort total"""
    print("Question 4")
    a = [
        (conversionKmhToMs(v_veh[i]) - conversionKmhToMs(v_veh[i - 1]))
        / (t[i] - t[i - 1])
        for i in range(nbEtapes)
    ]
    F_tot = [M[i] * a[i] for i in range(nbEtapes)]
    plot(a, "a", 4.1)
    plot(F_tot, "F_tot", 4.2)


def calculCoupleEffectifMoteur():
    """5. Calcul du couple effectif moteur"""
    print("Question 5")
    F_traction = [F_tot[i] - F_resistif[i] for i in range(nbEtapes)]
    C_roue = [F_traction[i] * R_roue for i in range(nbEtapes)]

    plot(F_traction, "F_traction", 5.1)
    plot(C_roue, "C_roue", 5.2)

    # TODO Ce_mot
    Ce_mot = []
    # Ce_mot = (C_roue - C_mot * r_moteur_roue) / r_me_roue
    # r_moteur_roue = vit_rotation_mth / vit_rotation_roue
    # r_me_roue = vit_rotation_me / vit_rotation_roue

    # Puissance en W = vitesse_rotation en rad/s * couple en N.m
    # omega_mot vitesse de rotation du moteur en rad/s
    omega_mot = [
        conversionTourParMinuteToRadParSeconde(N_mot[i]) for i in range(nbEtapes)
    ]
    # FIXME ici je suis vraiment pas sûre de P_traction
    Pe_mot = [Ce_mot[i] * omega_mot[i] / 1000 for i in range(nbEtapes)]
    P_traction = [C_roue[i] * omega_mot[i] / 1000 for i in range(nbEtapes)]

    plot(Ce_mot, "Ce_mot", 5.2)
    plot(Pe_mot, "Pe_mot", 5.4)
    plot(P_traction, "P_traction", 5.4)


def calculRendementEffectifConsoEtCO2():
    """6. Calcul du rendement effectif, de la consommation et du CO2"""
    print("Question 6")
    # TODO q_carb
    # TODO P_carb
    # TODO rend_e
    # TODO C
    # TODO E_carb

    # Question 6.6
    M_CHY = M_C + M_H * Y
    M_CO2 = M_C + 2 * M_O

    # On a C en litres / 100 km
    # Conversion en m3
    Cm3 = 0.001 * valeursGlobales.C
    # Conversion en g
    Cg = Cm3 * rho_carb * 1000
    # Tout ça c'est pour 100 km, pour 1 km je divise donc
    masse_carburant = Cg / 100
    valeursGlobales.CO2 = masse_carburant * M_CO2 / M_CHY


def evaluationAdaptationSurCycle():
    """7. Evaluation de l'adaptation moteur / véhicule / boite sur ce cycle"""
    print("Question 7")


def evaluationPotentielDeceleration():
    """8. Evaluation du potentiel de récupération d'énergie à la décélération"""
    print("Question 8")


### Notes
# Cf pages 112 et 154
# N_roue = [v_veh[i] / (2 * pi * R_roue) for i in range(nbEtapes)]

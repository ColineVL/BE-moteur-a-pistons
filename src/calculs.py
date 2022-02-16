from math import pi, atan, sin, cos
import matplotlib.pyplot as plt

import valeursGlobales
from data import *
from dataCycleDeRoulage import t, v_veh, pente, rapport, q_carb, nbEtapes

# Quelques valeurs réutilisées entre les questions
M = []
F_tot = []
F_resistif = []

plt.show()


def plot(data, titre):
    fig = plt.figure(titre)
    plt.plot(data)


def calculRegimeMoteur():
    """1. Calcul régime moteur"""
    print("Question 1")
    for rapport, V1000 in boite_de_vitesse_V1000.items():
        valeursGlobales.r_moteur_roue[rapport] = (2 * pi * 60 * R_roue) / V1000

    # FIXME ici on n'a pas besoin de ce qu'on vient de calculer, c'est bizarre
    N_mot = [max(1000 * v_veh[i] / V1000, N_ralenti) for i in range(nbEtapes)]

    plot(N_mot, "N_mot")


def calculEffortsResistifs():
    """2. Calcul des efforts résistifs"""
    print("Question 2")
    # Question 2.1
    # theta angle de la pente en radian
    F_rr = []

    theta = [atan(pente[i] / 100) for i in range(nbEtapes)]
    F_pente = [M_veh * g * sin(theta[i]) for i in range(nbEtapes)]
    F_aero = [0.5 * rho_air * v_veh[i] ** 2 * SCx for i in range(nbEtapes)]
    F_resistif = [
        F_pente[i] + F_aero[i] + F_rr[i] for i in range(nbEtapes)
    ]  # Attention aux signes

    # TODO F_meca ???
    # TODO F_rr ???

    plot(F_pente, "F_pente")
    plot(F_aero, "F_aero")
    plot(F_meca, "F_meca")
    plot(F_rr, "F_rr")
    plot(F_resistif, "F_resistif")


def calculMasses():
    """3. Calcul des masses"""
    print("Question 3")
    M_eq = []
    eta_trans = 1  # rapport global de transmission, TODO à calculer
    M_eq = [
        I * eta_trans * (valeursGlobales.r_moteur_roue[rapport[i]] / R_roue) ** 2
        for i in range(nbEtapes)
    ]
    M = [M_veh + M_eq[i] for i in range(nbEtapes)]

    plot(M_eq, "M_eq")
    plot(M, "M")


def calculEffortTotal():
    """4. Calcul de l'effort total"""
    print("Question 4")

    # Question 4.1
    a = [(v_veh[i] - v_veh[i - 1]) / (t[i] - t[i - 1]) for i in range(nbEtapes)]
    F_tot = [M[i] * a[i] for i in range(nbEtapes)]
    plot(a, "a")
    plot(F_tot, "F_tot")


def calculCoupleEffectifMoteur():
    """5. Calcul du couple effectif moteur"""
    print("Question 5")
    F_traction = [F_tot[i] - F_resistif[i] for i in range(nbEtapes)]
    C_roue = [F_traction[i] * R_roue for i in range(nbEtapes)]

    plot(F_traction, "F_traction")
    plot(C_roue, "C_roue")

    # TODO Ce_mot
    # Ce_mot = (C_roue - C_mot * r_moteur_roue) / r_me_roue
    # r_moteur_roue = vit_rotation_mth / vit_rotation_roue
    # r_me_roue = vit_rotation_me / vit_rotation_roue

    # Puissance en W = vitesse_rotation en rad/s * couple en N.m
    # TODO Pe_mot
    # TODO P_traction


def calculRendementEffectifConsoEtCO2():
    """6. Calcul du rendement effectif, de la consommation et du CO2"""
    print("Question 6")
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

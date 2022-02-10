from math import pi, atan, sin, cos
import matplotlib.pyplot as plt

import valeursGlobales
from data import *
from dataCycleDeRoulage import t, v_veh, pente, rapport, q_carb, nbEtapes

# Quelques valeurs réutilisées entre les questions
M = []
F_tot = []
F_resistif = []


def calculRegimeMoteur():
    """1. Calcul régime moteur"""
    print("Question 1")
    for rapport, V1000 in boite_de_vitesse_V1000.items():
        valeursGlobales.r_moteur_roue[rapport] = (2 * pi * 60 * R_roue) / V1000

    # FIXME ici on n'a pas besoin de ce qu'on vient de calculer, c'est bizarre
    N_mot = []
    for i in range(nbEtapes):
        N_mot[i] = 1000 * v_veh[i] / V1000
        if N_mot[i] < N_ralenti:
            N_mot[i] = N_ralenti
    plt.plot(N_mot, label="N_mot")


def calculEffortsResistifs():
    """2. Calcul des efforts résistifs"""
    print("Question 2")
    # Question 2.1
    # theta angle de la pente en radian
    theta = []
    F_pente = []
    F_aero = []
    F_meca = []
    F_rr = []

    for i in range(nbEtapes):
        theta[i] = atan(pente[i] / 100)

        F_pente = M_veh * g * sin(theta)

        F_aero = 0.5 * rho_air * v_veh**2 * SCx

        # TODO F_meca ???
        # TODO F_rr ???

        F_resistif[i] = F_pente[i] + F_aero[i] + F_rr[i]  # Attention aux signes

    plt.plot(F_pente, label="F_pente")
    plt.plot(F_aero, label="F_aero")
    plt.plot(F_meca, label="F_meca")
    plt.plot(F_rr, label="F_rr")
    plt.plot(F_resistif, label="F_resistif")


def calculMasses():
    """3. Calcul des masses"""
    print("Question 3")
    M_eq = []
    eta_trans = 1  # rapport global de transmission, TODO à calculer
    for i in range(nbEtapes):
        M_eq[i] = (
            I * eta_trans * (valeursGlobales.r_moteur_roue[rapport[i]] / R_roue) ** 2
        )
        M[i] = M_veh + M_eq[i]
    plt.plot(M_eq, label="M_eq")
    plt.plot(M, label="M")


def calculEffortTotal():
    """4. Calcul de l'effort total"""
    print("Question 4")

    # Question 4.1
    a = []
    for i in range(nbEtapes):
        a[i] = (v_veh[i] - v_veh[i - 1]) / (t[i] - t[i - 1])
        F_tot[i] = M[i] * a[i]
    plt.plot(a, label="a")
    plt.plot(F_tot, label="F_tot")


def calculCoupleEffectifMoteur():
    """5. Calcul du couple effectif moteur"""
    print("Question 5")
    F_traction = []
    C_roue = []
    for i in range(nbEtapes):
        F_traction[i] = F_tot[i] - F_resistif[i]
        C_roue[i] = F_traction[i] * R_roue

    plt.plot(F_traction, label="F_traction")
    plt.plot(C_roue, label="C_roue")

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
# N_roue[i] = v_veh[i] / (2 * pi * R_roue)

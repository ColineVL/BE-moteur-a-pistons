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
from dataCycleDeRoulage import t, v_veh, pente, rapport, q_carb_mgcp, nbEtapes
from fonctions import *


def calculRegimeMoteur():
    """1. Calcul régime moteur"""
    print("Question 1")
    for rap, V1000 in dict_V1000.items():
        valeursGlobales.r_moteur_roue[rap] = (
            (2 * pi * 60 * R_roue) / V1000 if V1000 != 0 else 0
        )

    valeursGlobales.N_mot = [
        max(1000 * v_veh[i] / dict_V1000[rapport[i]], N_ralenti)
        if rapport[i] != 0
        else N_ralenti
        for i in range(nbEtapes)
    ]

    # plot(valeursGlobales.N_mot, "N_mot", 1)


def calculEffortsResistifs():
    """2. Calcul des efforts résistifs"""
    print("Question 2")
    # theta angle de la pente en radian
    theta = [conversionDegreToRadian(pente[i]) for i in range(nbEtapes)]

    F_rr = [
        M_veh * g * cos(theta[i]) * Crr * 0.001 if v_veh[i] != 0 else 0
        for i in range(nbEtapes)
    ]
    F_meca = [F_meca_cte if v_veh[i] != 0 else 0 for i in range(nbEtapes)]
    F_pente = [M_veh * g * sin(theta[i]) for i in range(nbEtapes)]
    F_aero = [
        0.5 * rho_air * conversionKmhToMs(v_veh[i]) ** 2 * SCx for i in range(nbEtapes)
    ]
    valeursGlobales.F_resistif = [
        F_pente[i] + F_aero[i] + F_rr[i] + F_meca[i] for i in range(nbEtapes)
    ]

    # plot(F_pente, "F_pente", 2)
    # plot(F_aero, "F_aero", 2)
    # plot(F_meca, "F_meca", 2)
    # plot(F_rr, "F_rr", 2)
    # plot(valeursGlobales.F_resistif, "F_resistif", 2)


def calculMasses():
    """3. Calcul des masses"""
    print("Question 3")
    M_eq = [
        I * rend_trans * (valeursGlobales.r_moteur_roue[rapport[i]] / R_roue) ** 2
        for i in range(nbEtapes)
    ]
    valeursGlobales.M = [M_veh + M_eq[i] for i in range(nbEtapes)]

    # plot(M_eq, "M_eq", 3)
    # plot(valeursGlobales.M, "M", 3)


def calculEffortTotal():
    """4. Calcul de l'effort total"""
    print("Question 4")
    a = [
        (conversionKmhToMs(v_veh[i]) - conversionKmhToMs(v_veh[i - 1]))
        / (t[i] - t[i - 1])
        if i != 0
        else 0
        for i in range(nbEtapes)
    ]
    valeursGlobales.F_tot = [valeursGlobales.M[i] * a[i] for i in range(nbEtapes)]
    # plot(a, "a", 41)
    # plot(valeursGlobales.F_tot, "F_tot", 42)


def calculCoupleEffectifMoteur():
    """5. Calcul du couple effectif moteur"""
    print("Question 5")
    F_traction = [
        valeursGlobales.F_tot[i] + valeursGlobales.F_resistif[i]
        for i in range(nbEtapes)
    ]
    C_roue = [F_traction[i] * R_roue for i in range(nbEtapes)]

    plot(F_traction, "F_traction", 51)
    plot(C_roue, "C_roue", 52)

    Ce_mot = [
        C_roue[i] / (valeursGlobales.r_moteur_roue[rapport[i]] * rend_trans)
        if rapport[i] != 0
        else 0
        for i in range(nbEtapes)
    ]

    # Puissance en W = vitesse_rotation en rad/s * couple en N.m
    # omega_mot vitesse de rotation du moteur en rad/s
    omega_mot = [
        conversionTourParMinuteToRadParSeconde(valeursGlobales.N_mot[i])
        for i in range(nbEtapes)
    ]
    valeursGlobales.Pe_mot = [Ce_mot[i] * omega_mot[i] / 1000 for i in range(nbEtapes)]
    P_traction = [
        F_traction[i] * conversionKmhToMs(v_veh[i]) / 1000 for i in range(nbEtapes)
    ]

    plot(Ce_mot, "Ce_mot", 52)
    plot(valeursGlobales.Pe_mot, "Pe_mot", 54)
    plot(P_traction, "P_traction", 54)


def calculRendementEffectifConsoEtCO2():
    """6. Calcul du rendement effectif, de la consommation et du CO2"""
    print("Question 6")
    q_carb = [n_cyl * valeursGlobales.N_mot[i] / 2 for i in range(nbEtapes)]
    plot(q_carb, "q_carb", 61)
    P_carb = [q_carb[i] * PCI / 1000 for i in range(nbEtapes)]
    plot(P_carb, "P_carb", 62)
    rend_e = [valeursGlobales.Pe_mot[i] / P_carb[i] for i in range(nbEtapes)]
    plot(rend_e, "rend_e", 63)
    # masse_carburant_totale [kg] masse totale de carburant consommée sur tout le trajet
    masse_carburant_totale = (
        sum(q_carb[i] * (t[i] - t[i - 1]) for i in range(1, nbEtapes)) / 1000000
    )
    # conso_carburant_totale [litres] conso totale
    conso_carburant_totale = conversionCarburantKgToLitres(masse_carburant_totale)
    # distance_totale [km] distance totale parcourue pendant le trajet
    distance_totale = sum(
        conversionKmhToKms(v_veh[i]) * (t[i] - t[i - 1]) for i in range(1, nbEtapes)
    )
    # On convertit en litres aux 100 km
    valeursGlobales.C = conso_carburant_totale * 100 / distance_totale

    valeursGlobales.E_carb = conversionMJTokWh(PCI) * masse_carburant_totale

    M_CHY = M_C + M_H * Y
    M_CO2 = M_C + 2 * M_O
    # masse_carburant_au_km [g] masse de carburant par km
    masse_carburant_au_km = masse_carburant_totale / distance_totale * 1000
    valeursGlobales.CO2 = masse_carburant_au_km * M_CO2 / M_CHY


def evaluationAdaptationSurCycle():
    """7. Evaluation de l'adaptation moteur / véhicule / boite sur ce cycle"""
    print("Question 7")


def evaluationPotentielDeceleration():
    """8. Evaluation du potentiel de récupération d'énergie à la décélération"""
    print("Question 8")


### Notes
# Cf pages 112 et 154
# N_roue = [v_veh[i] / (2 * pi * R_roue) for i in range(nbEtapes)]

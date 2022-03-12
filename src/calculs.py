from math import pi, sin, cos

from valeursGlobales import dict_valeursGlobales
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
        dict_valeursGlobales["r_moteur_roue"][rap] = (
            (2 * pi * 60 * R_roue) / V1000 if V1000 != 0 else 0
        )

    valeursGlobales.N_mot = [
        max(1000 * v_veh[i] / dict_V1000[rapport[i]], N_ralenti)
        if rapport[i] != 0
        else N_ralenti
        for i in range(nbEtapes)
    ]
    plot(valeursGlobales.N_mot, "N_mot")


def calculEffortsResistifs():
    """2. Calcul des efforts résistifs"""
    print("Question 2")
    # theta angle de la pente en radian
    theta = [conversionDegreToRadian(pente[i]) for i in range(nbEtapes)]

    F_rr = [
        M_veh * g * cos(theta[i]) * Crr * 0.001 if v_veh[i] != 0 else 0
        for i in range(nbEtapes)
    ]
    plot(F_rr, "F_rr")
    F_meca = [F_meca_cte if v_veh[i] != 0 else 0 for i in range(nbEtapes)]
    plot(F_meca, "F_meca")
    F_pente = [M_veh * g * sin(theta[i]) for i in range(nbEtapes)]
    plot(F_pente, "F_pente")
    F_aero = [
        0.5 * rho_air * conversionKmhToMs(v_veh[i]) ** 2 * SCx for i in range(nbEtapes)
    ]
    plot(F_aero, "F_aero")
    valeursGlobales.F_resistif = [
        F_pente[i] + F_aero[i] + F_rr[i] + F_meca[i] for i in range(nbEtapes)
    ]
    plot(valeursGlobales.F_resistif, "F_resistif")


def calculMasses():
    """3. Calcul des masses"""
    print("Question 3")
    M_eq = [
        I
        * rend_trans
        * (dict_valeursGlobales["r_moteur_roue"][rapport[i]] / R_roue) ** 2
        for i in range(nbEtapes)
    ]
    plot(M_eq, "M_eq")
    valeursGlobales.M = [M_veh + M_eq[i] for i in range(nbEtapes)]
    plot(valeursGlobales.M, "M")


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
    plot(a, "a")
    valeursGlobales.F_tot = [valeursGlobales.M[i] * a[i] for i in range(nbEtapes)]
    plot(valeursGlobales.F_tot, "F_tot")


def calculCoupleEffectifMoteur():
    """5. Calcul du couple effectif moteur"""
    print("Question 5")
    F_traction = [
        valeursGlobales.F_tot[i] + valeursGlobales.F_resistif[i]
        for i in range(nbEtapes)
    ]
    plot(F_traction, "F_traction")
    C_roue = [F_traction[i] * R_roue for i in range(nbEtapes)]
    plot(C_roue, "C_roue")

    Ce_mot = [
        C_roue[i] / (dict_valeursGlobales["r_moteur_roue"][rapport[i]] * rend_trans)
        if rapport[i] != 0
        else 0
        for i in range(nbEtapes)
    ]
    plot(Ce_mot, "Ce_mot")

    # Puissance en W = vitesse_rotation en rad/s * couple en N.m
    # omega_mot vitesse de rotation du moteur en rad/s
    omega_mot = [
        conversionTourParMinuteToRadParSeconde(valeursGlobales.N_mot[i])
        for i in range(nbEtapes)
    ]
    valeursGlobales.Pe_mot = [Ce_mot[i] * omega_mot[i] / 1000 for i in range(nbEtapes)]
    plot(valeursGlobales.Pe_mot, "Pe_mot")
    valeursGlobales.P_traction = [
        F_traction[i] * conversionKmhToMs(v_veh[i]) / 1000 for i in range(nbEtapes)
    ]
    plot(valeursGlobales.P_traction, "P_traction")


def calculRendementEffectifConsoEtCO2():
    """6. Calcul du rendement effectif, de la consommation et du CO2"""
    print("Question 6")
    q_carb = [
        q_carb_mgcp[i]
        * n_cyl
        * conversionTrParMinToTrParSec(valeursGlobales.N_mot[i])
        / 2
        for i in range(nbEtapes)
    ]
    plot(q_carb, "q_carb")
    P_carb = [q_carb[i] * PCI / 1000 for i in range(nbEtapes)]
    plot(P_carb, "P_carb")
    rend_e = [
        valeursGlobales.Pe_mot[i] / P_carb[i] if P_carb[i] != 0 else 0
        for i in range(nbEtapes)
    ]
    plot(rend_e, "rend_e")
    # masse_carburant_totale [kg] masse totale de carburant consommée sur tout le trajet
    masse_carburant_totale = (
        sum(q_carb[i] * (t[i] - t[i - 1]) for i in range(1, nbEtapes)) / 1000000
    )
    # conso_carburant_totale [litres] conso totale
    conso_carburant_totale = conversionCarburantKgToLitres(masse_carburant_totale)
    # distance_totale [km] distance totale parcourue pendant le trajet
    valeursGlobales.distance_totale = sum(
        conversionKmhToKms(v_veh[i]) * (t[i] - t[i - 1]) for i in range(1, nbEtapes)
    )
    # On convertit en litres aux 100 km
    dict_valeursGlobales["C"] = (
        conso_carburant_totale * 100 / valeursGlobales.distance_totale
    )

    dict_valeursGlobales["E_carb"] = conversionMJTokWh(PCI) * masse_carburant_totale

    M_CHY = M_C + M_H * Y
    M_CO2 = M_C + 2 * M_O
    # masse_carburant_au_km [g] masse de carburant par km
    masse_carburant_au_km = (
        masse_carburant_totale / valeursGlobales.distance_totale * 1000
    )
    dict_valeursGlobales["CO2"] = masse_carburant_au_km * M_CO2 / M_CHY


def evaluationAdaptationSurCycle():
    """7. Evaluation de l'adaptation moteur / véhicule / boite sur ce cycle"""
    print("Question 7")


def evaluationPotentielDeceleration():
    """8. Evaluation du potentiel de récupération d'énergie à la décélération"""
    print("Question 8")
    # Puissance de traction
    P_traction_ap = [max(valeursGlobales.P_traction[i], 0) for i in range(nbEtapes)]
    plot(P_traction_ap, "P_traction_ap")
    P_traction_an = [min(valeursGlobales.P_traction[i], 0) for i in range(nbEtapes)]
    plot(P_traction_an, "P_traction_an")

    # Energie de traction
    dict_valeursGlobales["E_traction_ap"] = sum(
        P_traction_ap[i] * conversionSecondeToHeure(t[i] - t[i - 1])
        for i in range(1, nbEtapes)
    )
    dict_valeursGlobales["E_traction_an"] = sum(
        P_traction_an[i] * conversionSecondeToHeure(t[i] - t[i - 1])
        for i in range(1, nbEtapes)
    )

    # Energie disponible
    dict_valeursGlobales["E_traction_elec"] = (
        0.8 * dict_valeursGlobales["E_traction_an"]
    )
    # Energie restante
    dict_valeursGlobales["E_traction_therm"] = (
        dict_valeursGlobales["E_traction_ap"] - dict_valeursGlobales["E_traction_elec"]
    )
    # Rendement
    dict_valeursGlobales["rend_traction_therm"] = (
        dict_valeursGlobales["E_traction_therm"] / dict_valeursGlobales["E_carb"]
    )
    # Energie à introduire
    dict_valeursGlobales["E_carb_hyb"] = (
        dict_valeursGlobales["E_traction_therm"]
        / dict_valeursGlobales["rend_traction_therm"]
    )

    # Economies
    dict_valeursGlobales["eco_E_carb"] = (
        dict_valeursGlobales["E_carb"] - dict_valeursGlobales["E_carb_hyb"]
    )
    # assert dict_valeursGlobales["eco_E_carb"] != 0
    # eco_carburant_masse = conversionMJTokWh(PCI) /dict_valeursGlobales["eco_E_carb"]
    # dict_valeursGlobales["eco_V_carb"] = conversionCarburantKgToLitres(eco_carburant_masse)
    # dict_valeursGlobales["eco_C"] = (
    #    dict_valeursGlobales["eco_V_carb"] * 100 /valeursGlobales.distance_totale
    # )

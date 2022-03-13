from math import pi, sin, cos

from valeursGlobales import dict_valeursGlobales
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
from dataCycleDeRoulage import t, v_veh, pente, rapport, q_carb_mgcp, nbEtapes, delta_t
from fonctions import *

"""
C'est dans ce module que se font tous les calculs.
"""


def calculRegimeMoteur():
    """1. Calcul du régime moteur"""
    for rap, V1000 in dict_V1000.items():
        dict_valeursGlobales["r_moteur_roue"][rap] = (
            (2 * pi * 60 * R_roue) / V1000 if V1000 != 0 else 0
        )

    # [tr/min] Régime de rotation du moteur
    N_mot = [
        max(1000 * v_veh[i] / dict_V1000[rapport[i]], N_ralenti)
        if rapport[i] != 0
        else N_ralenti
        for i in range(nbEtapes)
    ]
    plot(N_mot, "N_mot [tr/min]")

    return N_mot


def calculEffortsResistifs():
    """2. Calcul des efforts résistifs"""
    # [radian] Angle de la pente
    theta = [conversionDegreToRadian(pente[i]) for i in range(nbEtapes)]

    # [N] Effort résistif au roulement
    F_rr = [
        M_veh * g * cos(theta[i]) * Crr * 0.001 if v_veh[i] != 0 else 0
        for i in range(nbEtapes)
    ]
    plot(F_rr, "F_rr [N]")

    # [N] Effort résistif mécanique
    F_meca = [F_meca_cte if v_veh[i] != 0 else 0 for i in range(nbEtapes)]
    plot(F_meca, "F_meca [N]")

    # [N] Effort résistif de pente
    F_pente = [M_veh * g * sin(theta[i]) for i in range(nbEtapes)]
    plot(F_pente, "F_pente [N]")

    # [N] Effort résistif aérodynamique
    F_aero = [
        0.5 * rho_air * conversionKmhToMs(v_veh[i]) ** 2 * SCx for i in range(nbEtapes)
    ]
    plot(F_aero, "F_aero [N]")

    # [N] Effort résistif total
    F_resistif = [F_pente[i] + F_aero[i] + F_rr[i] + F_meca[i] for i in range(nbEtapes)]
    plot(F_resistif, "F_resistif [N]")

    return F_resistif


def calculMasses():
    """3. Calcul des masses"""
    # [kg] Masse équivalente en rotation
    M_eq = [
        I
        * rend_trans
        * (dict_valeursGlobales["r_moteur_roue"][rapport[i]] / R_roue) ** 2
        for i in range(nbEtapes)
    ]
    plot(M_eq, "M_eq [kg]")

    # [kg] Masse totale à entraîner
    M = [M_veh + M_eq[i] for i in range(nbEtapes)]
    plot(M, "M [kg]")

    return M


def calculEffortTotal(M):
    """4. Calcul de l'effort total"""
    # [m.s-2] Accélération du véhicule
    a = [
        (conversionKmhToMs(v_veh[i]) - conversionKmhToMs(v_veh[i - 1]))
        / (t[i] - t[i - 1])
        if i != 0
        else 0
        for i in range(nbEtapes)
    ]
    plot(a, "a [m.s-2]")

    # [N] Effort total
    F_tot = [M[i] * a[i] for i in range(nbEtapes)]
    plot(F_tot, "F_tot [N]")

    return F_tot


def calculCoupleEffectifMoteur(F_tot, F_resistif, N_mot):
    """5. Calcul du couple effectif moteur"""
    # [N] Besoin en effort de traction
    F_traction = [F_tot[i] + F_resistif[i] for i in range(nbEtapes)]
    plot(F_traction, "F_traction [N]")

    # [N.m] Couple nécessaire à la roue
    C_roue = [F_traction[i] * R_roue for i in range(nbEtapes)]
    plot(C_roue, "C_roue [N.m]")

    # [N.m] Couple effectif moteur nécessaire
    Ce_mot = [
        C_roue[i] / (dict_valeursGlobales["r_moteur_roue"][rapport[i]] * rend_trans)
        if rapport[i] != 0
        else 0
        for i in range(nbEtapes)
    ]
    plot(Ce_mot, "Ce_mot [N.m]")

    # [rad/s] Vitesse de rotation du moteur
    omega_mot = [
        conversionTourParMinuteToRadParSeconde(N_mot[i]) for i in range(nbEtapes)
    ]

    # [kW] Puissance effective moteur
    Pe_mot = [abs(Ce_mot[i]) * omega_mot[i] / 1000 for i in range(nbEtapes)]
    plot(Pe_mot, "Pe_mot [kW]")

    # [kW] Puissance de traction
    P_traction = [
        F_traction[i] * conversionKmhToMs(v_veh[i]) / 1000 for i in range(nbEtapes)
    ]
    plot(P_traction, "P_traction [kW]")

    return Pe_mot, P_traction, Ce_mot


def calculRendementEffectifConsoEtCO2(N_mot, Pe_mot):
    """6. Calcul du rendement effectif, de la consommation et du CO2"""
    # [mg/s] Débit de carburant
    q_carb = [
        q_carb_mgcp[i] * n_cyl * conversionTrParMinToTrParSec(N_mot[i]) / 2
        for i in range(nbEtapes)
    ]
    plot(q_carb, "q_carb [mg/s]")

    # [kW] Puissance chimique introduite
    P_carb = [q_carb[i] * PCI / 1000 for i in range(nbEtapes)]
    plot(P_carb, "P_carb [kW]")

    # [-] Rendement effectif du moteur
    dict_valeursGlobales["rend_e"] = sum(Pe_mot) / sum(P_carb)

    # [kg] Masse totale de carburant consommée sur tout le trajet
    masse_carburant_totale = (
        sum(q_carb[i] * delta_t for i in range(nbEtapes)) / 1_000_000
    )

    # [L] Consommation totale de carburant
    conso_carburant_totale = conversionCarburantKgToLitres(masse_carburant_totale)

    # [km] Distance totale parcourue pendant le trajet
    distance_totale = sum(
        conversionKmhToKms(v_veh[i]) * delta_t for i in range(nbEtapes)
    )

    # On convertit en litres aux 100 km
    # [L/100km] Consommation en carburant sur ce cycle
    dict_valeursGlobales["C"] = conso_carburant_totale * 100 / distance_totale

    # [kW.h] Energie introduite sous forme de carburant
    dict_valeursGlobales["E_carb"] = conversionMJTokWh(PCI) * masse_carburant_totale

    # Calcul des masses molaires utiles
    M_CHY = M_C + M_H * Y
    M_CO2 = M_C + 2 * M_O

    # [g] Masse de carburant par km
    masse_carburant_au_km = masse_carburant_totale / distance_totale * 1000

    # [g/km] Emission de CO2 du véhicule sur ce cycle
    dict_valeursGlobales["CO2"] = masse_carburant_au_km * M_CO2 / M_CHY

    return distance_totale


def evaluationAdaptationSurCycle(N_mot, Ce_mot):
    """7. Evaluation de l'adaptation moteur / véhicule / boite sur ce cycle"""
    plt.figure("courbePleineCharge")
    plt.xlabel("Régime moteur [tr/min]")
    plt.ylabel("Couple [N.m]")
    plt.plot(
        dict_pleine_charge.keys(),
        dict_pleine_charge.values(),
        label="Courbe de pleine charge",
        marker=".",
        linestyle="None",
    )

    # On place les points de fonctionnement moteur utilisés
    plt.plot(
        N_mot, Ce_mot, label="Points de fonctionnement", marker=".", linestyle="None"
    )

    plt.legend()
    # Save fig in png
    filename = os.path.join("media", "courbePleineCharge" + ".png")
    plt.savefig(filename, transparent=False)


def evaluationPotentielDeceleration(P_traction, distance_totale):
    """8. Evaluation du potentiel de récupération d'énergie à la décélération"""

    # [kW] Puissance  de  traction lorsque l’effort de traction est positif
    P_traction_ap = [max(P_traction[i], 0) for i in range(nbEtapes)]
    plot(P_traction_ap, "P_traction_ap [kW]")

    # [kW] Puissance  de  traction lorsque l’effort de traction est négatif
    P_traction_an = [min(P_traction[i], 0) for i in range(nbEtapes)]
    plot(P_traction_an, "P_traction_an [kW]")

    # [kW.h] Energie de traction lorsque le conducteur demande un couple positif
    dict_valeursGlobales["E_traction_ap"] = sum(
        P_traction_ap[i] * conversionSecondeToHeure(delta_t) for i in range(nbEtapes)
    )

    # [kW.h] Energie de traction lorsque le conducteur demande un couple négatif
    dict_valeursGlobales["E_traction_an"] = sum(
        P_traction_an[i] * conversionSecondeToHeure(delta_t) for i in range(nbEtapes)
    )

    # [kW.h] Energie disponible à la roue si l’intégralité de E_traction_an est récupérée
    dict_valeursGlobales["E_traction_elec"] = (
        0.8 * dict_valeursGlobales["E_traction_an"]
    )
    # [kW.h] Energie de traction restant à fournir par le moteur thermique
    dict_valeursGlobales["E_traction_therm"] = (
        dict_valeursGlobales["E_traction_ap"] - dict_valeursGlobales["E_traction_elec"]
    )
    # [-] Rendement de traction thermique
    dict_valeursGlobales["rend_traction_therm"] = (
        dict_valeursGlobales["E_traction_therm"] / dict_valeursGlobales["E_carb"]
    )
    # [kW.h] Energie à introduire sous forme de carburant
    dict_valeursGlobales["E_carb_hyb"] = (
        dict_valeursGlobales["E_traction_therm"]
        / dict_valeursGlobales["rend_traction_therm"]
    )

    # [kW.h] Economie en énergie introduite sous forme de carburant
    dict_valeursGlobales["eco_E_carb"] = (
        dict_valeursGlobales["E_carb"] - dict_valeursGlobales["E_carb_hyb"]
    )
    # FIXME
    if dict_valeursGlobales["eco_E_carb"] != 0:
        # [kg] Réduction de consommation de carburant
        eco_carburant_masse = (
            conversionMJTokWh(PCI) / dict_valeursGlobales["eco_E_carb"]
        )
        # [L] Réduction de consommation de carburant
        dict_valeursGlobales["eco_V_carb"] = conversionCarburantKgToLitres(
            eco_carburant_masse
        )
        # [L/100km] Réduction de consommation
        dict_valeursGlobales["eco_C"] = (
            dict_valeursGlobales["eco_V_carb"] * 100 / distance_totale
        )

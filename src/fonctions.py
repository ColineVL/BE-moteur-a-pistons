from math import pi
import matplotlib.pyplot as plt
import os

from data import rho_carb


def conversionDegreToRadian(angleDegre):
    """Convertit un angle de degré en radian"""
    return angleDegre * pi / 180


def conversionKmhToMs(kmh):
    """Convertit une vitesse en km/h en m/s"""
    return kmh / 3.6


def conversionKmhToKms(kmh):
    """Convertit une vitesse en km/h en km/s"""
    return kmh / 3600


def conversionTourParMinuteToRadParSeconde(tourParMinute):
    """Convertit une vitesse de rotation de tours/minute en rad/s"""
    return tourParMinute * (2 * pi / 60)


def conversionCarburantKgToLitres(kg):
    """Convertit une masse de carburant en kg à des litres"""
    # Conversion en m3
    m3 = kg / rho_carb
    # Conversion en litres
    litres = m3 * 1000
    return litres


def conversionMJTokWh(MJ):
    """Convertit énergie de MJ à kWh"""
    return MJ / (3.6 * 10**12)


def conversionSecondeToHeure(seconde):
    return seconde / 3600


def plot(data, titre):
    plt.figure(titre)
    plt.plot(data, label=titre)
    plt.legend()
    # Save fig in png
    filename = os.path.join("media", titre + ".png")
    plt.savefig(filename, transparent=False)

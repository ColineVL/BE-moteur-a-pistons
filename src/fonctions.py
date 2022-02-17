from math import pi
import matplotlib.pyplot as plt
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


plt.show()


def plot(data, titre, number):
    fig = plt.figure(number)
    plt.plot(data, label=titre)
    plt.legend()

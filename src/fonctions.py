from math import pi
import matplotlib.pyplot as plt


def conversionDegreToRadian(angleDegre):
    """Convertit un angle de degré en radian"""
    return angleDegre * pi / 180


def conversionKmhToMs(vitesse):
    """Convertit une vitesse en km/h en m/s"""
    return vitesse / 3.6


def conversionTourParMinuteToRadParSeconde(vitesse_rot):
    return vitesse_rot / (2 * pi / 60)


plt.show()


def plot(data, titre, number):
    fig = plt.figure(number)
    fig.plot(data, label=titre)

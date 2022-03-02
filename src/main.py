from calculs import *
import valeursGlobales


def main():
    calculRegimeMoteur()
    calculEffortsResistifs()
    calculMasses()
    calculEffortTotal()
    calculCoupleEffectifMoteur()
    calculRendementEffectifConsoEtCO2()
    evaluationAdaptationSurCycle()
    evaluationPotentielDeceleration()
    valeursGlobales.printAll()


if __name__ == "__main__":
    main()

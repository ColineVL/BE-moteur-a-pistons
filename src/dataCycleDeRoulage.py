# t [s] : temps
# v_veh [km/h] : vitesse du véhicule
# pente [°] : pente de la route, en degrés
# rapport [-] : rapport de boite engagé
# q_carb [mg/cp] : débit de carburant (mg/cp : milligrammes par coup, masse de carburant injectée par cylindre pour 1 cycle thermodynamique)

t = []
v_veh = []
pente = []
rapport = []
q_carb = []

assert len(t) == len(v_veh) == len(pente) == len(rapport) == len(q_carb)
nbEtapes = len(q_carb)
print(f"Chargé {nbEtapes} lignes du fichier")

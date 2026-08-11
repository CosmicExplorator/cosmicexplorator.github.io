---
title: Liste des équipements
url: /equipements/
description: Équipements utilisés pour les sessions d’astronomie.
weight: 30
---

| Catégorie | Matériel | Pilote INDI | Connexion | Rôle |
|---|---|---|---|---|
| Monture | Sky-Watcher EQ6-R Pro | `indi_eqmod_telescope` | USB / série | Pointage et suivi |
| Caméra principale | ZWO ASI | `indi_asi_ccd` | USB | Acquisition astronomique |
| Appareil photo | Canon EOS 1200D | `indi_canon_ccd` | USB | Imagerie grand champ |
| Mise au point | Focuser Celestron SCT | `indi_celestron_sct_focus` | USB | Mise au point motorisée |
| Localisation | GPS U-Blox | `indi_gpsd` | USB / USB-IP | Position et synchronisation |
| Pilotage | Joystick | `indi_joystick` | USB-IP | Commande manuelle |
| Serveur | Serveur Ubuntu 26.04 | `INDI Server` | Réseau | Centralisation des équipements |
| Station cliente | KStars / Ekos | `Client INDI` | Réseau | Pilotage des sessions |

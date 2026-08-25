---
title: "Huawei E3372 LTE"
description: "Fiche CMDB du modem LTE raccordé à Home Assistant."
weight: 40
---

## Équipement

| Attribut | Valeur |
|---|---|
| Constructeur / modèle | Huawei E3372 |
| Mode | HiLink |
| Adresse | `192.168.8.1` |
| Interface | `http://192.168.8.1/` |
| Firmware | Exemple : `22.xxx.xx.xx.xxx` — interface HiLink → Informations appareil |
| IMEI / carte SIM | Format : IMEI à 15 chiffres et ICCID à 19–20 chiffres ; stocker hors dépôt public |
| Usage | Secours LTE, télémétrie et SMS |

## Intégration

| Attribut | Valeur |
|---|---|
| Intégration | Huawei LTE |
| Transport | API HiLink locale |
| Flux requis | HAOS vers `192.168.8.1` |

## Entités

| Entité | Fonction |
|---|---|
| `binary_sensor.local_e3372_connexion_mobile` | Liaison mobile |
| `switch.local_e3372_donnees_mobiles` | Données mobiles |
| `select.local_e3372_mode_reseau_prefere` | Mode réseau |
| `sensor.local_e3372_nom_de_l_operateur` | Opérateur |
| `sensor.local_e3372_mode` | Technologie radio |
| `sensor.local_e3372_rssi` | RSSI |
| `sensor.local_e3372_rsrp` | RSRP |
| `sensor.local_e3372_rsrq` | RSRQ |
| `sensor.local_e3372_sinr` | SINR |
| `sensor.local_e3372_id_de_cellule` | Cellule LTE |
| `sensor.local_e3372_sms_non_lus` | SMS non lus |

## Reconnexion

| Attribut | Valeur |
|---|---|
| Automation | `huawei_e3372_reconnexion_automatique` |
| Fichier | `automations/network/huawei_e3372.yaml` |
| Déclenchement | Coupure 2 minutes ou contrôle toutes les 5 minutes |
| Action | Données à `off`, délai 3 secondes, puis `on` |
| Mode | `single` |

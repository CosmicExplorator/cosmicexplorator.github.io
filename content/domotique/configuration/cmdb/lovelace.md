---
title: "Interface Lovelace"
description: "Fiche CMDB du dashboard Supervision HAOS et de la carte SMS."
weight: 60
---

## Dashboard Supervision HAOS

| Attribut | Valeur |
|---|---|
| Identifiant | `supervision-haos` |
| Mode | YAML |
| Fichier | `/config/dashboards/supervision_haos.yaml` |
| Icône | `mdi:server` |
| Barre latérale | Activée |
| Accès | Administrateurs uniquement |

## Vues

| Vue | Contenu |
|---|---|
| Vue d'ensemble | Versions, sauvegardes, modem, réseau |
| Performances | CPU, mémoire, stockage |
| Réseau Huawei LTE | Radio, trafic, consommation |
| SMS | Lecture, envoi, suppression |
| Sauvegardes | État, calendrier, historique |

## Carte Huawei SMS

| Attribut | Valeur |
|---|---|
| Type | `custom:huawei-sms-card` |
| Fichier | `/config/www/huawei-sms-card.js` |
| Ressource | `/local/huawei-sms-card.js?v=4` |
| Type de ressource | `module` |
| Entité | `sensor.sms_huawei_e3372` |
| Actions | Lecture, envoi, suppression unitaire et globale |
| Protection DOM | Valeurs échappées avant insertion |
| Suppression globale | Confirmation utilisateur |

Incrémenter `?v=N` après chaque déploiement JavaScript.

## Style

`card-mod` personnalise les cartes de supervision.

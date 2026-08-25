---
title: "Instance Home Assistant OS"
description: "Fiche CMDB de l'instance HAOS."
weight: 10
---

## Identification

| Attribut | Valeur |
|---|---|
| Plateforme | Home Assistant OS |
| Nom d'instance | Exemple : `ha-maison` — Paramètres → Système → Réseau |
| Version Home Assistant | Exemple : `2026.8.2` — Paramètres → À propos |
| Version HAOS | Exemple : `16.1` — Paramètres → À propos |
| Version Supervisor | Exemple : `2026.08.1` — Paramètres → À propos |
| Matériel hôte | Exemple : `Raspberry Pi 5, 8 Go` — Paramètres → Système → Matériel |
| Adresse MAC | Exemple fictif : `02:00:00:12:34:56` — interface du routeur ; ne pas publier l'adresse réelle |

## Réseau

| Attribut | Valeur |
|---|---|
| Adresse IPv4 | Exemple privé : `192.0.2.10/24` — Paramètres → Système → Réseau |
| Passerelle | Exemple privé : `192.0.2.1` |
| Serveurs DNS | Exemple : `192.0.2.1`, `1.1.1.1` |
| URL interne | Exemple : `http://homeassistant.local:8123` |
| URL externe | Exemple réservé : `https://ha.example.com` |
| VLAN / sous-réseau | Exemple : `VLAN 20 — 192.0.2.0/24` |

## Stockage et sauvegardes

| Attribut | Valeur |
|---|---|
| Stockage système | Exemple : `SSD SATA` |
| Capacité | Exemple : `256 Go, 18 % utilisés` |
| Cible des sauvegardes | Exemple : `NAS via partage NFS` ; ne pas publier l'identifiant d'accès |
| Fréquence | Exemple : `quotidienne à 03:00` |
| Rétention | Exemple : `7 quotidiennes, 4 hebdomadaires, 12 mensuelles` |
| Chiffrement | Exemple : `activé, clé stockée hors de HAOS` ; ne pas publier la clé |
| Test de restauration | Exemple : `2026-08-01 — restauration validée sur instance isolée` |

## Composants spécifiques

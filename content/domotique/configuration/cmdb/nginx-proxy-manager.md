---
title: "Nginx Proxy Manager"
description: "Fiche CMDB du reverse proxy Home Assistant."
weight: 20
---

## Identification

| Attribut | Valeur |
|---|---|
| Produit | Nginx Proxy Manager |
| Déploiement | Add-on Home Assistant |
| Version | Exemple : `2.12.6` — visible dans l'interface de l'add-on |
| Administration | `http://<IP_HAOS>:81` |
| Rôle | Reverse proxy et terminaison TLS |

## Proxy Host Home Assistant

| Attribut | Valeur |
|---|---|
| FQDN public | Exemple réservé : `ha.example.com` |
| Schéma amont | Exemple : `http` |
| Hôte amont | Exemple privé : `192.0.2.10` |
| Port amont | Exemple Home Assistant : `8123/TCP` |
| WebSocket | Exemple : `activé` |
| Blocage des exploits courants | Exemple : `activé` |
| Redirection HTTP vers HTTPS | Exemple : `Force SSL activé` |
| Certificat affecté | Let's Encrypt, nom à relever |

## Flux

| Source | Destination | Port | Usage |
|---|---|---:|---|
| Internet | Nginx Proxy Manager | `443/TCP` | Accès HTTPS |
| Internet | Nginx Proxy Manager | `80/TCP` | Redirection HTTP |
| Réseau d'administration | HAOS | `81/TCP` | Administration NPM |
| Nginx Proxy Manager | Home Assistant | Exemple : `8123/TCP` | Proxy applicatif |

## Contrôles

| Contrôle | Valeur |
|---|---|
| Port 81 limité au LAN/VPN | Exemple attendu : `oui, filtré par pare-feu` |
| Compte administrateur nominatif | Exemple attendu : `oui, compte distinct par administrateur` |
| MFA | Exemple : `non disponible` ou `protégé par un SSO avec MFA` |
| Sauvegarde NPM | Exemple : `incluse dans la sauvegarde HAOS quotidienne` |
| Journaux d'accès | Exemple : `conservés 30 jours` |

## Procédure

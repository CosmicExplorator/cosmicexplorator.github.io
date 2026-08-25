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
| Version | À relever |
| Administration | `http://<IP_HAOS>:81` |
| Rôle | Reverse proxy et terminaison TLS |

## Proxy Host Home Assistant

| Attribut | Valeur |
|---|---|
| FQDN public | À relever |
| Schéma amont | À relever |
| Hôte amont | À relever |
| Port amont | À relever |
| WebSocket | À relever |
| Blocage des exploits courants | À relever |
| Redirection HTTP vers HTTPS | À relever |
| Certificat affecté | Let's Encrypt, nom à relever |

## Flux

| Source | Destination | Port | Usage |
|---|---|---:|---|
| Internet | Nginx Proxy Manager | `443/TCP` | Accès HTTPS |
| Internet | Nginx Proxy Manager | `80/TCP` | Redirection HTTP |
| Réseau d'administration | HAOS | `81/TCP` | Administration NPM |
| Nginx Proxy Manager | Home Assistant | À relever | Proxy applicatif |

## Contrôles

| Contrôle | Valeur |
|---|---|
| Port 81 limité au LAN/VPN | À vérifier |
| Compte administrateur nominatif | À vérifier |
| MFA | À relever |
| Sauvegarde NPM | À relever |
| Journaux d'accès | À relever |

## Procédure

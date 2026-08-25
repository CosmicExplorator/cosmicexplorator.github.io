---
title: "Let's Encrypt et DNS OVH"
description: "Fiche CMDB du certificat Home Assistant et de sa validation DNS."
weight: 30
---

## Certificat

| Attribut | Valeur |
|---|---|
| Autorité | Let's Encrypt |
| Gestionnaire ACME | Nginx Proxy Manager |
| Validation | DNS-01 |
| Fournisseur DNS | OVH |
| FQDN couvert | À relever |
| SAN supplémentaires | À relever |
| Expiration | Dynamique ; à superviser |
| Renouvellement | Automatique via Nginx Proxy Manager |

## API OVH

| Attribut | Valeur |
|---|---|
| Endpoint | À relever |
| Application key | Présence à vérifier ; secret non documenté |
| Application secret | Présence à vérifier ; secret non documenté |
| Consumer key | Présence à vérifier ; secret non documenté |
| Droits | Limiter à la zone DNS concernée |
| Rotation | À planifier |

## Dépendances

| Dépendance | Exigence |
|---|---|
| Zone DNS OVH | Modification TXT autorisée par API |
| DNS public | Enregistrements du FQDN valides |
| Horloge HAOS | Synchronisée |
| Sortie Internet | API ACME et OVH accessibles |

## Supervision

| Contrôle | Seuil |
|---|---|
| Expiration | Alerte avant 30 jours |
| Échec de renouvellement | Alerte immédiate |
| Résolution du FQDN | Contrôle externe |

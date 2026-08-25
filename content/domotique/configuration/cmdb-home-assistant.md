---
title: "CMDB Home Assistant"
description: "Inventaire technique de l'instance HAOS, de ses services et de ses composants spécifiques."
weight: 5
---

## Instance

| Attribut | Valeur |
|---|---|
| Plateforme | Home Assistant OS (HAOS) |
| Nom d'instance | À relever |
| Version Home Assistant | À relever |
| Version HAOS | À relever |
| Version Supervisor | À relever |
| Matériel hôte | À relever |
| Adresse IP HAOS | À relever |
| URL interne | À relever |
| URL externe | Domaine `blog.cosmic.ovh` documenté pour le site uniquement ; URL HA non documentée |
| Sauvegardes | Supervisées dans le dashboard ; cible, fréquence et rétention à relever |

## Exposition HTTPS

| Élément | Configuration |
|---|---|
| Reverse proxy | Add-on Nginx Proxy Manager |
| Interface d'administration | `http://<IP>:81` |
| Certificat | Let's Encrypt |
| Validation ACME | Challenge DNS |
| Fournisseur DNS | OVH |
| Proxy Host | Présent ; FQDN, destination et ports à relever |
| Renouvellement | Géré par Nginx Proxy Manager |

## Accès LTE de secours

| Attribut | Valeur |
|---|---|
| Équipement | Huawei E3372 |
| Mode | HiLink |
| Interface locale | `http://192.168.8.1/` |
| Intégration | Huawei LTE |
| Usage | Connexion LTE de secours, télémétrie radio et SMS |
| Dépendance réseau | Routage et filtrage autorisant HAOS vers `192.168.8.1` |
| Carte SIM / opérateur | À relever |

### Entités principales

| Entité | Rôle |
|---|---|
| `binary_sensor.local_e3372_connexion_mobile` | État de la liaison mobile |
| `switch.local_e3372_donnees_mobiles` | Activation des données mobiles |
| `select.local_e3372_mode_reseau_prefere` | Mode réseau préféré |
| `sensor.local_e3372_nom_de_l_operateur` | Opérateur courant |
| `sensor.local_e3372_mode` | Technologie radio |
| `sensor.local_e3372_rssi` | Puissance reçue globale |
| `sensor.local_e3372_rsrp` | Puissance du signal LTE de référence |
| `sensor.local_e3372_rsrq` | Qualité du signal LTE |
| `sensor.local_e3372_sinr` | Rapport signal/bruit et interférences |
| `sensor.local_e3372_id_de_cellule` | Cellule LTE |
| `sensor.local_e3372_sms_non_lus` | Compteur de SMS non lus |
| `sensor.sms_huawei_e3372` | Boîte de réception SMS normalisée |

### Reconnexion automatique

| Attribut | Valeur |
|---|---|
| Automation | `huawei_e3372_reconnexion_automatique` |
| Fichier | `automations/network/huawei_e3372.yaml` |
| Inclusion YAML | `automation network: !include_dir_merge_list automations/network/` |
| Déclenchement sur panne | Liaison à `off` pendant 2 minutes |
| Contrôle périodique | Toutes les 5 minutes |
| Condition | Liaison coupée et données mobiles activées |
| Remédiation | `switch.turn_off`, attente 3 secondes, `switch.turn_on` |
| Mode | `single` |

## Composant local SMS

| Attribut | Valeur |
|---|---|
| Domaine | `huawei_sms` |
| Type | Custom component, `local_polling` |
| Version déclarée | `1.0.0` |
| Répertoire | `/config/custom_components/huawei_sms/` |
| Bibliothèque | `huawei-lte-api` |
| Période d'interrogation | 60 secondes |
| Limite configurée | 20 messages ; plage admise de 1 à 50 |
| Conservation sur erreur | Dernière boîte connue conservée ; état indisponible |
| Données exposées | Attribut `messages` de `sensor.sms_huawei_e3372` |

### Services

| Service | Paramètres | Effet |
|---|---|---|
| `huawei_sms.send` | `phone_number`, `message` | Envoi d'un SMS |
| `huawei_sms.delete` | `message_id` | Suppression par index modem |
| `huawei_sms.delete_all` | Aucun | Suppression complète et irréversible |

### Protection des données

```yaml
recorder:
  exclude:
    entities:
      - sensor.sms_huawei_e3372
```

Objectif : ne pas historiser le contenu des SMS et leurs métadonnées dans la base Recorder.

## Interface Lovelace

| Attribut | Valeur |
|---|---|
| Dashboard | Supervision HAOS |
| Identifiant | `supervision-haos` |
| Mode | YAML |
| Fichier | `dashboards/supervision_haos.yaml` |
| Accès | Administrateurs uniquement (`require_admin: true`) |
| Vues | Vue d'ensemble, Performances, Réseau Huawei LTE, SMS, Sauvegardes |
| Carte SMS | `/config/www/huawei-sms-card.js` |
| Ressource | `/local/huawei-sms-card.js?v=4`, type `module` |
| Personnalisation | `card-mod` |

La ressource JavaScript utilise un numéro de version de requête comme cache-buster. Incrémenter `?v=N` après chaque déploiement du fichier.

## Arborescence spécifique

```text
/config/
├── automations/
│   └── network/
│       └── huawei_e3372.yaml
├── custom_components/
│   └── huawei_sms/
│       ├── __init__.py
│       ├── manifest.json
│       ├── sensor.py
│       └── services.yaml
├── dashboards/
│   └── supervision_haos.yaml
└── www/
    └── huawei-sms-card.js
```

## Dépendances et points de contrôle

| Contrôle | État documentaire |
|---|---|
| Accès HAOS vers `192.168.8.1` | Requis |
| Résolution DNS publique | À relever |
| Redirection NAT vers Nginx Proxy Manager | À relever |
| Politique de pare-feu | À relever |
| Secret API OVH | Emplacement et rotation à relever ; ne pas consigner la valeur |
| Expiration du certificat | À superviser |
| Santé du modem | Dashboard et automation présents |
| Contenu SMS dans Recorder | Exclu |
| Sauvegarde de `/config` | Méthode et restauration à documenter |
| Versions des custom components | À suivre manuellement |

## Documents associés

- [Configurer une clé Huawei E3372]({{< ref "/domotique/configuration/huawei-e3372" >}})
- [Ajouter une vue SMS Huawei]({{< ref "/domotique/howto/vue-sms-huawei" >}})
- [Créer le tableau de bord Supervision HAOS]({{< ref "/domotique/tableaux-de-bord/supervision-haos" >}})
- [Renouvellement du certificat Home Assistant]({{< ref "/informatique/renouveler-certificat-home-assistant" >}})

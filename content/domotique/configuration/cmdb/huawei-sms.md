---
title: "Composant Huawei SMS"
description: "Fiche CMDB du composant local de gestion des SMS et des contacts SIM."
weight: 50
---

## Composant

| Attribut | Valeur |
|---|---|
| Domaine | `huawei_sms` |
| Type | Custom component, `local_polling` |
| Version | `1.0.0` |
| Répertoire | `/config/custom_components/huawei_sms/` |
| Bibliothèque | `huawei-lte-api` |
| Interrogation | 60 secondes |
| Limite | 20 messages ; maximum 50 |

## Fichiers

```text
/config/custom_components/huawei_sms/
├── __init__.py
├── manifest.json
├── sensor.py
└── services.yaml
```

## Entité

| Attribut | Valeur |
|---|---|
| Entité | `sensor.sms_huawei_e3372` |
| Source | `http://192.168.8.1/` |
| Attributs | `messages`, `contacts` |
| Champs | `id`, `from`, `contact_name`, `date`, `content`, `unread` |
| Sur erreur | Dernières données conservées ; état indisponible |

## Contacts

| Attribut | Valeur |
|---|---|
| Source | Carnet d'adresses de l'API HiLink (`client.pb`) |
| Stockage visé | Carte SIM (`save_type: 1`) |
| Correspondance | Numéro normalisé au format international lorsque possible |
| Repli | Le numéro brut reste affiché si aucun contact ne correspond |
| Compatibilité | Dépend du firmware HiLink de la clé E3372 |

## Services

| Service | Paramètres | Effet |
|---|---|---|
| `huawei_sms.send` | `phone_number`, `message` | Envoi |
| `huawei_sms.delete` | `message_id` | Suppression unitaire |
| `huawei_sms.delete_all` | Aucun | Suppression complète irréversible |
| `huawei_sms.add_contact` | `name`, `phone_number` | Ajout d'un contact sur la SIM |
| `huawei_sms.delete_contact` | `contact_id` | Suppression d'un contact |

## Recorder

```yaml
recorder:
  exclude:
    entities:
      - sensor.sms_huawei_e3372
```

Le contenu et les métadonnées SMS ne doivent pas être historisés.

[Procédure de la vue SMS]({{< ref "/domotique/howto/vue-sms-huawei" >}})

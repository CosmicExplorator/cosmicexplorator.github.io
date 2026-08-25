---
title: "Composant Huawei SMS"
description: "Fiche CMDB du composant local de gestion des SMS."
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
| Attribut | `messages` |
| Champs | `id`, `from`, `date`, `content`, `unread` |
| Sur erreur | Dernières données conservées ; état indisponible |

## Services

| Service | Paramètres | Effet |
|---|---|---|
| `huawei_sms.send` | `phone_number`, `message` | Envoi |
| `huawei_sms.delete` | `message_id` | Suppression unitaire |
| `huawei_sms.delete_all` | Aucun | Suppression complète irréversible |

## Recorder

```yaml
recorder:
  exclude:
    entities:
      - sensor.sms_huawei_e3372
```

Le contenu et les métadonnées SMS ne doivent pas être historisés.

[Procédure de la vue SMS]({{< ref "/domotique/howto/vue-sms-huawei" >}})

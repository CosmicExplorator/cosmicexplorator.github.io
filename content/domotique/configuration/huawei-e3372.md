---
title: "Configurer une clé Huawei E3372 dans Home Assistant"
description: "Intégration LTE, reconnexion automatique, SMS et contacts enregistrés sur la SIM."
weight: 10
---

La clé **Huawei E3372 HiLink** fournit à Home Assistant une connexion LTE de secours ainsi que l’accès aux SMS reçus sur la carte SIM. Son interface locale est disponible à l’adresse `http://192.168.8.1/`.

## Prérequis

- une clé Huawei E3372 en mode HiLink, accessible depuis Home Assistant ;
- l’intégration **Huawei LTE** installée et configurée avec l’URL locale de la clé ;
- une carte SIM active ;
- un accès réseau autorisé entre Home Assistant et `192.168.8.1`.

Après l’ajout de l’intégration Huawei LTE, les entités utilisées dans cette installation sont notamment :

| Entité | Usage |
|---|---|
| `binary_sensor.local_e3372_connexion_mobile` | État de la connexion mobile |
| `switch.local_e3372_donnees_mobiles` | Activation des données mobiles |
| `select.local_e3372_mode_reseau_prefere` | Choix du mode réseau |
| `sensor.local_e3372_nom_de_l_operateur` | Opérateur courant |
| `sensor.local_e3372_rssi` | Puissance globale du signal |
| `sensor.local_e3372_rsrp` | Puissance du signal LTE de référence |
| `sensor.local_e3372_rsrq` | Qualité du signal LTE |
| `sensor.local_e3372_sinr` | Rapport signal sur interférences et bruit |
| `sensor.local_e3372_sms_non_lus` | Nombre de SMS non lus |

Les identifiants sont propres à l’installation. Il faut les remplacer dans les exemples si Home Assistant a créé des noms différents.

## Reconnexion automatique

Une automation contrôle la liaison toutes les cinq minutes et intervient aussi lorsqu’elle reste coupée pendant deux minutes. Si les données mobiles sont activées, le commutateur est arrêté pendant trois secondes puis réactivé.

```yaml
- id: huawei_e3372_reconnexion_automatique
  alias: Huawei E3372 - Reconnexion automatique
  description: Relance les données mobiles après 2 minutes de déconnexion.
  triggers:
    - trigger: state
      entity_id: binary_sensor.local_e3372_connexion_mobile
      to: "off"
      for: "00:02:00"
    - trigger: time_pattern
      minutes: "/5"
  conditions:
    - condition: state
      entity_id: binary_sensor.local_e3372_connexion_mobile
      state: "off"
    - condition: state
      entity_id: switch.local_e3372_donnees_mobiles
      state: "on"
  actions:
    - action: switch.turn_off
      target:
        entity_id: switch.local_e3372_donnees_mobiles
    - delay: "00:00:03"
    - action: switch.turn_on
      target:
        entity_id: switch.local_e3372_donnees_mobiles
  mode: single
```

L’automation est enregistrée dans `automations/network/huawei_e3372.yaml`, puis chargée avec un bloc dédié dans `configuration.yaml` :

```yaml
automation network: !include_dir_merge_list automations/network/
```

## Préparer l’accès aux SMS et aux contacts

La bibliothèque Python `huawei-lte-api` est utilisée par le composant local présenté dans le [HowTo consacré à la vue SMS]({{< ref "/domotique/howto/vue-sms-huawei" >}}). Le capteur interroge la boîte de réception et le carnet d'adresses toutes les minutes. Il expose le nom du contact avec chaque message lorsqu'une correspondance est trouvée.

```yaml
sensor:
  - platform: huawei_sms
    name: SMS Huawei E3372
    url: http://192.168.8.1/
    max_messages: 20
```

`max_messages` accepte une valeur de 1 à 50. Le capteur créé par cette configuration est `sensor.sms_huawei_e3372`.

## Vérifications

1. Ouvrir **Outils de développement → États** et vérifier que les entités `local_e3372` répondent.
2. Couper temporairement la connexion mobile et contrôler le déclenchement de l’automation.
3. Vérifier que `sensor.sms_huawei_e3372` est disponible et possède les attributs `messages` et `contacts`.
4. Ajouter un contact de test avec l'action `huawei_sms.add_contact`, puis vérifier que son nom remplace le numéro dans la vue SMS.

L’intégration et la carte SMS communiquent uniquement avec l’API locale de la clé. Si la clé est placée sur un autre sous-réseau, le routage et les règles de pare-feu doivent permettre l’accès à son adresse HiLink.

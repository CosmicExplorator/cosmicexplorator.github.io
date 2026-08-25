---
title: "Créer le tableau de bord Supervision HAOS"
description: "Un dashboard YAML dédié à la plateforme Home Assistant et au réseau Huawei LTE."
weight: 10
---

Le tableau de bord **Supervision HAOS** centralise l’état de Home Assistant, ses performances, ses sauvegardes et la connexion LTE Huawei. Il est déclaré en mode YAML afin que sa configuration reste versionnable.

## Déclarer le dashboard

Le fichier `dashboards/supervision_haos.yaml` est enregistré dans `configuration.yaml` :

```yaml
lovelace:
  dashboards:
    supervision-haos:
      mode: yaml
      title: Supervision HAOS
      icon: mdi:server
      show_in_sidebar: true
      require_admin: true
      filename: dashboards/supervision_haos.yaml
```

`require_admin: true` réserve cette vue aux administrateurs, ce qui est adapté à un écran de supervision technique.

## Organisation des vues

| Vue | Contenu |
|---|---|
| Vue d’ensemble | Versions, sauvegardes, état synthétique du modem et réseau local |
| Performances | CPU, mémoire et stockage HAOS |
| Réseau Huawei LTE | Radio, qualité du signal, trafic et consommation mensuelle |
| SMS | Lecture, envoi et suppression des messages |
| Sauvegardes | État, calendrier et historique des sauvegardes |

## Vue Réseau Huawei LTE

La vue utilise le type `sections` et sépare le signal mobile du trafic réseau :

```yaml
- title: Réseau Huawei LTE
  path: reseau-huawei-lte
  icon: mdi:signal-4g
  type: sections
  max_columns: 2
  sections:
    - type: grid
      cards:
        - type: heading
          heading: Signal mobile
          icon: mdi:signal
        - type: entities
          title: Radio LTE
          entities:
            - entity: binary_sensor.local_e3372_connexion_mobile
              name: Connexion mobile
            - entity: switch.local_e3372_donnees_mobiles
              name: Données mobiles
            - entity: select.local_e3372_mode_reseau_prefere
              name: Réseau préféré
            - entity: sensor.local_e3372_nom_de_l_operateur
              name: Opérateur
            - entity: sensor.local_e3372_mode
              name: Technologie
            - entity: sensor.local_e3372_rssi
              name: RSSI
            - entity: sensor.local_e3372_rsrp
              name: RSRP
            - entity: sensor.local_e3372_rsrq
              name: RSRQ
            - entity: sensor.local_e3372_sinr
              name: SINR
            - entity: sensor.local_e3372_id_de_cellule
              name: Cellule
```

La seconde colonne affiche les débits montant et descendant, les volumes de la session, sa durée, la consommation mensuelle et le nombre de SMS non lus.

## Lecture des indicateurs radio

- **RSSI** donne une indication globale de la puissance reçue ;
- **RSRP** mesure la puissance du signal LTE utile ;
- **RSRQ** représente sa qualité ;
- **SINR** compare le signal utile au bruit et aux interférences.

Ces quatre valeurs doivent être observées ensemble : un signal puissant peut rester peu exploitable si sa qualité ou son SINR sont mauvais.

## Style des cartes

Les cartes emploient `card-mod` pour conserver une identité visuelle homogène. Exemple pour le bloc LTE :

```yaml
card_mod:
  style: |
    ha-card {
      border: 2px solid #00aaff;
      border-radius: 14px;
      background: #1a1a1a !important;
      box-shadow: 0 0 12px #00aaff;
      color: #f2f2f2 !important;
    }
```

La [vue SMS Huawei]({{< ref "/domotique/howto/vue-sms-huawei" >}}) complète ce dashboard avec une carte Lovelace personnalisée.

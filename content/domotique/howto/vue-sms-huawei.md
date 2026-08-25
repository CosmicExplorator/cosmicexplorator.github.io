---
title: "Ajouter une vue SMS pour la clé Huawei E3372"
description: "Lire, envoyer et supprimer les SMS depuis un dashboard Home Assistant."
weight: 10
---

Cette vue ajoute à Home Assistant une boîte de réception complète pour la clé Huawei E3372 : affichage des messages du plus récent au plus ancien, envoi d’un SMS, suppression individuelle et vidage de la boîte de réception.

## Architecture

{{< mermaid >}}
flowchart LR
    M["Huawei E3372<br/>API HiLink"]
    C["Composant huawei_sms<br/>Python"]
    S["sensor.sms_huawei_e3372"]
    V["huawei-sms-card.js<br/>Vue Lovelace"]

    M <-->|"huawei-lte-api"| C
    C -->|"attribut messages"| S
    S -->|"lecture"| V
    V -->|"services send / delete / delete_all"| C
{{< /mermaid >}}

Le composant Python assure la communication locale avec le modem. Le capteur expose les messages et la carte JavaScript se charge uniquement de l’affichage et des actions utilisateur.

## Installer le composant local

Créer le répertoire suivant :

```text
custom_components/huawei_sms/
├── __init__.py
├── manifest.json
├── sensor.py
└── services.yaml
```

Le manifeste déclare une intégration locale avec interrogation périodique :

```json
{
  "domain": "huawei_sms",
  "name": "Huawei SMS Inbox",
  "codeowners": [],
  "documentation": "https://github.com/Salamek/huawei-lte-api",
  "iot_class": "local_polling",
  "version": "1.0.0"
}
```

Dans `sensor.py`, le capteur utilise `huawei-lte-api`, limite la lecture à 20 messages par défaut et interroge la clé toutes les minutes. Chaque SMS est normalisé sous cette forme :

```python
{
    "id": str(message.get("Index", "")),
    "from": str(message.get("Phone", "Numéro inconnu")),
    "date": str(message.get("Date", "")),
    "content": str(message.get("Content", "")),
    "unread": str(message.get("Smstat", "1")) == "0",
}
```

Le capteur expose ensuite la liste dans l’attribut `messages`. Il conserve la dernière boîte de réception connue en cas d’erreur transitoire, tout en passant son état à indisponible.

## Déclarer le capteur

Ajouter le bloc suivant dans `configuration.yaml`, puis redémarrer Home Assistant :

```yaml
sensor:
  - platform: huawei_sms
    name: SMS Huawei E3372
    url: http://192.168.8.1/
    max_messages: 20
```

Pour ne pas enregistrer le contenu privé des messages dans la base de données, exclure le capteur de Recorder :

```yaml
recorder:
  exclude:
    entities:
      - sensor.sms_huawei_e3372
```

Cette exclusion est importante : les attributs d’une entité sont normalement historisés avec son état.

## Services disponibles

Le composant enregistre trois services :

| Service | Paramètres | Fonction |
|---|---|---|
| `huawei_sms.send` | `phone_number`, `message` | Envoyer un SMS |
| `huawei_sms.delete` | `message_id` | Supprimer un message par son index modem |
| `huawei_sms.delete_all` | aucun | Supprimer définitivement toute la boîte de réception |

Exemple d’envoi depuis **Outils de développement → Actions** :

```yaml
action: huawei_sms.send
data:
  phone_number: "+33612345678"
  message: "Test envoyé depuis Home Assistant"
```

## Installer la carte Lovelace

Copier `huawei-sms-card.js` dans le répertoire `www/`, puis déclarer la ressource :

```yaml
lovelace:
  resources:
    - url: /local/huawei-sms-card.js?v=4
      type: module
```

Le paramètre `?v=4` sert de cache-buster. Il faut l’incrémenter après une modification importante du fichier JavaScript afin de forcer le navigateur à télécharger la nouvelle version.

La carte échappe le numéro, la date et le contenu avant insertion dans le DOM. Elle demande aussi une confirmation avant la suppression globale, qui est irréversible.

## Créer la vue SMS

Dans `dashboards/supervision_haos.yaml`, ajouter :

```yaml
- title: SMS
  path: sms
  icon: mdi:message-text
  type: sections
  max_columns: 1
  sections:
    - type: grid
      cards:
        - type: heading
          heading: Boîte de réception
          icon: mdi:message-text-outline
        - type: custom:huawei-sms-card
          entity: sensor.sms_huawei_e3372
```

La vue affiche le nombre de messages, distingue les messages non lus, propose un formulaire d’envoi et associe une action de suppression à chaque entrée.

## Dépannage

- **Entité indisponible** : vérifier l’accès à `http://192.168.8.1/` depuis Home Assistant et consulter les journaux contenant `huawei_sms`.
- **Carte inconnue** : contrôler le chemin `/config/www/huawei-sms-card.js`, la ressource Lovelace et le cache du navigateur.
- **Aucun attribut `messages`** : vérifier le redémarrage après l’installation du composant et la syntaxe du bloc `sensor`.
- **Échec de l’envoi ou de la suppression** : tester le service concerné depuis les outils de développement pour distinguer un problème d’API d’un problème d’interface.
- **Entités différentes** : adapter le nom du capteur dans la carte et dans l’exclusion Recorder.

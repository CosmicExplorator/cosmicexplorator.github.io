---
title: "Ajouter une vue SMS pour la clé Huawei E3372"
description: "Lire, envoyer et supprimer les SMS, puis gérer les contacts de la SIM depuis Home Assistant."
weight: 10
---

Cette vue ajoute à Home Assistant une boîte de réception complète pour la clé Huawei E3372 : affichage des messages du plus récent au plus ancien, résolution des numéros depuis les contacts de la SIM, envoi d’un SMS, suppression individuelle et vidage de la boîte de réception.

## Architecture

{{< mermaid >}}
flowchart LR
    M["Huawei E3372<br/>API HiLink"]
    C["Composant huawei_sms<br/>Python"]
    S["sensor.sms_huawei_e3372"]
    V["huawei-sms-card.js<br/>Vue Lovelace"]

    M <-->|"huawei-lte-api"| C
    C -->|"attributs messages et contacts"| S
    S -->|"lecture"| V
    V -->|"services SMS et contacts"| C
{{< /mermaid >}}

Le composant Python assure la communication locale avec le modem. Le capteur expose les messages et les contacts ; la carte JavaScript se charge uniquement de l’affichage et des actions utilisateur.

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

## Lire et normaliser les contacts

Le carnet d'adresses est lu avec `client.pb.get_pb_list(save_type=1)`. Sur les firmwares compatibles, `save_type=1` sélectionne la carte SIM. Comme la structure retournée varie selon les versions HiLink, normaliser la réponse avant de l'exposer :

```python
import re


def normalize_phone_number(value: str) -> str:
    value = value.strip()
    prefix = "+" if value.startswith("+") else ""
    return prefix + re.sub(r"\D", "", value)


def normalize_contacts(payload: dict) -> list[dict[str, str]]:
    phonebook = payload.get("PhoneBook", payload)
    entries = phonebook.get("PbList", {}).get("PbItem", [])
    if isinstance(entries, dict):
        entries = [entries]

    contacts = []
    for entry in entries:
        fields = entry.get("Field", [])
        if isinstance(fields, dict):
            fields = [fields]
        values = {
            str(field.get("Name", "")): str(field.get("Value", ""))
            for field in fields
        }
        number = values.get("MobilePhone", "")
        contacts.append(
            {
                "id": str(entry.get("Index", "")),
                "name": values.get("FormattedName", ""),
                "phone_number": number,
                "normalized_number": normalize_phone_number(number),
            }
        )
    return contacts
```

Après la lecture des SMS et des contacts, enrichir chaque message sans supprimer le numéro d'origine :

```python
contacts_by_number = {
    contact["normalized_number"]: contact["name"]
    for contact in contacts
    if contact["normalized_number"]
}

for message in messages:
    message["contact_name"] = contacts_by_number.get(
        normalize_phone_number(message["from"]),
        "",
    )
```

Le capteur doit exposer `contacts` en plus de `messages`. La carte affiche `contact_name` lorsqu'il est renseigné et conserve `from` comme information secondaire et comme valeur de réponse.

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

Le composant enregistre cinq services :

| Service | Paramètres | Fonction |
|---|---|---|
| `huawei_sms.send` | `phone_number`, `message` | Envoyer un SMS |
| `huawei_sms.delete` | `message_id` | Supprimer un message par son index modem |
| `huawei_sms.delete_all` | aucun | Supprimer définitivement toute la boîte de réception |
| `huawei_sms.add_contact` | `name`, `phone_number` | Ajouter un contact sur la carte SIM |
| `huawei_sms.delete_contact` | `contact_id` | Supprimer un contact du carnet |

Exemple d’envoi depuis **Outils de développement → Actions** :

```yaml
action: huawei_sms.send
data:
  phone_number: "+33612345678"
  message: "Test envoyé depuis Home Assistant"
```

Dans `async_setup`, enregistrer les deux actions consacrées aux contacts en réutilisant la même connexion et le même verrou que les actions SMS :

```python
import voluptuous as vol

from homeassistant.const import CONF_NAME
from homeassistant.helpers import config_validation as cv

CONF_PHONE_NUMBER = "phone_number"
CONF_CONTACT_ID = "contact_id"

ADD_CONTACT_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_PHONE_NUMBER): cv.string,
    }
)
DELETE_CONTACT_SCHEMA = vol.Schema(
    {vol.Required(CONF_CONTACT_ID): vol.Coerce(int)}
)


async def add_contact(call):
    await hass.async_add_executor_job(
        client.pb.pb_new,
        0,                         # group_id
        1,                         # save_type : SIM
        call.data[CONF_NAME],
        call.data[CONF_PHONE_NUMBER],
    )
    await coordinator.async_request_refresh()


async def delete_contact(call):
    await hass.async_add_executor_job(
        client.pb.pb_delete,
        call.data[CONF_CONTACT_ID],
    )
    await coordinator.async_request_refresh()


hass.services.async_register(
    DOMAIN, "add_contact", add_contact, schema=ADD_CONTACT_SCHEMA
)
hass.services.async_register(
    DOMAIN, "delete_contact", delete_contact, schema=DELETE_CONTACT_SCHEMA
)
```

Cet extrait suppose que le composant possède déjà `client`, `coordinator`, `DOMAIN` et un mécanisme de connexion partagé. Ne pas ouvrir une seconde session HiLink concurrente : certains firmwares E3372 invalident alors la première session.

Ajouter également les descriptions suivantes dans `services.yaml` :

```yaml
add_contact:
  name: Ajouter un contact SIM
  fields:
    name:
      name: Nom
      required: true
      selector:
        text:
    phone_number:
      name: Numéro de téléphone
      required: true
      selector:
        text:

delete_contact:
  name: Supprimer un contact
  fields:
    contact_id:
      name: Identifiant du contact
      required: true
      selector:
        number:
          min: 0
          mode: box
```

Exemple d'ajout depuis **Outils de développement → Actions** :

```yaml
action: huawei_sms.add_contact
data:
  name: "Jean Dupont"
  phone_number: "+33612345678"
```

Le nombre et la longueur des contacts dépendent de la carte SIM. Il est préférable d'utiliser des noms courts et des numéros au format international.

## Installer la carte Lovelace

Copier `huawei-sms-card.js` dans le répertoire `www/`, puis déclarer la ressource :

```yaml
lovelace:
  resources:
    - url: /local/huawei-sms-card.js?v=5
      type: module
```

Le paramètre `?v=5` sert de cache-buster. Il faut l’incrémenter après une modification importante du fichier JavaScript afin de forcer le navigateur à télécharger la nouvelle version.

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
- **Erreur sur `pb-list` ou `pb-new`** : le firmware HiLink ne prend probablement pas en charge le carnet d'adresses. Vérifier aussi que l'authentification administrateur est configurée si elle est exigée.
- **Contact ajouté dans le modem plutôt que sur la SIM** : le firmware n'interprète pas `save_type=1` comme attendu. Comparer les réponses de `get_pb_list(save_type=0)` et `get_pb_list(save_type=1)` avant de conserver l'action.
- **Nom non affiché** : comparer le numéro du SMS et celui du contact après normalisation ; les variantes nationales (`06…`) et internationales (`+336…`) ne sont pas équivalentes avec cette normalisation minimale.
- **Entités différentes** : adapter le nom du capteur dans la carte et dans l’exclusion Recorder.

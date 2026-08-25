---
title: "Moteur d'interaction SMS"
description: "Étape 1 : normaliser un SMS et valider son format sans l'interpréter."
weight: 10
---

## Périmètre

Cette première étape réalise uniquement :

1. la normalisation du texte ;
2. l'identification d'une commande ou d'une interrogation ;
3. l'extraction de la pièce et du contenu restant ;
4. le rejet des formats invalides.

Aucune entité Home Assistant n'est recherchée et aucune action n'est exécutée.

## Formats acceptés

Commande :

```text
<Pièce>, <action> <paramètres>
```

Interrogation :

```text
<Pièce>, <question> ?
```

Exemples valides :

```text
Salon, allume lumière
Bureau, règle chauffage à 19
Salon, température ?
Garage, état porte ?
```

## Validateur

```python
import re
import unicodedata
from dataclasses import dataclass
from enum import Enum


class SmsType(Enum):
    COMMAND = "command"
    QUERY = "query"
    INVALID = "invalid"


@dataclass
class ValidationResult:
    valid: bool
    sms_type: SmsType
    normalized_message: str
    piece: str | None = None
    payload: str | None = None
    error: str | None = None


COMMAND_RE = re.compile(
    r"^(?P<piece>[a-z0-9][a-z0-9 _-]*)"
    r"\s*,\s*"
    r"(?P<payload>[a-z0-9][a-z0-9 _.,°%+-]*)"
    r"[.!]?$"
)

QUERY_RE = re.compile(
    r"^(?P<piece>[a-z0-9][a-z0-9 _-]*)"
    r"\s*,\s*"
    r"(?P<payload>[a-z0-9][a-z0-9 _.,°%+-]*)"
    r"\s*\?$"
)


def normalize_sms(message: str) -> str:
    message = unicodedata.normalize("NFKD", message)
    message = "".join(
        character
        for character in message
        if not unicodedata.combining(character)
    )
    message = re.sub(r"\s+", " ", message)
    return message.strip().lower()


def validate_sms(message: str) -> ValidationResult:
    normalized = normalize_sms(message)

    if not normalized:
        return ValidationResult(
            valid=False,
            sms_type=SmsType.INVALID,
            normalized_message=normalized,
            error="empty_message",
        )

    match = QUERY_RE.fullmatch(normalized)
    if match:
        return ValidationResult(
            valid=True,
            sms_type=SmsType.QUERY,
            normalized_message=normalized,
            piece=match.group("piece").strip(),
            payload=match.group("payload").strip(),
        )

    match = COMMAND_RE.fullmatch(normalized)
    if match:
        return ValidationResult(
            valid=True,
            sms_type=SmsType.COMMAND,
            normalized_message=normalized,
            piece=match.group("piece").strip(),
            payload=match.group("payload").strip(),
        )

    return ValidationResult(
        valid=False,
        sms_type=SmsType.INVALID,
        normalized_message=normalized,
        error="invalid_format",
    )
```

## Résultats attendus

| SMS | Type | Pièce | Payload |
|---|---|---|---|
| `Salon, allume lumière` | `command` | `salon` | `allume lumiere` |
| `Salon, température ?` | `query` | `salon` | `temperature` |
| `allume lumière salon` | `invalid` | — | — |
| chaîne vide | `invalid` | — | — |

## Contrat de sortie

| Champ | Type | Description |
|---|---|---|
| `valid` | `bool` | Résultat de la validation |
| `sms_type` | `SmsType` | `command`, `query` ou `invalid` |
| `normalized_message` | `str` | Message sans accents, en minuscules et avec espaces normalisés |
| `piece` | `str \| None` | Pièce extraite |
| `payload` | `str \| None` | Contenu restant, non interprété |
| `error` | `str \| None` | `empty_message` ou `invalid_format` |

## Étape suivante

L'analyse du `payload` devra produire une intention structurée sans exécuter directement l'action :

```text
payload
  → verbe
  → équipement ou information
  → valeur optionnelle
  → intention validée
```

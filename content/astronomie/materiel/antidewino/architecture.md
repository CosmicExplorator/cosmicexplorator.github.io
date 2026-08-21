---
title: "Architecture d’AntiDewino"
description: "Architecture du contrôleur Arduino et de l’anneau chauffant de la lame correctrice."
aliases:
  - /astronomie/materiel/antidewino/conception/
weight: 10
---

## Principe de fonctionnement

AntiDewino mesure les conditions autour du télescope, estime le risque de rosée puis module l’anneau chauffant. La lame est ainsi maintenue légèrement au-dessus du point de rosée, sans chauffage excessif.

{{< mermaid >}}
flowchart LR
    S["Sondes de température<br/>et d’humidité"] --> A["Arduino Uno<br/>mesure et régulation"]
    A --> M["Étage de puissance<br/>MOSFET"]
    P["Alimentation protégée<br/>par fusible"] --> M
    M --> R["Anneau chauffant 12 V<br/>sur la lame correctrice"]
{{< /mermaid >}}

## Architecture

| Élément | Rôle |
|---|---|
| Arduino Uno | Acquisition des mesures, régulation et contrôles de sécurité |
| Sonde près de la lame | Mesure de la température de l’optique |
| Sonde ambiante | Mesure de la température et de l’humidité |
| Étage MOSFET | Modulation de la puissance de l’anneau chauffant |
| Fusible | Protection de l’alimentation et du câblage |
| Anneau chauffant 12 V | Chauffage de la lame correctrice du C8 EdgeHD |

## Comportement de sécurité

Le chauffage reste arrêté au démarrage jusqu’à la validation des mesures et des contrôles. Il s’arrête également si une sonde renvoie une valeur incohérente.

Le système garantit :

- un état **OFF** pendant le démarrage et après une erreur ;
- une puissance et une température maximales limitées ;
- un câblage dimensionné pour le courant mesuré ;
- un fusible placé au plus près de l’alimentation ;
- l’absence de charge chauffante sur une sortie de l’Arduino.

---
title: "Conception d’AntiDewino"
description: "Architecture envisagée et points à valider avant l’assemblage du contrôleur anti-rosée."
weight: 10
---

## Principe de fonctionnement

AntiDewino doit mesurer les conditions autour du télescope, estimer le risque de rosée puis moduler le ruban chauffant. La lame est ainsi maintenue légèrement au-dessus du point de rosée, sans chauffage excessif.

{{< mermaid >}}
flowchart LR
    S["Sondes de température<br/>et d’humidité"] --> A["Arduino Uno<br/>mesure et régulation"]
    A --> M["Étage de puissance<br/>MOSFET"]
    P["Alimentation protégée<br/>par fusible"] --> M
    M --> R["Ruban chauffant<br/>autour de la lame"]
{{< /mermaid >}}

## Architecture envisagée

| Élément | Rôle | État |
|---|---|---|
| Arduino Uno | Mesure, régulation et contrôles de sécurité | Carte détectée |
| Sonde près de la lame | Mesure de la température de l’optique | À choisir |
| Sonde ambiante | Mesure de la température et de l’humidité | À choisir |
| Étage MOSFET | Modulation de la puissance du ruban | À dimensionner |
| Fusible | Protection de l’alimentation et du câblage | À dimensionner |
| Ruban chauffant | Chauffage de la lame | Caractéristiques à mesurer |

## Informations à relever

Avant de finaliser le schéma et le firmware, il faut relever :

1. le diamètre et la circonférence de la lame ;
2. la tension d’alimentation disponible ;
3. la résistance et la puissance nominale du ruban chauffant ;
4. le courant maximal attendu ;
5. les références des sondes disponibles ;
6. le boîtier et la connectique souhaités.

## Comportement de sécurité

Le chauffage doit rester arrêté au démarrage, jusqu’à la validation des mesures et des contrôles. Il doit également s’arrêter si une sonde renvoie une valeur incohérente.

La conception finale devra garantir :

- un état **OFF** pendant le démarrage et après une erreur ;
- une puissance et une température maximales limitées ;
- un câblage dimensionné pour le courant mesuré ;
- un fusible placé au plus près de l’alimentation ;
- l’absence de charge chauffante sur une sortie de l’Arduino.

## Prochaines étapes

1. mesurer les caractéristiques du ruban chauffant ;
2. inventorier les sondes et composants disponibles ;
3. choisir et dimensionner l’étage de puissance ;
4. définir le brochage et produire le schéma électrique ;
5. implémenter le firmware avec le chauffage désactivé par défaut ;
6. valider progressivement le montage par des essais et des mesures.


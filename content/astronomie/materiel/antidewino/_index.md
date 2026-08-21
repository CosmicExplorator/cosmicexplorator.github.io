---
title: "AntiDewino"
description: "Contrôleur Arduino de chauffage anti-rosée pour la lame du télescope."
weight: 10
---

AntiDewino est un contrôleur autonome basé sur un Arduino Uno. Il pilote l’anneau chauffant 12 V installé sur la lame correctrice du C8 EdgeHD afin d’empêcher la formation de rosée.

## Objectif

Maintenir la lame quelques degrés au-dessus du point de rosée en utilisant uniquement la puissance nécessaire. Cette régulation limite la consommation et évite les turbulences thermiques devant l’instrument.

## Périmètre du projet

- l’Arduino Uno mesure les conditions et calcule la puissance nécessaire ;
- l’étage de puissance commande l’anneau chauffant alimenté en 12 V ;
- les protections matérielles et logicielles sécurisent le chauffage ;
- l’ensemble fonctionne indépendamment du serveur INDI.

> **Sécurité :** l’anneau chauffant n’est jamais alimenté directement par une sortie de l’Arduino. La commande passe par un étage de puissance adapté et l’alimentation est protégée par un fusible.

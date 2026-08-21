---
title: "AntiDewino"
description: "Contrôleur Arduino de chauffage anti-rosée pour la lame du télescope."
weight: 10
---

AntiDewino est un contrôleur de chauffage destiné à empêcher la formation de rosée sur la lame du télescope.

Le projet est actuellement en phase de conception. Le circuit de puissance, les capteurs et le brochage doivent encore être validés avant de commander le chauffage.

## Objectif

Maintenir la lame quelques degrés au-dessus du point de rosée en utilisant uniquement la puissance nécessaire. Cette régulation doit limiter la consommation et éviter les turbulences thermiques devant l’instrument.

## Périmètre du projet

- le firmware de l’Arduino Uno ;
- le schéma électrique, le câblage et la nomenclature ;
- les essais et les mesures ;
- les protections matérielles et logicielles.

> **Sécurité :** le ruban chauffant ne doit jamais être alimenté directement par une sortie de l’Arduino. Le montage final devra intégrer un étage de puissance adapté, un fusible et des limites de température.


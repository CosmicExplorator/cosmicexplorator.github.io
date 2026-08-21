---
title: "AntiDewino"
description: "Contrôleur Arduino de l’anneau chauffant de la lame correctrice du C8 EdgeHD."
weight: 10
---

AntiDewino commande l’anneau chauffant 12 V installé sur la lame correctrice du C8 EdgeHD. Un ordinateur transmet le niveau de chauffe à un Arduino Uno par USB avec le protocole Firmata. L’Arduino génère ensuite le signal PWM destiné au module de puissance D4184.

## Chaîne de commande

1. l’ordinateur envoie une consigne comprise entre 0 et 255 ;
2. l’Arduino Uno reçoit cette consigne via Firmata à 57 600 bauds ;
3. la sortie D9 commande l’entrée PWM du module MOSFET D4184 ;
4. le D4184 module l’alimentation 12 V de l’anneau chauffant ;
5. une LED RGB indique le niveau de chauffe demandé.

La logique de commande et le circuit de puissance sont séparés. L’Arduino ne fournit jamais le courant consommé par l’anneau.

## Documentation

- [Architecture d’AntiDewino]({{< ref "architecture" >}}) : flux de commande, câblage, niveaux et sécurité ;
- [Arduino Uno]({{< ref "arduino" >}}) : téléversement du firmware et programmes de test.

> **Sécurité :** l’anneau doit disposer d’une alimentation 12 V protégée par un fusible adapté. Sa puissance ne doit jamais transiter par une sortie de l’Arduino.

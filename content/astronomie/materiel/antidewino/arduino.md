---
title: "Arduino Uno"
description: "Câblage, installation du firmware et tests de l’Arduino d’AntiDewino."
weight: 20
---

Cette page décrit la partie Arduino d’AntiDewino. L’[architecture générale]({{< ref "architecture" >}}) présente séparément la commande USB et le circuit de puissance 12 V.

## Matériel nécessaire

- un Arduino Uno et son câble USB ;
- un module MOSFET D4184 ;
- une LED RGB à anode commune et ses résistances ;
- une petite charge de test avec une alimentation adaptée.

> Pour les premiers essais, ne pas raccorder l’anneau chauffant. Une charge ne doit jamais être alimentée directement par une broche de l’Arduino.

## Câblage

| Arduino | Connexion |
|---|---|
| D9 | Entrée PWM du D4184 |
| GND | Masse de l’entrée du D4184 |
| D2 | Rouge de la LED RGB, avec une résistance |
| D4 | Vert de la LED RGB, avec une résistance |
| D7 | Bleu de la LED RGB, avec une résistance |
| 5 V | Anode commune de la LED RGB |

La charge utilise sa propre alimentation. Seuls D9 et la masse relient sa commande à l’Arduino.

## Installer le firmware

1. installer l’IDE Arduino ;
2. installer la bibliothèque **Firmata** depuis le gestionnaire de bibliothèques ;
3. ouvrir `firmware/antidewino_firmata/antidewino_firmata.ino` ;
4. sélectionner la carte **Arduino Uno** et son port USB ;
5. téléverser le programme.

Il faut utiliser le firmware du dépôt et non l’exemple `StandardFirmata` : cette version ajoute la commande du chauffage sur D9 et l’affichage du niveau sur la LED RGB. La communication Firmata utilise une vitesse de **57 600 bauds**.

## Vérifier chaque élément

Les programmes du dossier `firmware` sont indépendants et doivent être téléversés un par un :

1. `test_led_rgb` vérifie les trois couleurs de la LED ;
2. `diagnostic_d9` vérifie la sortie D9, reliée temporairement à A0 avec le D4184 débranché ;
3. `test_d4184_moteur_lent` vérifie doucement le module avec une petite charge ;
4. `test_d4184_marche_arret` teste trois niveaux de puissance.

Après les essais, téléverser de nouveau `antidewino_firmata.ino`.

## Résultat attendu

Au démarrage, la sortie de chauffage et la LED restent éteintes. À la réception d’une commande, D9 module la puissance entre 0 et 255 :

| Commande | LED |
|---:|---|
| 0 | Éteinte |
| 1 à 84 | Jaune |
| 85 à 169 | Orange |
| 170 à 255 | Rouge |

En cas de comportement anormal, débrancher la charge puis vérifier le type de LED, la masse commune et la connexion de D9.

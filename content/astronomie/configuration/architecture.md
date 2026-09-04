---
title: "Architecture de l’observatoire"
description: "Organisation de la station cliente, du serveur INDI et des équipements astronomiques."
weight: 5
---

L’architecture distingue la **monture**, qui assure les mouvements, du **télescope et de ses accessoires**, portés mécaniquement par la monture. Toutes les commandes convergent vers le hub USB du serveur INDI.

[![Schéma de l’architecture physique de l’observatoire : station cliente, serveur INDI, hub USB, monture, télescope et système anti-rosée](/assets/images/architecture-observatoire.svg)](/assets/images/architecture-observatoire.svg)

*Cliquer sur le schéma pour l’ouvrir en pleine taille. Les traits bleus représentent les liaisons USB ou réseau, les traits gris pointillés la fixation mécanique et les traits jaunes la chaîne de puissance de l’anti-rosée.*

## Station cliente

La station exécute **KStars/Ekos** et communique avec le serveur grâce au protocole INDI. Le GPS et le joystick sont physiquement branchés sur cette station, puis exportés vers le serveur avec USB/IP.

## Serveur INDI

Le serveur Ubuntu centralise les pilotes et les profils matériels. Son hub USB distribue les connexions vers la monture, le Canon, la caméra de guidage, le focuser et l’Arduino AntiDewino.

## Gestion de la rosée

**AntiDewino** reçoit de l’ordinateur une consigne de chauffe via USB et le protocole Firmata. L’Arduino Uno convertit cette consigne en un signal PWM sur D9, puis le module MOSFET D4184 module la puissance 12 V envoyée à l’anneau chauffant installé sur la lame correctrice du C8 EdgeHD.

L’anneau n’est jamais raccordé directement à une sortie de l’Arduino. AntiDewino ne nécessite pas de pilote INDI : sa commande utilise directement la liaison série USB. Consulter la [documentation d’AntiDewino]({{< ref "/astronomie/materiel/antidewino" >}}) pour le câblage et le fonctionnement détaillés.

## Flux et commandes

| Source | Destination | Liaison | Usage |
|---|---|---|---|
| KStars / Ekos | Serveur INDI | INDI / réseau | Pilotage et acquisition |
| GPS U-Blox | Serveur INDI | USB/IP | Position et synchronisation |
| Joystick | Serveur INDI | USB/IP | Commande manuelle de la monture |
| Serveur INDI | Hub USB | USB | Concentration des équipements de l’observatoire |
| Hub USB | Monture EQ6-R Pro | USB / série | Pointage et suivi |
| Hub USB | Canon EOS 1200D | USB | Acquisition principale |
| Hub USB | ASI120MM-S | USB | Guidage et résolution astrométrique |
| Hub USB | Focuser Celestron SCT | USB | Mise au point motorisée |
| Ordinateur de commande | Arduino Uno / AntiDewino | USB / Firmata | Envoi de la consigne de chauffe |
| Arduino Uno / AntiDewino | Module D4184 | PWM sur D9 | Modulation de la puissance |
| Module D4184 | Anneau chauffant 12 V | Alimentation de puissance | Prévention de la rosée sur la lame correctrice |

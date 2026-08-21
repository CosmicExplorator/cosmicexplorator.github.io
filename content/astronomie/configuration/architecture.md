---
title: "Architecture de l’observatoire"
description: "Organisation de la station cliente, du serveur INDI et des équipements astronomiques."
weight: 5
---

L’architecture sépare l’interface de pilotage du serveur chargé de communiquer avec les équipements.

{{< mermaid >}}
flowchart LR
    subgraph CLIENT["Station cliente"]
        K["KStars / Ekos"]
        G["GPS U-Blox"]
        J["Joystick"]
    end

    subgraph SERVER["Serveur INDI - Ubuntu 26.04"]
        I["INDI Server"]
        M["Monture EQ6-R Pro"]
        Z["Caméra ZWO ASI"]
        C["Canon EOS 1200D"]
        F["Focuser Celestron SCT"]
    end

    subgraph DEW["Gestion de la rosée"]
        H["Ordinateur de commande<br/>Firmata"]
        A["Arduino Uno<br/>AntiDewino"]
        D["Module D4184"]
        R["Anneau chauffant 12 V<br/>lame correctrice"]
    end

    K <-->|"Protocole INDI / réseau"| I
    G -. "Export USB/IP" .-> I
    J -. "Export USB/IP" .-> I

    I --- M
    I --- Z
    I --- C
    I --- F
    H -->|"USB / série"| A
    A -->|"PWM D9"| D
    D --> R
{{< /mermaid >}}

## Station cliente

La station exécute **KStars/Ekos** et communique avec le serveur grâce au protocole INDI. Le GPS et le joystick sont physiquement branchés sur cette station, puis exportés vers le serveur avec USB/IP.

## Serveur INDI

Le serveur Ubuntu centralise les pilotes et les profils matériels. La monture, les caméras et le focuser y sont directement connectés.

## Gestion de la rosée

**AntiDewino** reçoit de l’ordinateur une consigne de chauffe via USB et le protocole Firmata. L’Arduino Uno convertit cette consigne en un signal PWM sur D9, puis le module MOSFET D4184 module la puissance 12 V envoyée à l’anneau chauffant installé sur la lame correctrice du C8 EdgeHD.

L’anneau n’est jamais raccordé directement à une sortie de l’Arduino. AntiDewino ne nécessite pas de pilote INDI : sa commande utilise directement la liaison série USB. Consulter la [documentation d’AntiDewino]({{< ref "/astronomie/materiel/antidewino" >}}) pour le câblage et le fonctionnement détaillés.

## Flux et commandes

| Source | Destination | Liaison | Usage |
|---|---|---|---|
| KStars / Ekos | Serveur INDI | INDI / réseau | Pilotage et acquisition |
| GPS U-Blox | Serveur INDI | USB/IP | Position et synchronisation |
| Joystick | Serveur INDI | USB/IP | Commande manuelle de la monture |
| Ordinateur de commande | Arduino Uno / AntiDewino | USB / Firmata | Envoi de la consigne de chauffe |
| Arduino Uno / AntiDewino | Module D4184 | PWM sur D9 | Modulation de la puissance |
| Module D4184 | Anneau chauffant 12 V | Alimentation de puissance | Prévention de la rosée sur la lame correctrice |

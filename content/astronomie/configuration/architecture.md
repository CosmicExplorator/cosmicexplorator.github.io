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

    subgraph DEW["Gestion autonome de la rosée"]
        A["Arduino Uno<br/>AntiDewino"]
        R["Anneau chauffant 12 V<br/>lame correctrice"]
    end

    K <-->|"Protocole INDI / réseau"| I
    G -. "Export USB/IP" .-> I
    J -. "Export USB/IP" .-> I

    I --- M
    I --- Z
    I --- C
    I --- F
    A --> R
{{< /mermaid >}}

## Station cliente

La station exécute **KStars/Ekos** et communique avec le serveur grâce au protocole INDI. Le GPS et le joystick sont physiquement branchés sur cette station, puis exportés vers le serveur avec USB/IP.

## Serveur INDI

Le serveur Ubuntu centralise les pilotes et les profils matériels. La monture, les caméras et le focuser y sont directement connectés.

## Gestion de la rosée

**AntiDewino** est un contrôleur autonome basé sur un Arduino Uno. Il mesure les conditions autour du télescope et ajuste, par l’intermédiaire d’un étage de puissance, la puissance de l’anneau chauffant installé sur la lame correctrice du C8 EdgeHD.

L’anneau est alimenté en 12 V et n’est jamais raccordé directement à une sortie de l’Arduino. AntiDewino fonctionne indépendamment du serveur INDI et de KStars/Ekos. Consulter la [documentation d’AntiDewino]({{< ref "/astronomie/materiel/antidewino" >}}) pour le détail de cette architecture.

## Flux et commandes

| Source | Destination | Liaison | Usage |
|---|---|---|---|
| KStars / Ekos | Serveur INDI | INDI / réseau | Pilotage et acquisition |
| GPS U-Blox | Serveur INDI | USB/IP | Position et synchronisation |
| Joystick | Serveur INDI | USB/IP | Commande manuelle de la monture |
| Arduino Uno / AntiDewino | Anneau chauffant 12 V | Commande par étage de puissance | Prévention de la rosée sur la lame correctrice |

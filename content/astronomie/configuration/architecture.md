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

    subgraph DEW["Gestion de la rosée - en conception"]
        A["AntiDewino"]
        R["Ruban chauffant"]
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

**AntiDewino** est un contrôleur Arduino autonome, actuellement en phase de conception. Il doit mesurer les conditions autour du télescope et ajuster la puissance du ruban chauffant placé sur la lame.

Ce contrôleur ne dépend pas du serveur INDI dans l’architecture actuelle. Son circuit de puissance, ses capteurs et ses connexions restent à valider. Consulter la [documentation d’AntiDewino]({{< ref "/astronomie/materiel/antidewino" >}}) pour suivre sa conception.

## Flux et commandes

| Source | Destination | Liaison | Usage |
|---|---|---|---|
| KStars / Ekos | Serveur INDI | INDI / réseau | Pilotage et acquisition |
| GPS U-Blox | Serveur INDI | USB/IP | Position et synchronisation |
| Joystick | Serveur INDI | USB/IP | Commande manuelle de la monture |
| AntiDewino | Ruban chauffant | Commande de puissance | Prévention de la rosée (en conception) |

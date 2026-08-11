---
title: "HOWTO — Résolution des problèmes"
description: "Transformer les incidents rencontrés pendant les sessions en solutions vérifiées et réutilisables."
weight: 40
---

Cette page capitalise simplement les problèmes rencontrés et les solutions validées pendant les sessions.

## Focuser instable via le hub USB

- **Problème :** erreurs USB, arrêt du moteur et déplacements impossibles lorsque le focuser est connecté au hub.
- **Solution :** brancher le focuser directement sur le serveur INDI.
- **Contrôle Ekos :** `KStars → Outils → Ekos → Mise au point → Position du focuser`.
- **Contrôle INDI :** `Panneau de contrôle INDI → Celestron SCT → Connexion`, puis tester un déplacement dans les deux sens.

## StellarSolver ne résout pas le champ

- **Problème :** StellarSolver échoue à résoudre le champ de l’ASI120.
- **Solution :** installer les index `4207` à `4210`, puis relancer la résolution.
- **Chemin :** `KStars → Outils → Ekos → Alignement → Options → Fichiers d’index`.

## Coordonnées nulles dans Ekos

- **Problème :** Ekos affiche des coordonnées nulles après le démarrage.
- **Solution :** vérifier que la monture est `Parked`, puis la déparquer pour faire apparaître les coordonnées.
- **Chemin :** `KStars → Outils → Ekos → Monture → État du parcage`, puis `Panneau de contrôle INDI → EQMod Mount`.
- **Contrôle INDI :** `Panneau de contrôle INDI → EQMod Mount → Gestion des sites → État : Parked`.

## Guidage très instable

- **Problème :** le guidage affiche un RMS compris entre 16 et 23 secondes d’arc.
- **Solution :** refaire la calibration avec dix itérations, une impulsion de 1000 ms et une agressivité de 0,70 en AD et 0,60 en DEC.
- **Chemin :** `KStars → Outils → Ekos → Guidage → Options → Calibration`.
- **Contrôle INDI :** `Panneau de contrôle INDI → EQMod Mount → Guidage`, pour vérifier la réception des impulsions.

## Modèle à recopier

```markdown
## Nom court du problème

- **Problème :** …
- **Solution :** …
```

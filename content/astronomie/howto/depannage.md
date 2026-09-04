---
title: "Résoudre un problème"
description: "Identifier rapidement un incident et appliquer une solution déjà vérifiée."
weight: 40
type: "howto"
duration: "Selon le problème"
difficulty: "Diagnostic"
---

> **Mode d’emploi :** choisissez le symptôme dans le sommaire, appliquez la solution, puis effectuez le contrôle indiqué.

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

## Aucun mouvement avec les commandes Est/Ouest

- **Problème :** la monture est connectée et déparquée, mais un clic sur `Est` ou `Ouest` ne produit aucun mouvement perceptible.
- **Cause :** les boutons de mouvement sont actifs uniquement pendant leur maintien. Un clic bref démarre et arrête le déplacement presque instantanément ; le journal affiche alors `Starting West slew`, puis `West Slew stopped` à la même seconde.
- **Solution :** dans `Panneau de contrôle INDI → EQMod Mount → Contrôle du mouvement`, choisir `32×`, puis maintenir `Est` ou `Ouest` enfoncé. Tester d'abord pendant 2 à 3 secondes.
- **Rotation de 15° :** à `32×`, maintenir le même bouton pendant environ `1 min 53 s`. Pour l'alignement polaire, effectuer les deux rotations dans le même sens, sans desserrer les freins.
- **Sécurité :** surveiller les câbles et garder le bouton `STOP` accessible pendant le déplacement.

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

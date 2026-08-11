---
title: "Alignement polaire avec Ekos"
description: "Mesurer et corriger l’erreur polaire de l’EQ6-R avec l’assistant Ekos."
weight: 26
---

Cette méthode utilise le train de guidage, dont le champ large facilite la résolution astrométrique. Elle peut affiner une première mise en station réalisée avec le [viseur polaire](../alignement-polaire-viseur/).

Elle a permis d’obtenir une erreur polaire totale de **3′23″**.

## Prérequis

- la procédure [Démarrer une session d’observation](../demarrer-session/) est terminée ;
- la monture est en position initiale et encore parquée ;
- le train `EvoGuide 50ED + ASI120MM-S` existe dans Ekos ;
- les index StellarSolver `4207` à `4210` sont installés ;
- les câbles disposent d’assez de mou pour deux rotations de l’axe AD.

## 1. Vérifier la monture dans INDI

**Chemin :** `Panneau de contrôle INDI → EQMod Mount → Connexion`

- vérifier que la monture est connectée ;
- vérifier l’état `Parked` ;
- contrôler visuellement le dégagement autour du pilier ;
- vérifier les limites de sécurité avant tout mouvement.

Ne pas utiliser **Effacer le parcage** ni **Purger toutes les configurations**.

## 2. Ouvrir l’outil d’alignement polaire

**Chemin :** `KStars → Outils → Ekos → Alignement → Alignement polaire`

| Paramètre | Valeur |
|---|---|
| Train optique | `EvoGuide 50ED + ASI120MM-S` |
| Exposition | `5 s` |
| Regroupement | `1×1` |
| Solveur | `StellarSolver` hors ligne |
| Rotation par étape | `15°` |
| Pointage manuel | Activé |
| Vitesse de déplacement | `32×`, puis `8×` pour finir |

## 3. Vérifier les index StellarSolver

Si la résolution ne démarre pas :

**Chemin :** `Ekos → Alignement → Options → Fichiers d’index`

Vérifier la présence des index `4207`, `4208`, `4209` et `4210`. Il est inutile de télécharger tous les index.

## 4. Lancer les trois acquisitions

1. déparquer la monture depuis `Ekos → Monture → Déparquer` ;
2. cliquer sur **Démarrer** dans l’outil d’alignement polaire ;
3. attendre la première acquisition et sa résolution ;
4. déplacer uniquement l’axe AD de `15°` avec les moteurs ;
5. attendre la deuxième acquisition et sa résolution ;
6. déplacer à nouveau l’axe AD de `15°` dans le même sens ;
7. attendre la troisième acquisition et sa résolution.

Une rotation de `15°` correspond à environ une heure d’ascension droite. Ne pas desserrer les freins pendant la procédure.

## 5. Corriger l’altitude et l’azimut

Après la troisième résolution, Ekos passe à l’étape **Ajuster**.

**Chemin :** `Ekos → Alignement → Alignement polaire → Ajuster → Actualiser`

1. cliquer sur **Actualiser** pour lancer les mesures répétées ;
2. corriger doucement l’altitude avec les réglages mécaniques de la monture ;
3. corriger ensuite l’azimut ;
4. attendre au moins deux images après chaque mouvement ;
5. continuer jusqu’à obtenir une erreur compatible avec la session.

Ne pas cliquer sur **Démarrer** à cette étape : ce bouton recommence toute la séquence et demande à nouveau les rotations.

## 6. Résultat de référence

| Mesure | Valeur obtenue |
|---|---|
| Erreur totale | **3′23″** |
| Altitude | Environ **-3′00″** |
| Azimut | Environ **-1′33″** |

Cette valeur constitue un bon point de référence pour les prochaines sessions. La précision nécessaire dépendra ensuite de la focale et du temps de pose.

## 7. Terminer la procédure

- arrêter l’actualisation ;
- vérifier que la monture est toujours loin du pilier ;
- conserver la valeur finale dans le journal de session ;
- passer au pointage d’une étoile puis au test de guidage.

## RETEX

- **Problème :** lors de la première nuit, la rotation automatique était trop importante et la monture s’est approchée du pilier.
  - **Solution :** activer le pointage manuel et limiter chaque rotation à `15°`.
- **Problème :** cliquer sur **Démarrer** pendant la correction relance toute la procédure.
  - **Solution :** utiliser **Actualiser** à l’étape **Ajuster**.
- **Problème :** StellarSolver ne résout pas les images de l’EvoGuide.
  - **Solution :** installer les index `4207` à `4210` depuis les options d’alignement.

## Checklist

- [ ] Monture connectée, parquée et dégagement vérifié
- [ ] Train EvoGuide + ASI120 sélectionné
- [ ] Index StellarSolver présents
- [ ] Pointage manuel activé
- [ ] Rotations limitées à 15°
- [ ] Trois images résolues
- [ ] Correction réalisée avec **Actualiser**
- [ ] Erreur finale notée dans le journal de session

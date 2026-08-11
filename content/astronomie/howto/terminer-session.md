---
title: "Terminer une session d’observation"
description: "Arrêter proprement les acquisitions, la monture et le serveur INDI."
weight: 20
---

Cette procédure met l’installation en sécurité et conserve les informations utiles pour la prochaine nuit.

## 1. Arrêter les opérations en cours

- arrêter la séquence dans `Ekos → Acquisition → Arrêter` ;
- arrêter le guidage dans `Ekos → Guidage → Arrêter` ;
- arrêter la mise au point dans `Ekos → Mise au point → Arrêter` ;
- arrêter l’alignement dans `Ekos → Alignement → Arrêter` s’il est actif ;
- attendre la fin de l’écriture des images sur le disque.

## 2. Parquer la monture

**Chemin :** `KStars → Outils → Ekos → Monture → Parquer`

1. cliquer sur **Parquer** dans le module Monture ;
2. contrôler l’état avec `Panneau de contrôle INDI → EQMod Mount → Gestion des sites → Parked` ;
3. vérifier visuellement que la barre de contrepoids est verticale vers le bas et que le C8 pointe vers le pôle ;
4. ne pas couper l’alimentation tant que le parcage n’est pas terminé.

## 3. Fermer KStars et Ekos

- déconnecter les équipements avec `Ekos → Panneau principal → Déconnecter` ;
- arrêter le profil avec `Ekos → Panneau principal → Arrêter INDI` ;
- fermer KStars après avoir vérifié que les images et les journaux sont enregistrés.

En cas de doute, contrôler individuellement :

`Panneau de contrôle INDI → Équipement → Connexion → Déconnecter`

## 4. Arrêter le profil INDI

Depuis le dépôt `indi-ansible`, arrêter le profil utilisé pendant la nuit :

```bash
ansible-playbook playbooks/profile_eq6r_asi_focuser_canon_joystick_gps.yml \
  -e "state=stopped"
```

Vérifier ensuite qu’aucun profil `indiserver-*` n’est encore actif.

## 5. Déconnecter et protéger le matériel

- arrêter les exports USB/IP du GPS et du joystick s’ils ne sont plus nécessaires ;
- couper les alimentations dans un ordre maîtrisé ;
- remettre les bouchons sur les optiques et les caméras ;
- ranger les câbles sans déplacer la monture parquée ;
- protéger l’installation contre l’humidité.

## 6. Sauvegarder le RETEX

- noter la cible et les principaux résultats ;
- conserver les captures utiles ;
- ajouter chaque problème et sa solution en liste à puces ;
- noter les actions à reprendre lors de la prochaine session ;
- vérifier que les acquisitions importantes sont sauvegardées.

## Checklist rapide

- [ ] Acquisition et guidage arrêtés
- [ ] Images enregistrées
- [ ] Monture `Parked` et position vérifiée
- [ ] Équipements déconnectés dans Ekos
- [ ] Profil INDI arrêté
- [ ] Alimentations coupées
- [ ] Optiques protégées
- [ ] RETEX et sauvegarde terminés

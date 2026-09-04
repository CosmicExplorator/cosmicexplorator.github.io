---
title: "Configurer KStars et Ekos avec le serveur INDI"
description: "Créer un profil Ekos distant et les trains optiques de l’observatoire."
weight: 10
type: "howto"
duration: "20 min"
difficulty: "Intermédiaire"
steps: 7
---

> **Objectif :** connecter KStars au serveur `telescope.lan`, puis créer les deux trains optiques de l’observatoire.

## Prérequis

- le serveur INDI répond sur `telescope.lan:7624` ;
- le profil matériel adapté est démarré avec `indi-ansible` ;
- KStars et Ekos sont installés sur la station cliente ;
- la monture reste parquée pendant la configuration initiale.

## 1. Démarrer le profil matériel

Pour charger l’ensemble de l’installation :

```bash
ansible-playbook playbooks/profile_eq6r_asi_focuser_canon_joystick_gps.yml
```

Le playbook attache le GPS et le joystick exportés par USB/IP, vérifie le matériel puis démarre INDI.

## 2. Créer le profil Ekos distant

**Chemin :** `KStars → Outils → Ekos → Profils → +`

Dans la fenêtre de profil Ekos :

1. créer un nouveau profil ;
2. le nommer `EQ6R ASI Focuser Canon Joystick GPS` ;
3. choisir le mode de connexion **Distant** ;
4. saisir l’hôte `telescope.lan` ;
5. saisir le port `7624` ;
6. choisir le guidage **Interne** ;
7. désactiver **INDI Web Manager** ;
8. laisser **Connexion automatique** désactivée pour le premier test.

## 3. Affecter les pilotes

**Chemin :** `KStars → Outils → Ekos → Profils → Modifier le profil → Équipements`

| Fonction | Pilote ou équipement |
|---|---|
| Monture | `EQMod Mount` |
| Caméra principale | `Canon DSLR` |
| Caméra de guidage | `ZWO CCD` |
| Focuser | `Celestron SCT Focuser` |
| Auxiliaire | `Joystick` |
| Auxiliaire | `GPSD` |

Enregistrer le profil, démarrer INDI puis connecter manuellement chaque équipement. Activer la connexion automatique uniquement après un premier démarrage complet réussi.

## 4. Créer le train principal

**Chemin :** `KStars → Outils → Ekos → Éditeur de train optique → +`

Créer le train **C8 EdgeHD + Canon 1200D** avec les valeurs suivantes :

| Paramètre | Valeur |
|---|---|
| Monture | `EQMod Mount` |
| Caméra | `Canon DSLR EOS 1200D` |
| Ouverture | `203,2 mm` |
| Focale | `2032 mm` |
| Capteur | `5184 × 3456` |
| Taille des pixels | `4,30 × 4,30 µm` |
| Focuser | `Celestron SCT` |
| Réducteur / Barlow | `1,00×` |

Utiliser ce train pour **Acquisition**, **Mise au point** et **Alignement** lorsque la précision du capteur principal doit être contrôlée.

## 5. Créer le train de guidage

**Chemin :** `KStars → Outils → Ekos → Éditeur de train optique → +`

Créer le train **EvoGuide 50ED + ASI120MM-S** :

| Paramètre | Valeur |
|---|---|
| Monture | `EQMod Mount` |
| Caméra | `ZWO CCD ASI120MM-S` |
| Ouverture | `50 mm` |
| Focale | `242 mm` |
| Capteur | `1280 × 960` |
| Taille des pixels | `3,75 × 3,75 µm` |
| Guidage via | `EQMod Mount` |
| Focuser | Aucun |
| Réducteur / Barlow | `1,00×` |

Utiliser ce train pour le **Guidage** et pour un alignement polaire rapide grâce à son champ plus large.

## 6. Valider la configuration

**Chemin :** `KStars → Outils → Ekos → Démarrer INDI → Panneau de contrôle INDI`

- [ ] Le profil Ekos se connecte à `telescope.lan:7624`.
- [ ] Les six équipements apparaissent dans le panneau INDI.
- [ ] Les deux trains optiques sont disponibles dans les modules Ekos.
- [ ] Le Canon est sélectionné pour l’acquisition principale.
- [ ] L’ASI120 est sélectionnée pour le guidage.
- [ ] La monture affiche `Parked` avant le premier mouvement.

## 7. Retrouver les contrôles INDI

Ouvrir le panneau avec :

`KStars → Outils → Périphériques → Panneau de contrôle INDI`

Puis vérifier chaque équipement :

| Équipement | Chemin INDI | Contrôle |
|---|---|---|
| Monture | `INDI → EQMod Mount → Connexion` | État connecté |
| Parcage | `INDI → EQMod Mount → Gestion des sites → Options de parcage` | État `Parked` et position enregistrée |
| Canon | `INDI → Canon DSLR EOS 1200D → Connexion` | Appareil détecté et connecté |
| Caméra ZWO | `INDI → ZWO CCD ASI120MM-S → Connexion` | Caméra détectée et connectée |
| Focuser | `INDI → Celestron SCT → Connexion` | Port stable et position lisible |
| GPS | `INDI → GPSD → Connexion` | Coordonnées reçues |
| Joystick | `INDI → Joystick → Connexion` | Périphérique détecté |

Pour enregistrer la position de parcage de l’EQ6-R :

`INDI → EQMod Mount → Gestion des sites → Options de parcage → Courant → Écrire les données`

## En cas de problème

Si les coordonnées semblent nulles, suivre d’abord :

`KStars → Outils → Ekos → Monture → État du parcage`

Puis contrôler directement :

`Panneau de contrôle INDI → EQMod Mount → État : Parked`

Pour les autres incidents validés pendant les sessions, consulter le [HowTo de résolution des problèmes](../depannage/).

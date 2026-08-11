---
title: "Démarrer une session d’observation"
description: "Mettre en route l’installation et vérifier qu’elle est prête avant le premier mouvement."
weight: 15
---

Cette procédure suppose que le profil Ekos et les trains optiques existent déjà. Pour leur création ou leur modification, consulter [Configurer KStars et Ekos avec le serveur INDI](../configurer-kstars-ekos/).

## 1. Installer et sécuriser le matériel

- monter les contrepoids avant le tube et conserver la butée en bout de barre ;
- installer tous les équipements avant l’équilibrage ;
- équilibrer les axes DEC puis AD ;
- vérifier le mou des câbles dans plusieurs orientations ;
- placer la monture en position initiale : contrepoids vers le bas et C8 dirigé vers le pôle ;
- vérifier que rien ne peut heurter le pilier.

## 2. Exporter les périphériques USB/IP

Sur la station cliente, exporter le joystick et le GPS :

```bash
sudo ./scripts/export_joystick_usbip.sh
sudo ./scripts/export_gps_usbip.sh
```

Le joystick et le GPS restent physiquement branchés sur la station cliente. Le serveur INDI les reçoit ensuite par USB/IP.

## 3. Démarrer le profil INDI

Depuis le dépôt `indi-ansible` :

```bash
ansible-playbook playbooks/profile_eq6r_asi_focuser_canon_joystick_gps.yml
```

Le playbook attache les périphériques USB/IP, vérifie le matériel et démarre le profil INDI.

En cas de doute, lancer d’abord le contrôle sans démarrer INDI :

```bash
ansible-playbook playbooks/check_hardware_complete.yml
```

## 4. Ouvrir le profil Ekos existant

**Chemin :** `KStars → Outils → Ekos → Profils`

1. sélectionner `EQ6R ASI Focuser Canon Joystick GPS` ;
2. cliquer sur **Démarrer INDI** ;
3. attendre la connexion des équipements ;
4. ne pas recréer le profil ni les trains optiques.

## 5. Vérifier les équipements dans INDI

**Chemin :** `KStars → Outils → Périphériques → Panneau de contrôle INDI`

- `INDI → EQMod Mount → Connexion` : monture connectée et `Parked` ;
- `INDI → Canon DSLR EOS 1200D → Connexion` : Canon connecté ;
- `INDI → ZWO CCD ASI120MM-S → Connexion` : caméra de guidage connectée ;
- `INDI → Celestron SCT → Connexion` : position du focuser lisible ;
- `INDI → GPSD → Connexion` : coordonnées reçues ;
- `INDI → Joystick → Connexion` : joystick détecté.

Si un équipement manque, ne pas déparquer la monture. Consulter le [HowTo de résolution des problèmes](../depannage/).

## 6. Sélectionner les trains optiques

- **Acquisition et mise au point :** `C8 EdgeHD + Canon 1200D` ;
- **Guidage et alignement polaire :** `EvoGuide 50ED + ASI120MM-S`.

Les valeurs détaillées des trains restent dans le [HowTo de configuration](../configurer-kstars-ekos/#4-créer-le-train-principal).

## 7. Contrôles avant déparcage

- [ ] Montage et équilibrage terminés
- [ ] Câbles libres autour des deux axes
- [ ] Profil `indi-ansible` démarré sans erreur
- [ ] Six équipements connectés dans INDI
- [ ] Monture en position initiale et `Parked`
- [ ] Trains optiques sélectionnés
- [ ] Dossier d’acquisition et espace disque vérifiés
- [ ] Limites de sécurité de la monture actives

Une fois tous les contrôles validés, la monture peut être déparquée depuis :

`KStars → Outils → Ekos → Monture → Déparquer`

À la fin de la nuit, suivre [Terminer une session d’observation](../terminer-session/).

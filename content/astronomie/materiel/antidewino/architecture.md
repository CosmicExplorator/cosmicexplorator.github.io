---
title: "Architecture d’AntiDewino"
description: "Architecture du contrôleur Arduino, du module D4184 et de l’anneau chauffant du C8 EdgeHD."
aliases:
  - /astronomie/materiel/antidewino/conception/
weight: 10
---

## Principe de fonctionnement

AntiDewino reçoit de l’ordinateur une consigne de chauffe comprise entre **0 et 255**. Le firmware Firmata transmet cette valeur à la sortie PWM **D9** de l’Arduino Uno. Le module MOSFET **D4184** module alors la puissance fournie par l’alimentation 12 V à l’anneau chauffant de la lame correctrice du C8 EdgeHD.

Une LED RGB indique visuellement le niveau demandé. Dans l’implémentation actuelle, la mesure des conditions ambiantes et le calcul de la consigne ne sont pas réalisés par l’Arduino.

{{< mermaid >}}
flowchart LR
    H["Ordinateur<br/>consigne 0 à 255"] -->|"USB / Firmata<br/>57 600 bauds"| A["Arduino Uno<br/>firmware AntiDewino"]
    A -->|"PWM sur D9"| M["Module MOSFET<br/>D4184"]
    A -->|"D2 / D4 / D7"| L["LED RGB<br/>niveau de chauffe"]
    P["Alimentation 12 V<br/>protégée par fusible"] --> M
    M --> R["Anneau chauffant 12 V<br/>lame du C8 EdgeHD"]
{{< /mermaid >}}

## Répartition des rôles

| Élément | Rôle |
|---|---|
| Ordinateur | Envoie la consigne de chauffe par le protocole Firmata |
| Arduino Uno | Reçoit la consigne, produit le signal PWM et pilote la LED d’état |
| Module D4184 | Commute et module la puissance 12 V destinée à l’anneau |
| Alimentation 12 V | Fournit l’énergie à l’anneau chauffant, indépendamment du 5 V de l’Arduino |
| Anneau chauffant | Chauffe la lame correctrice du C8 EdgeHD pour prévenir la buée |
| LED RGB à anode commune | Indique le niveau de chauffe demandé |

AntiDewino ne dépend pas d’un pilote INDI. La communication de commande passe directement par la liaison série USB et Firmata.

## Câblage de commande

| Arduino Uno | Connexion | Fonction |
|---|---|---|
| D9 | Entrée PWM du D4184 | Commande de chauffe, de 0 à 255 |
| GND | Masse de l’entrée du D4184 | Référence commune du signal PWM |
| D2 | Rouge de la LED, avec une résistance | Signalisation |
| D4 | Vert de la LED, avec une résistance | Signalisation |
| D7 | Bleu de la LED, avec une résistance | Signalisation |
| 5 V | Anode commune de la LED RGB | Alimentation de la LED |

L’anneau possède sa propre alimentation 12 V. Seuls le signal D9 et la masse relient l’Arduino à l’entrée de commande du D4184 : l’anneau n’est jamais alimenté par une broche de l’Arduino.

## Niveaux de chauffe

| Consigne PWM | Niveau | LED |
|---:|---|---|
| 0 | Arrêt | Éteinte |
| 1 à 84 | Faible | Jaune |
| 85 à 169 | Moyen | Orange |
| 170 à 255 | Fort | Rouge |

La teinte orange est obtenue par une modulation logicielle non bloquante du canal vert sur D4, afin de ne pas perturber les échanges Firmata.

## Démarrage et sécurité

Lors d’un démarrage ou d’une réinitialisation Firmata, la commande de chauffe est remise à **0** et la LED est éteinte. Le système respecte également les principes suivants :

- alimentation de puissance séparée de l’Arduino ;
- masse commune entre l’Arduino et l’entrée du D4184 ;
- fusible adapté, placé au plus près de l’alimentation 12 V ;
- câbles et connecteurs dimensionnés pour le courant de l’anneau ;
- premiers essais effectués avec une petite charge de test avant de raccorder l’anneau.

## Firmware et programmes de test

Le dépôt `AntiDewino` contient le firmware normal et plusieurs programmes de diagnostic :

| Programme | Usage |
|---|---|
| `antidewino_firmata` | Fonctionnement normal : Firmata, PWM D9 et LED RGB |
| `test_led_rgb` | Vérification des trois canaux de la LED |
| `diagnostic_d9` | Vérification de D9 avec un retour de mesure sur A0, D4184 débranché |
| `test_d4184_moteur_lent` | Essai prudent du D4184 avec une petite charge |
| `test_d4184_marche_arret` | Essai des niveaux 25 %, 60 % et 100 % |

Après un diagnostic, il faut téléverser de nouveau `antidewino_firmata.ino` pour rétablir le fonctionnement normal. Le [guide Arduino Uno]({{< ref "arduino" >}}) détaille le téléversement et les essais.

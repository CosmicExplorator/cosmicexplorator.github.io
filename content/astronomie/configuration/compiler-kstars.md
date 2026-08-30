---
title: "Compiler KStars"
url: /compilKstars/
description: "Compiler KStars depuis les sources et le connecter à un serveur INDI distant."
weight: 20
---

## Prérequis

- dépendances de compilation KStars installées ;
- INDI installé ;
- serveur INDI distant accessible.

## 1. Télécharger les sources

```bash
mkdir -p ~/git
git clone https://github.com/KDE/kstars.git ~/git/kstars
```

## 2. Compiler et installer

```bash
cmake -S ~/git/kstars -B ~/git/kstars/build \
  -DCMAKE_INSTALL_PREFIX=/usr \
  -DCMAKE_BUILD_TYPE=Release
cmake --build ~/git/kstars/build --parallel
sudo cmake --install ~/git/kstars/build
```

## 3. Lancer KStars

```bash
kstars
```

## 4. Connecter le serveur INDI

1. ouvrir **Outils → Ekos** ;
2. créer un profil **Distant** ;
3. renseigner l’adresse du serveur INDI et le port `7624` ;
4. démarrer le profil ;
5. vérifier la connexion de chaque équipement.

![Profil INDI distant](/assets/images/compilUseKstars/2025-01-12_20-53.png)

![Équipements INDI](/assets/images/compilUseKstars/2025-01-12_20-52.png)

![Équipements connectés dans Ekos](/assets/images/compilUseKstars/2025-01-12_20-48.png)

## Checklist

- [ ] Compilation terminée sans erreur
- [ ] KStars démarre
- [ ] Profil distant créé
- [ ] Serveur INDI joignable sur le port `7624`
- [ ] Équipements connectés et pilotables dans Ekos

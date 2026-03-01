---
layout: default
title: Sauvegarde Kopia
permalink: /compilKstarts/
---


 
 
 
 
# Compilation des sources:
```bash

root@station:~# mkdir git; cd git;

root@station:~/git# git clone https://github.com/KDE/kstars.git kstars
root@station:~/git# cd kstars/;mkdir build;cd build

root@station:~/git/kstars/build# cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Debug\
 ~/git/kstars/
root@station:~/git/kstars/build# make -j$(nproc)
root@station:~/git/kstars/build# make install
```

# Lancement de l'appli
```
emmanuel@station:~# kstars
```


# Connexion au serveur indilib distant


![Projet Indilib](/assets/images/compilUseKstars/2025-01-12_20-48.png)

Les équipements chargés par IndiServer sur le server, sont bien vu depuis la station cliente qui exécute kstars.  Ils sont bien tous connectés et pilotables via Ekos.


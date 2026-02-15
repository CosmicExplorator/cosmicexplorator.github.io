---
layout: default
title: Sauvegarde Kopia
permalink: /svgWithKopia/
---


# Sauvegarder avec Kopia

Voici la procédure que j'utilise pour renouveler automatiquement un certificat
Let's Encrypt via acme.sh et OVH DNS.


## 0. Ptit mémo: architecture


                     +---------------------------+
                     |     Serveur Nextcloud     |
                     |---------------------------|
                     |  - Service Nextcloud      |
                     |  - Kopia (backup)         |
                     +------------+--------------+
                                  |
                                  | Montage NFS
                                  v
                     +---------------------------+
                     |       Synology NAS       |
                     |---------------------------|
                     |  Stockage des sauvegardes|
                     +---------------------------+



```
root@nextcloud:~/letsencrypt# tree -d -a
.
├── config
│   ├── accounts
│   │   └── acme-v02.api.letsencrypt.org
│   │       └── directory
│   │           └── 99b2791cd2c5f9982788289fceb80b6c
│   ├── archive

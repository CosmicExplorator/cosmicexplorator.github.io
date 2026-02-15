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

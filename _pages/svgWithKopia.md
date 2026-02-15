---
layout: default
title: Sauvegarde Kopia
permalink: /svgWithKopia/
---


# Sauvegarder avec Kopia

Voici la procédure que j'utilise pour renouveler automatiquement un certificat
Let's Encrypt via acme.sh et OVH DNS.


## 0. Ptit mémo: architecture


                     +-----------------------------------+
                     |     Serveur Nextcloud             |
                     |-----------------------------------|
                     |  - Service Nextcloud              |
                     |  - Kopia (backup)  :51515         |   <------- Snapshot : 12h20
                     +------------+----------------------+
                                  |
                                  | Montage NFS
                                  v
                     +---------------------------+
                     |       Synology NAS        | <----------------   Demarrage quotidien: 11h50 - 13h00
                     |---------------------------|                        - 12h00 : renew certficiat
                     |  Stockage des sauvegardes | 
                     +---------------------------+



## 1. Installation sur Ubuntu

``` bash
apt install kopia -y
```

## 2. Configuration

### vérifier le montage NFS actif (démarrer le NAS)
``` bash
root@nextcloud:~# mount |grep nas
10.0.1.5:/volume1/backup_nextcloud on /media/nas2b_for_kopia type nfs4 (rw,noatime,vers=4.0,rsize=131072,wsize=131072,namlen=255,hard,proto=tcp,timeo=600,retrans=2,sec=sys,clientaddr=10.0.1.10,local_lock=none,addr=10.0.1.5,_netdev)
root@nextcloud:~#
```

### créer une instance server pour Kopia
``` bash
root@nextcloud:~# kopia repository create server
   --url https://localhost:51515
   --username xxxxx
   --password xxxxxx
   --path /media/nas2b_for_kopia
```

  


### créer un dépot (repo)
``` bash
root@nextcloud:~# /usr/bin/kopia server start
    --address=0.0.0.0:51515
    --ui
    --tls-cert-file=/etc/ssl/cosmic/fullchain.pem
    --tls-key-file=/etc/ssl/cosmic/privkey.pem
    --server-username=xxxx
    --server-password=xxxxx
   --log-level=debug
   --config-file=/root/.config/kopia/repository.config
```
--server-username= user au login
--server-password= mdp au login

### configurer une stratégie de svg (policy)

ℹ️ : avant et après il faut dans mon cas, effectuer:
- activer le mode maintenance sur nextcloud
- faire un dump de la base de donnée
- après le snapshot, désactiver le mode maintenance

``` bash
root@nextcloud:~# kopia policy set /media/nextcloud-raid1/nextcloud
--before-snapshot-root-action="/media/nextcloud-raid1/nextcloud/data/emmanuel/files/Documents/itech/kopia/script/nextcloud_maintenance_on_dump_bdd.sh"
--after-snapshot-root-action="/media/nextcloud-raid1/nextcloud/data/emmanuel/files/Documents/itech/kopia/script/nextcloud_maintenance_off.sh"
--snapshot-time=22:00 --password=xxxxxx

```
--password= mdp du server


output:

``` bash
Setting policy for root@nextcloud:/media/nextcloud-raid1/nextcloud
 - setting snapshot times to [12:20]
 - setting before-snapshot-root (essential) action command to "/media/nextcloud-raid1/nextcloud/data/emmanuel/files/Documents/itech/kopia/script/nextcloud_maintenance_on_dump_bdd.sh" and timeout 5m0s
 - setting after-snapshot-root (essential) action command to "/media/nextcloud-raid1/nextcloud/data/emmanuel/files/Documents/itech/kopia/script/nextcloud_maintenance_off.sh" and timeout 5m0s
```




### quelques captures du servive : https://@IP:51515

![Serveur:51515](/assets/images/svgWithKopia/2026-02-15_19-54.png)

![Serveur:51515](/assets/images/svgWithKopia/2026-02-15_19-55.png)

![Serveur:51515](/assets/images/svgWithKopia/2026-02-15_19-56.png)

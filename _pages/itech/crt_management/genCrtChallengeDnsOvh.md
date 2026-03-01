---
layout: default
title: Generer un certificat let's encrypt avec challenge DNS
permalink: /genCrtChallengeDnsOvh/
---


Prérequis: disposer d’un nom de domaine chez OVH


# Configurer et récupérer les éléments de l’API (ovh)


[Lien Api OVH] (https://www.ovh.com/auth/api/createToken)


Sur ce lien: créer l'api si non existante et entrez les routes suivantes (elles correspondent aux actions nécessaires pour Certbot et la validation :

- GET /domain/zone/* : Lecture des zones DNS.
- PUT /domain/zone/* : Modification des enregistrements DNS.
- POST /domain/zone/* : Ajouter des enregistrements DNS.
- DELETE /domain/zone/* : Supprimer des enregistrements DNS.
- POST /domain/zone/*/refresh : Rafraîchir la zone DNS après des modifications.

En retour copier les éléments renvoyés dans un fichier $USER_HOME/ovh.ini


```bash

dns_ovh_endpoint = ovh-eu
dns_ovh_application_key = ebf.....f
dns_ovh_application_secret = 448......e
dns_ovh_consumer_key = 5bd.....7 

```


Installer cerbot et ses dépendances 
root@cloud:~#python3 -m venv .venv/py3.12-certbot
root@cloud:~#source  .venv/py3.12-certbot/bin/activate
(py3.12-certbot) root@cloud:~#pip install pip install --upgrade certbot certbot-dns-ovh
 
Les secrets de l'api
(py3.12-certbot) root@cloud:~/letsencrypt# ls -alh ./.secrets/
total 12K
drwxr-xr-x 2 root     root     4,0K août   5 13:17 .
drwxr-xr-x 6 www-data www-data 4,0K août   5 13:17 ..
-rw------- 1 www-data www-data  229 août   5 13:45 ovh.ini
(py3.12-certbot) root@cloud:~/letsencrypt# 
(py3.12-certbot) root@cloud:~/letsencrypt# cat ./.secrets/ovh.ini 
# Informations pour l'accès à l'API OVH
dns_ovh_endpoint = ovh-eu
dns_ovh_application_key = ....
dns_ovh_application_secret = ...
dns_ovh_consumer_key = ...
(py3.12-certbot) root@cloud:~/letsencrypt# 
 
Fichier de configuration pour certbot
(py3.12-certbot) root@cloud:~/letsencrypt# 
(py3.12-certbot) root@cloud:~/letsencrypt# cd config/
(py3.12-certbot) root@cloud:~/letsencrypt/config# 
(py3.12-certbot) root@cloud:~/letsencrypt/config# cat cli.ini 
# cli.ini – configuration globale certbot
config-dir = /root/letsencrypt/config
work-dir = /root/letsencrypt/work
logs-dir = /root/letsencrypt/logs
# Adresse e-mail par défaut
email = xxxxx@gmail.com
agree-tos = true
no-eff-email = true
 
Générer les certificats 
(py3.12-certbot) root@cloud:~# certbot certonly --config /root/letsencrypt/config/cli.ini --dns-ovh --dns-ovh-credentials /root/letsencrypt/.secrets/ovh.ini -d "*.cosmic.ovh" -d "cosmic.ovh"    -d "*.grey.cosmic.ovh"   -d "*.green.cosmic.ovh"
 Lister les certificats
 (py3.12-certbot) root@cloud:~/letsencrypt# certbot certificates   --concertbot certificates --config /root/letsencrypt/config/cli.ini --dns-ovh --dns-ovh-credentials /root/letsencrypt/.secrets/ovh.ini


Copie des *pem vers les equipements cibles

(py3.12-certbot) root@cloud:~/letsencrypt/config/live/xxxx.ovh# scp -P 2222 -O ./*pem root@10.0.1.1:/etc/ssl/xxxx.ovh/



Révocation et suppression des certificats

(py3.12-certbot) root@cloud:~#certbot revoke   --cert-path /root/letsencrypt/config/live/xxxx.ovh/cert.pem   --key-path /root/letsencrypt/config/live/xxxx.ovh/privkey.pem --config /root/letsencrypt/config/cli.ini

Cas d'une instance openwrt : https
root@router:/etc/ssl#chmod 600 /etc/ssl/cosmic.ovh/privkey.pem
root@router:/etc/ssl#chmod 644 /etc/ssl/cosmic.ovh/fullchain.pem
root@router:/etc/ssl#uci set uhttpd.main.cert='/etc/ssl/cosmic.ovh/fullchain.pem' root@router:/etc/ssl#uci set uhttpd.main.key='/etc/ssl/cosmic.ovh/privkey.pem'
root@router:/etc/ssl#uci commit uhttpd
root@router:/etc/ssl#/etc/init.d/uhttpd restart

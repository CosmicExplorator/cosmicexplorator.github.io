---
title: "Générer un certificat Let's Encrypt avec OVH"
url: /itech/crt_management/genCrtChallengeDnsOvh/
description: "Créer un certificat Let's Encrypt avec Certbot et le challenge DNS OVH."
weight: 10
---

## Prérequis

- un domaine géré par OVH ;
- Python 3 et `venv` ;
- un accès administrateur au serveur.

## 1. Créer les identifiants OVH

Ouvrir le [formulaire de création d’un jeton OVH](https://www.ovh.com/auth/api/createToken), puis autoriser :

- `GET /domain/zone/*` ;
- `PUT /domain/zone/*` ;
- `POST /domain/zone/*` ;
- `DELETE /domain/zone/*` ;
- `POST /domain/zone/*/refresh`.

Créer `/root/letsencrypt/.secrets/ovh.ini` :

```ini
dns_ovh_endpoint = ovh-eu
dns_ovh_application_key = ...
dns_ovh_application_secret = ...
dns_ovh_consumer_key = ...
```

```bash
chmod 600 /root/letsencrypt/.secrets/ovh.ini
```

## 2. Installer Certbot

```bash
python3 -m venv /root/.venv/certbot
source /root/.venv/certbot/bin/activate
pip install --upgrade pip certbot certbot-dns-ovh
```

## 3. Configurer Certbot

Créer `/root/letsencrypt/config/cli.ini` :

```ini
config-dir = /root/letsencrypt/config
work-dir = /root/letsencrypt/work
logs-dir = /root/letsencrypt/logs
email = adresse@example.com
agree-tos = true
no-eff-email = true
```

## 4. Générer le certificat

```bash
certbot certonly \
  --config /root/letsencrypt/config/cli.ini \
  --dns-ovh \
  --dns-ovh-credentials /root/letsencrypt/.secrets/ovh.ini \
  -d "*.example.com" \
  -d "example.com"
```

## 5. Contrôler le résultat

```bash
certbot certificates --config /root/letsencrypt/config/cli.ini
```

Les fichiers sont dans `/root/letsencrypt/config/live/example.com/`.

## 6. Déployer le certificat

Exemple avec SSH :

```bash
scp -P 2222 -O \
  /root/letsencrypt/config/live/example.com/*.pem \
  root@10.0.1.1:/etc/ssl/example.com/
```

Pour OpenWrt :

```bash
chmod 600 /etc/ssl/example.com/privkey.pem
chmod 644 /etc/ssl/example.com/fullchain.pem
uci set uhttpd.main.cert='/etc/ssl/example.com/fullchain.pem'
uci set uhttpd.main.key='/etc/ssl/example.com/privkey.pem'
uci commit uhttpd
/etc/init.d/uhttpd restart
```

## Révoquer le certificat

```bash
certbot revoke \
  --cert-path /root/letsencrypt/config/live/example.com/cert.pem \
  --key-path /root/letsencrypt/config/live/example.com/privkey.pem \
  --config /root/letsencrypt/config/cli.ini
```

## Checklist

- [ ] Jeton OVH créé avec les droits nécessaires
- [ ] `ovh.ini` protégé en mode `600`
- [ ] Certificat généré et contrôlé
- [ ] Certificat déployé
- [ ] HTTPS vérifié sur la cible

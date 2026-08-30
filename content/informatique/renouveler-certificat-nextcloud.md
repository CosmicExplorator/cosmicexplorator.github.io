---
title: "Renouveler le certificat Nextcloud"
url: /itech/crt_management/renewCertForNextcloud/
description: "Automatiser le renouvellement d’un certificat Let's Encrypt pour Nextcloud."
weight: 40
---

## Prérequis

- Certbot et `certbot-dns-ovh` installés ;
- identifiants OVH dans `/root/letsencrypt/.secrets/ovh.ini` ;
- certificat déjà créé.

## 1. Générer le certificat

```bash
certbot certonly \
  --dns-ovh \
  --dns-ovh-credentials /root/letsencrypt/.secrets/ovh.ini \
  -d example.com \
  --config-dir /root/letsencrypt/config \
  --work-dir /root/letsencrypt/work \
  --logs-dir /root/letsencrypt/logs
```

## 2. Tester le renouvellement

```bash
certbot renew --dry-run \
  --config-dir /root/letsencrypt/config \
  --work-dir /root/letsencrypt/work \
  --logs-dir /root/letsencrypt/logs
```

## 3. Créer le script

Créer `/root/letsencrypt/renew.sh` :

```bash
#!/usr/bin/env bash
set -euo pipefail

certbot renew \
  --config-dir /root/letsencrypt/config \
  --work-dir /root/letsencrypt/work \
  --logs-dir /root/letsencrypt/logs \
  --dns-ovh \
  --dns-ovh-credentials /root/letsencrypt/.secrets/ovh.ini

systemctl reload apache2
```

```bash
chmod 700 /root/letsencrypt/renew.sh
```

## 4. Planifier l’exécution

Ajouter avec `crontab -e` :

```cron
30 12 * * 0,3 /root/letsencrypt/renew.sh
```

## Checklist

- [ ] Renouvellement à blanc réussi
- [ ] Script exécutable
- [ ] Tâche cron installée
- [ ] Apache rechargé après renouvellement
- [ ] Nouveau certificat visible dans Nextcloud

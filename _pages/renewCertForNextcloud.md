# Renouvellement Automatique Certificat Let's Encrypt Nextcloud

Voici la procédure que j'utilise pour renouveler automatiquement un certificat
Let's Encrypt via acme.sh et OVH DNS.


## 0. Ptit mémo: arboresence

```
root@nextcloud:~/letsencrypt# tree -d -a
.
├── config
│   ├── accounts
│   │   └── acme-v02.api.letsencrypt.org
│   │       └── directory
│   │           └── 99b2791cd2c5f9982788289fceb80b6c
│   ├── archive
│   │   └── xxxxx.ovh
│   ├── live
│   │   └── xxxxx.ovh
│   ├── renewal
│   └── renewal-hooks
│       ├── deploy
│       ├── post
│       └── pre
├── logs
├── .secrets
└── work
    └── backups
```
## 1. Les variables pour l'Api OVH

```bash
root@nextcloud:~/letsencrypt/.secrets# cat ovh.ini
# Informations pour l'accès à l'API OVH
dns_ovh_endpoint = ovh-eu
dns_ovh_application_key = xxxxx
dns_ovh_application_secret = xxxxx
dns_ovh_consumer_key = xxxxx
```


## 2. Générer le certificat

```bash
certbot certonly --dns-ovh -d xxxxx.ovh  --config-dir ~/letsencrypt/config     --work-dir ~/letsencrypt/work     --logs-dir ~/letsencrypt/logs
```

## 3. Renouveller le certificat


```bash
certbot renew --config-dir ~/letsencrypt/config --work-dir ~/letsencrypt/work --logs-dir ~/letsencrypt/logs
```


## 4. Automatiser le renouvellement


```bash
root@nextcloud:~/letsencrypt# crontab -l
# Edit this file to introduce tasks to be run by cron.
# ....
# m h  dom mon dow   command
30 12 * * 0,3 /root/letsencrypt/renew.sh  && systemctl reload apache2
```

### le script renew.sh
```bash
#!/bin/bash
certbot  renew --config-dir /root/letsencrypt/config --work-dir /root/letsencrypt/work --logs-dir /root/letsencrypt/logs --dns-ovh --dns-ovh-credentials /root/letsencrypt/.secrets/ovh.ini
```

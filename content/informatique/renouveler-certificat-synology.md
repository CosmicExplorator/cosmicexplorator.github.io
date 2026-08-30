---
title: "Renouveler le certificat Synology"
url: /itech/crt_management/renewCertForDSM/
description: "Générer et déployer un certificat Let's Encrypt sur Synology DSM."
weight: 20
---

## Prérequis

- accès SSH au NAS ;
- domaine géré par OVH ;
- clés API OVH `AK`, `AS` et `CK`.

## 1. Installer acme.sh

```bash
curl https://get.acme.sh | sh -s -- \
  --accountemail "adresse@example.com" \
  --nocron
```

## 2. Configurer OVH

Créer `~/.acme.sh/ovh.ini` :

```bash
export OVH_AK="..."
export OVH_AS="..."
export OVH_CK="..."
```

```bash
chmod 600 ~/.acme.sh/ovh.ini
```

## 3. Générer le certificat

```bash
source ~/.acme.sh/ovh.ini
~/.acme.sh/acme.sh --issue \
  -d example.com \
  --dns dns_ovh \
  --server letsencrypt
```

## 4. Déployer dans DSM

```bash
source ~/.acme.sh/ovh.ini
~/.acme.sh/acme.sh --deploy \
  --home ~/.acme.sh/ \
  -d example.com \
  --deploy-hook synology_dsm
```

## 5. Automatiser

1. ouvrir **Panneau de configuration → Planificateur de tâches** ;
2. créer une tâche planifiée ;
3. charger `ovh.ini`, puis lancer `acme.sh --cron` ;
4. contrôler le journal après la première exécution.

## Checklist

- [ ] `ovh.ini` protégé
- [ ] Certificat généré
- [ ] Déploiement DSM réussi
- [ ] Tâche planifiée testée
- [ ] Certificat présenté par DSM vérifié

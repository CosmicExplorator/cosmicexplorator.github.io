---
title: "Sauvegarder Nextcloud avec Kopia"
url: /itech/backup/svgWithKopia/
description: "Sauvegarder un serveur Nextcloud sur un NAS Synology avec Kopia."
weight: 50
---

## Architecture

{{< mermaid >}}
flowchart LR
    N["Serveur Nextcloud<br/>Kopia :51515"] -->|"Montage NFS<br/>snapshot planifié"| S["NAS Synology<br/>dépôt de sauvegarde"]
{{< /mermaid >}}

## Prérequis

- le partage NFS du NAS est monté ;
- le NAS est actif pendant la sauvegarde ;
- les certificats TLS de Kopia sont disponibles ;
- les scripts de maintenance Nextcloud sont testés.

## 1. Installer Kopia

```bash
apt install kopia -y
```

## 2. Vérifier le montage NFS

```bash
mount | grep /media/nas2b_for_kopia
```

Arrêter si le montage est absent.

## 3. Créer le dépôt

```bash
kopia repository create server \
  --url https://localhost:51515 \
  --username USER \
  --password PASSWORD \
  --path /media/nas2b_for_kopia
```

## 4. Démarrer le serveur Kopia

```bash
/usr/bin/kopia server start \
  --address=0.0.0.0:51515 \
  --ui \
  --tls-cert-file=/etc/ssl/example.com/fullchain.pem \
  --tls-key-file=/etc/ssl/example.com/privkey.pem \
  --server-username=USER \
  --server-password=PASSWORD \
  --config-file=/root/.config/kopia/repository.config
```

Interface : `https://ADRESSE_IP:51515`.

## 5. Configurer la stratégie

Avant le snapshot :

- activer le mode maintenance Nextcloud ;
- sauvegarder la base de données.

Après le snapshot :

- désactiver le mode maintenance.

```bash
kopia policy set /media/nextcloud-raid1/nextcloud \
  --before-snapshot-root-action="/chemin/nextcloud_maintenance_on_dump_bdd.sh" \
  --after-snapshot-root-action="/chemin/nextcloud_maintenance_off.sh" \
  --snapshot-time=12:20 \
  --password=PASSWORD
```

## 6. Contrôler

- vérifier l’exécution des deux scripts ;
- vérifier la présence du snapshot dans l’interface ;
- consulter les journaux Kopia ;
- effectuer un test de restauration.

![Vue du serveur Kopia](/assets/images/svgWithKopia/2026-02-15_20-17.png)

![Snapshots Kopia](/assets/images/svgWithKopia/2026-02-15_19-55.png)

![Détail d’un snapshot](/assets/images/svgWithKopia/2026-02-15_19-56.png)

## Checklist

- [ ] Montage NFS actif
- [ ] Dépôt Kopia accessible
- [ ] Serveur HTTPS opérationnel
- [ ] Scripts avant/après exécutés
- [ ] Snapshot présent
- [ ] Restauration testée

# Renouvellement d'un certificat Let's Encrypt sur Synology

Voici la procédure que j'utilise pour renouveler automatiquement un certificat
Let's Encrypt via acme.sh et OVH DNS.

## 1. Préparer les variables OVH

Créer un fichier `ovh.ini` :

OVH_AK="xxx"
OVH_AS="xxx"
OVH_CK="xxx"

## 2. Générer le certificat


acme.sh  --issue --dns dns_ovh -d nas2b.grey.cosmic.ovh

## 3. Déployer sur Synology


acme.sh  --deploy -d nas2b.grey.cosmic.ovh  --deploy-hook synology_dsm


## 4. Automatiser

Créer une tâche planifiée dans DSM :

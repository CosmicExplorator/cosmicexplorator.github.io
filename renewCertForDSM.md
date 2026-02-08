# Renouvellement d'un certificat Let's Encrypt sur Synology

Voici la procédure que j'utilise pour renouveler automatiquement un certificat
Let's Encrypt via acme.sh et OVH DNS.

## 1. Préparer les variables OVH

Créer un fichier `ovh.ini` :
```bash
cat ovh.ini
# Informations pour l'accès à l'API OVH
export OVH_AK="xxxxx"
export OVH_AS="xxxxx"
export OVH_CK="xxxxx"
```
## 2. Générer le certificat


acme.sh  --issue --dns dns_ovh -d nas2b.grey.cosmic.ovh

## 3. Déployer sur Synology


acme.sh  --deploy -d nas2b.grey.cosmic.ovh  --deploy-hook synology_dsm


## 4. Automatiser

Créer une tâche planifiée dans DSM :
